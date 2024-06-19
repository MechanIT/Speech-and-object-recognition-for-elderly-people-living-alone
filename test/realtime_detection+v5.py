"""
  git clone yolov5 후 해당 경로에서 실행시킴
"""
import torch
import cv2
import numpy as np
# from yolov5 import YOLOv5


# 사용자 정의 가중치 파일 경로
MODEL_PATH = "C:/Users/wltns/Downloads/best.pt"

# YOLOv9 모델 로드 (여기서는 YOLOv5를 사용)
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)

# # YOLOv5 모델 로드
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 웹캠 연결
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 모델을 사용하여 객체 탐지
    results = model(frame)
    
    # 결과를 이미지에 표시
    labels, cords = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
    for label, cord in zip(labels, cords):
        x1, y1, x2, y2, conf = cord
        x1, y1, x2, y2 = int(x1 * frame.shape[1]), int(y1 * frame.shape[0]), int(x2 * frame.shape[1]), int(y2 * frame.shape[0])
        label_name = model.names[int(label)]
        
        # 박스 및 라벨 그리기
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    
    # 결과 이미지 표시
    cv2.imshow('YOLOv5 Detection', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
