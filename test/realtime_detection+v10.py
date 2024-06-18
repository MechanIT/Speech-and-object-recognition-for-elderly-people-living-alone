import torch
import cv2
import numpy as np
# from yolov5 import YOLOv5
from ultralytics import YOLOv10

# YOLOv5 모델 로드
# model = YOLOv10.from_pretrained('jameslahm/yolov10{n/s/m/b/l/x}') 
# 저장소 ID는 'repo_name' 또는 'namespace/repo_name' 형태여야 합니다. 메시지에서 'jameslahm/yolov10{n/s/m/b/l/x}'가 올바른 형식이 아니라고 지적
model = YOLOv10.from_pretrained('jameslahm/yolov10n')  # 예시로 'yolov10n' 사용


# 웹캠 연결
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 모델을 사용하여 객체 탐지
    results = model(frame)
    # 결과 구조 확인 (디버깅용)
    print(type(results))
    print(results)
    
    # 결과를 이미지에 표시
    # labels, cords = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
    # for label, cord in zip(labels, cords):
    #     x1, y1, x2, y2, conf = cord
    #     x1, y1, x2, y2 = int(x1 * frame.shape[1]), int(y1 * frame.shape[0]), int(x2 * frame.shape[1]), int(y2 * frame.shape[0])
    #     label_name = model.names[int(label)]
        
    #     # 박스 및 라벨 그리기
    #     cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    #     cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
  
    for result in results:
        boxes = result.boxes.xyxy.numpy()  # bounding boxes
        confidences = result.boxes.conf.numpy()  # confidences
        class_ids = result.boxes.cls.numpy()  # class ids
        
        for box, conf, cls_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            label_name = model.names[int(cls_id)]
            
            # 박스 및 라벨 그리기
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f'{label_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    
    
    # 결과 이미지 표시
    cv2.imshow('YOLOv10 Detection', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
