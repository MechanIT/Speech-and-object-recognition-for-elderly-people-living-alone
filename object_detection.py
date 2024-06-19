import subprocess
import cv2

def run_detection():
    command = [
        'python', 'detect_modified.py',
        '--weights', 'best_v7.pt',
        '--conf', '0.25',
        '--img-size', '640',
        '--source', '0'  # 카메라 소스
    ]
    
    # 지정된 인수와 함께 detect.py 호출
    subprocess.run(command)


def detect_motion(prev_frame, current_frame, threshold_value=100, min_contour_area=2000):
    diff_frame = cv2.absdiff(prev_frame, current_frame) # 프레임 차이 계산
    gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY) # 그레이스케일 변환
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # 가우시안 블러 적용
    _, thresh = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY) # 이진화 - 임계값을 높여서 작은 차이를 무시
    dilated = cv2.dilate(thresh, None, iterations=3)    # 팽창 - 노이즈 제거 및 객체 강조
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 외곽선 찾기
    
    # 최소 면적 조건을 높여서 큰 움직임만 감지
    return any(cv2.contourArea(contour) > min_contour_area for contour in contours)

if __name__ == "__main__":
    run_detection()