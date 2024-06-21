import cv2
from speech_management import recognize_speech, play_text
from object_detection import detect_person, detect_motion
from emergency_alert import send_alert

# def play_text():
#     print("사용자를 불러오는 중...")

def main():
    def no_response_callback():
        cap = cv2.VideoCapture(0)
        ret, prev_frame = cap.read()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if detect_person(frame):
                play_text()
                for _ in range(30):
                    ret, frame = cap.read()
                    if detect_person(frame):
                        return
                    if detect_motion(prev_frame, frame):
                        break
                else:
                    send_alert()
                    return

            prev_frame = frame

    while True:
        command = recognize_speech(no_response_callback, send_alert)
        if command:
            print(f"음성 명령 인식: {command}")

if __name__ == "__main__":
    main()
