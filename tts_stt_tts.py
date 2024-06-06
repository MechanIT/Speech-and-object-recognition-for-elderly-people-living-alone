from gtts import gTTS
import pygame
import io
import speech_recognition as sr

def play_text(text, lang='ko'):
    # 텍스트를 음성으로 변환
    tts = gTTS(text=text, lang=lang)
    
    # 변환된 음성을 메모리에 저장
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # pygame 초기화 및 설정
    pygame.init()
    pygame.mixer.init()
    
    # 변환된 음성을 pygame을 통해 재생
    pygame.mixer.music.load(fp, 'mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def recognize_speech_from_mic(recognizer, microphone):
    """음성 인식을 통해 텍스트를 반환합니다."""

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
        response["transcription"] = recognizer.recognize_google(audio, language='ko-KR') # 인식 언어 한국어로 지정.
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API 요청 실패"
    except sr.UnknownValueError:
        response["error"] = "음성을 이해할 수 없음"

    return response

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # 텍스트를 음성으로 출력
    text_to_speak = '시작' #"음성 인식을 시작합니다."
    play_text(text_to_speak)
    
    # 음성 인식 시작
    print("음성 인식 시작...")
    response = recognize_speech_from_mic(recognizer, microphone)
    
    # if response["success"]:
    #     print("인식된 텍스트: {}".format(response["transcription"]))    
    #     recognition_success_msg = "좋은 하루 보내세용."
    #     play_text(recognition_success_msg)
    # else:
    #     print("에러: {}".format(response["error"]))
    if response["success"]:
        if response["transcription"]:
            print("인식된 텍스트: {}".format(response["transcription"]))
            success_message = "좋은 하루 보내세용."
            print('사용자의 음성이 정상적으로 인식 되었습니다.')
            play_text(success_message)
        else:
            print("아무 음성도 인식되지 않았습니다. \n영상 탐지를 시작합니다.")
            play_text('음성이 인식되지 않습니다. 영상 탐지를 시작합니다.')
    else:
        print("에러: {}".format(response["error"]))
