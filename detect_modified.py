import cv2
import torch
import time
import threading

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.plots import plot_one_box
from utils.torch_utils import select_device, TracedModel

import numpy as np
from my_speech_recognition import play_text
from emergency_alert import send_alert


# 웹캠 스트림 초기화
cap = cv2.VideoCapture(0)  # '0'은 기본 웹캠 장치를 의미합니다.

def detect_motion(prev_frame, current_frame, threshold_value=100, min_contour_area=2000):
    diff_frame = cv2.absdiff(prev_frame, current_frame) # 프레임 차이 계산
    gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY) # 그레이스케일 변환
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # 가우시안 블러 적용
    _, thresh = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY) # 이진화 - 임계값을 높여서 작은 차이를 무시
    dilated = cv2.dilate(thresh, None, iterations=3)    # 팽창 - 노이즈 제거 및 객체 강조
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 외곽선 찾기
    
    # 최소 면적 조건을 높여서 큰 움직임만 감지
    return any(cv2.contourArea(contour) > min_contour_area for contour in contours)

def voice_output(text):
    play_text(text)

def detect():
    # 모델 로드
    weights = 'best_v7.pt'
    device = select_device('')
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(640, s=stride)  # check img_size

    model = TracedModel(model, device, 640)

    half = device.type != 'cpu'  # half precision only supported on CUDA
    if half:
        model.half()  # to FP16

    # 이름과 색상 가져오기
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]
    
    prev_frame = None
    response_timer = time.time()
    print(response_timer)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        img = letterbox(frame, imgsz, stride=stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        
        
        # # 추론
        # pred = model(img, augment=False)[0]
        # pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)
        person_detected = False

        for det in pred:  # 감지된 객체마다
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

                for *xyxy, conf, cls in det:
                    label_name = names[int(cls)]
                    if label_name == "person":
                        person_detected = True
                        x1, y1, x2, y2 = map(int, xyxy)
                        # 박스 및 라벨 그리기
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    if label_name == "fallen person":
                        fallen_person_detected = True
                        x1, y1, x2, y2 = map(int, xyxy)
                        # 박스 및 라벨 그리기
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        
        # 웹캠 프레임을 화면에 표시
        cv2.imshow('YOLOv7 Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # 감지 결과 처리
        for i, det in enumerate(pred):  # 이미지당 감지
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

                person_detected = any(names[int(cls)] == "person" for cls in det[:, -1].tolist())
                fallen_person_detected = any(names[int(cls)] == "fallen person" for cls in det[:, -1].tolist())
                print(person_detected)
                
                if fallen_person_detected:
                    print("쓰러진 사용자 : 비정상적인 상황 감지.")
                    threading.Thread(target=voice_output, args=("쓰러진 사용자가 감지되었습니다. 비상 메일을 발송합니다.",)).start()
                    send_alert()
                    return # 루프 종료
                
                if person_detected:
                    last_seen = time.time()
                    print("사용자가 인식됨. 움직임 추가 요청")
                    threading.Thread(target=voice_output, args=("사용자가 인식되었습니다. 정확한 확인을 위해 움직여주세요",)).start()

                    # 10초 동안 움직임 감지
                    movement_detected = False
                    start_time = time.time()
                    while time.time() - start_time < 10:
                        ret, frame = cap.read()
                        if not ret:
                            print("프레임을 읽을 수 없습니다.")
                            break
                        if prev_frame is not None:
                            if detect_motion(prev_frame, frame):
                                movement_detected = True
                                break
                        prev_frame = frame
                        time.sleep(1)

                    if movement_detected:
                        print("정상적인 움직임 감지 : 확인 완료")
                        threading.Thread(target=voice_output, args=("정상적인 움직임이 감지되었습니다. 확인 완료.",)).start()
                        return
                    else:
                        print("움직임 감지되지 않음 : 비정상적인 상황 감지.")
                        threading.Thread(target=voice_output, args=("움직임이 감지되지 않습니다. 비상 메일을 발송합니다.",)).start()
                        send_alert()
                        return
            # if not person_detected: 캠에서 인식되는 객체가 없으면 false가 아니라 아예 아무 반응이x
            print(time.time())
            if (time.time() - response_timer) > 5:  # 10초 동안 반응이 없으면

                print("사용자가 시야에서 확인되지 않습니다.")
                threading.Thread(target=voice_output, args=("확인을 위해 카메라 앞으로 와주세요",)).start()
                start_time = time.time()
                while time.time() - start_time < 10:
                    time.sleep(0.5)
                    ret, frame = cap.read()
                    if not ret:
                        print("프레임을 읽을 수 없습니다.")
                        break
                    img = letterbox(frame, imgsz, stride=stride)[0]
                    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
                    img = np.ascontiguousarray(img)

                    img = torch.from_numpy(img).to(device)
                    img = img.half() if half else img.float()  # uint8 to fp16/32
                    img /= 255.0  # 0 - 255 to 0.0 - 1.0
                    if img.ndimension() == 3:
                        img = img.unsqueeze(0)

                    pred = model(img, augment=False)[0]
                    pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)

                    person_detected = any(names[int(cls)] == "person" for cls in det[:, -1].tolist())
                    if person_detected:
                        print("사용자가 나타났습니다 : 정상 종료")
                        threading.Thread(target=voice_output, args=("사용자가 정상적으로 확인되었습니다.",)).start()
                        prev_frame = frame
                        return

                if not person_detected:
                    print("시야 내에서 사용자 확인 불가 : 비정상적인 상황 감지")
                    threading.Thread(target=voice_output, args=("사용자를 찾을 수 없습니다. 위험 상황이 발생할 수 있습니다. 비상 메일을 발송합니다.",)).start()
                    send_alert()
                    return

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect()
