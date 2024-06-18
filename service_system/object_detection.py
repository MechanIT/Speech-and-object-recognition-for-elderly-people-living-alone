import torch
import cv2

# 사용자 정의 모델 로드
model_path = '/Users/yangseyoung/sookmyung/24-1/opensource/service_integration/best.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

def detect_person(frame):
    results = model(frame)
    labels = results.xyxyn[0][:, -1].numpy()
    return any(label == 0 for label in labels)  # assuming '0' is the label for person

def detect_motion(prev_frame, current_frame):   # 임시 움직임 감지 코드
    diff_frame = cv2.absdiff(prev_frame, current_frame)
    gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return any(cv2.contourArea(contour) > 500 for contour in contours)

# 카메라를 통해 프레임을 캡처하고 감지하는 메인 루프
def main():
    cap = cv2.VideoCapture(0)
    ret, prev_frame = cap.read()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 사람 감지
        if detect_person(frame):
            print("사람이 감지되었습니다.")

        # 움직임 감지
        if detect_motion(prev_frame, frame):
            print("움직임이 감지되었습니다.")

        prev_frame = frame

        # 프레임을 표시 (옵션)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
