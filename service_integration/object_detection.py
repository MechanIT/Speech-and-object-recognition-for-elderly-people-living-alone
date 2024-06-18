import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

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
