import cv2
import numpy as np
VidioSignal = cv2.VideoCapture(0)
Yolo_net = cv2.dnn.readNet('yolov3_tiny.weights', 'yolov3_tiny.cfg')
with open('yolo_name.txt', 'r', encoding='utf-8') as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = Yolo_net.getLayerNames()
output_layer = [layer_names[i-1] for i in Yolo_net.getUnconnectedOutLayers()]
cv2.namedWindow('YOLO3_CM_01')


while True:

    # 카메라에서 영상 읽어들이기
    ret, frame = VidioSignal.read()
    # frame 정보에서 높이, 너비, 채널(흑백 또는 컬러)추출하기
    h,w,c = frame.shape
    # --------------------- 
    # Blob 데이터 구조화
    blob = cv2.dnn.blobFromImage(
        # 카메라에서 읽어들인 frame(이미지) 데이터
        image = frame,
        # 이미지 픽셀 값 정규화(스케일링)
        scalefactor = 1/255.0,
        # Yolo 모델이 사용할 크기로 조정
        size=(416,416),
        # BGR,RGB 선택
        # - True 이면 OpenCV의 기본 BGR 색상 순서를 RGB로 변경
        swapRB = True,
        # 위에 size로 조정 후 어떻게 할지 결정
        # - True : 잘라내기
        # - False : size로 전체 조정하기
        crop = False
    )
    # YOLO 입력 데이터로 넣어주기
    Yolo_net.setInput(blob)
    # YOLO 모델에 출력계층 이름을 알려주고 출력결과 받아오기
    outs = Yolo_net.forward(output_layer)
    # 라벨명칭 담을 리스트 변수
    class_ids = []
    # 정확도 담을 리스트 변수
    confidences = []
    # 바운딩 박스의 좌표를 담을 리스트 변수
    boxes = []
    # 출력 결과 여러개(인식된 객체 여러개)
    for out in outs:
        # 실제 객체 인식 데이터 처리
        for detection in out:
            # 인식 데이터의 인식률(정밀도)
            scores = detection[5:]
            # 인식률(정밀도)가 가장 높은 인덱스 위치 얻기 : 라벨의 위치값
            class_id = np.argmax(scores)
            # 인식률 값 추출하기 : class_id의 인덱스번호 위치값이 정밀도
            confidence = scores[class_id]
            # 정밀도가 50% 이상인 경우만 처리 : 기준은 자유롭게 정의
            if confidence > 0.5:
                # 중앙값의 좌표 비율에 실제 너비로 연산하여 중앙 x값 추출
                center_x = int(detection[0] * w)
                # 중앙값의 좌표 비율에 실제 높이로 연산하여 중앙 y값 추출
                center_y = int(detection[1] * h)
                # 바운딩 박스의 실제 너비와 높이 계산하기
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # 바운딩 박스의 시작좌표(x,y)계산하기
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                
                boxes.append([x,y,dw,dh])
                class_ids.append(class_id)
                confidences.append(float(confidence))
    
    # 중복된 바운딩 박스 제거하기
    # - 정확도가 0.45보다 작으면 제거하기
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.45,0.4)
    # 바운딩 박스 처리하기
    for i in range (len(boxes)):
        # 중복 제거 이후 남은 바운딩 박스의 정보만 이용
        if i in indexes:
            # 해당 객체에 대한 좌표값
            x,y,w,h = boxes[i]
            # 해당 객체에 대한 라벨값
            label = str(classes[class_ids[i]])
            # 해당 객체에 대한 정확도
            score = confidences[i]
            
            # 바운딩 박스 그리기
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5)
            # 라벨, 정확도 이미지에 그리기
            cv2.putText(
                # 지금까지 그려진 frame 이미지
                img = frame,
                # 추가할 텍스트(문자열타입으로)
                text = label, 
                # 텍스트 시작 위치 지정
                org=(x,y-20),
                # 텍스트 font 스타일
                fontFace = cv2.FONT_ITALIC,
                # font 크기
                fontScale = 0.5, 
                # font 색상 
                color = (255,255,255),
                # font 선굵기
                thickness =1)
            
    
    
                
    # 윈도우 창 open하기
    cv2.imshow('YOLO3_CM_01',frame)
    # 윈도우 창 크기 조절하기
    cv2.resizeWindow('YOLO3_CM_01',650,500)

    # 키보드에서 아무키 눌리면 while문 종료하기
    if cv2.waitKey(100) > 0:
        # 윈도우 무조건 종료
        cv2.destroyAllWindows()
        break
    # 키보드에서 q 입력시 종료시키기
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break