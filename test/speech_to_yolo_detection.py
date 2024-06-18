import cv2
import io
import pygame
import speech_recognition as sr
import time
import schedule
from gtts import gTTS
from ultralytics import YOLOv10
import smtplib
from email.message import EmailMessage
import threading
import flask_webcam_stream  # Flask 웹 서버를 별도의 스레드에서 실행시킴

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_ADDR = 'wltnslagg@sookmyung.ac.kr'
EMAIL_PASSWORD = 'fdtkexjgfususojy'

def play_text(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(fp, 'mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer`는 `Recognizer` 인스턴스여야 합니다.")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone`은 `Microphone` 인스턴스여야 합니다.")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("말씀하세요!")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language='ko-KR')
        if "도와" in response["transcription"]: # (eg. "'도와'줘", "'도와'주세요!")
            # 위험상황3: 언제든 도움을 요청하는 음성 메세지가 인식될 때
            send_alert()
            return None
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API 요청 실패"
    except sr.UnknownValueError:
        response["error"] = "음성을 이해할 수 없음"

    return response

def detect_motion(prev_frame, current_frame, threshold_value=50, min_contour_area=1000):
    
    diff_frame = cv2.absdiff(prev_frame, current_frame) # 프레임 차이 계산
    gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY) # 그레이스케일 변환
    blur = cv2.GaussianBlur(gray, (5, 5), 0) # 가우시안 블러 적용
    _, thresh = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY) # 이진화 - 임계값을 높여서 작은 차이를 무시
    dilated = cv2.dilate(thresh, None, iterations=3)    # 팽창 - 노이즈 제거 및 객체 강조
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 외곽선 찾기
    
    # 최소 면적 조건을 높여서 큰 움직임만 감지
    return any(cv2.contourArea(contour) > min_contour_area for contour in contours)

def start_yolo_detection():
    model = YOLOv10.from_pretrained('jameslahm/yolov10n')
    cap = cv2.VideoCapture(0)

    prev_frame = None
    last_seen = time.time()
    person_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        person_detected = any(model.names[int(cls_id)] == "person" for result in results for cls_id in result.boxes.cls.numpy())

        if person_detected:
            if prev_frame is None:
                prev_frame = frame
                continue

            if detect_motion(prev_frame, frame):
                last_seen = time.time()
            else:
                if time.time() - last_seen > 5:  # 5초 동안 움직임이 없으면
                    print("사용자에게서 비정상적인 상황이 감지되었습니다.")
                    play_text("움직임이 감지되지 않았습니다. 위험 상황이 발생할 수 있습니다.")
                    # 위험상황1: 안부 응답x, 카메라에 인식o, 움직이지x
                    send_alert()
                    break  # 루프 종료
            
            prev_frame = frame
        else:
            play_text("안녕하신지 확인하기 위해 카메라 앞으로 와주세요") #멘트 추천..
            time.sleep(10)  # 10초 기다림
            if not person_detected:
                print("사용자에게서 비정상적인 상황이 감지되었습니다.")
                play_text("카메라 앞에 나타나지 않았습니다. 위험 상황이 발생할 수 있습니다.")
                # 위험상황2: 안부 응답x, 카메라에 인식x, 호출 반응x
                send_alert()
                break  # 루프 종료

        cv2.imshow('YOLOv10 Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def send_alert():
    print("비상 상황! 긴급 연락을 취합니다.")
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)
        message = EmailMessage()
        message.set_content('http://172.30.1.9:5000 비상 상황이 발생했습니다. 즉시 조치를 취하십시오. ')
        message["Subject"] = "SOS : 사용자에게 비상 상황이 발생하였습니다"
        message["From"] = EMAIL_ADDR
        message["To"] = 'wltnslagg@naver.com'
        smtp.send_message(message)
        print("이메일을 성공적으로 보냈습니다.")

if __name__ == "__main__":
    # Start the Flask web-server in a separate thread
    flask_thread = threading.Thread(target=flask_webcam_stream.start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    text_to_speak = '시작' # initial 안부 음성
    play_text(text_to_speak)
    
    print("음성 인식 시작...")
    response = recognize_speech_from_mic(recognizer, microphone)
    
    if response["success"]:
        if response["transcription"]:
            print("인식된 텍스트: {}".format(response["transcription"]))
            success_message = "좋은 하루 보내세용."
            print('사용자의 음성이 정상적으로 인식 되었습니다.')
            play_text(success_message)
        else: #10/15/35 매우 다양..
            print("아무 음성도 인식되지 않았습니다. \n영상 탐지를 시작합니다.")
            play_text('음성이 인식되지 않습니다. 영상 탐지를 시작합니다.')
            start_yolo_detection()
    else:
        print("에러: {}".format(response["error"]))
