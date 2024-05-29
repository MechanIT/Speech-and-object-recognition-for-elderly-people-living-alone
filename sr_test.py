import speech_recognition as sr
'''
    구글 Web Speech API는 편리하지만 하루에 50회 호출 제한이 있다.
'''


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer`는 `Recognizer` 인스턴스여야 합니다.")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone`은 `Microphone` 인스턴스여야 합니다.")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something!")
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

    print("음성 인식 시작...")
    response = recognize_speech_from_mic(recognizer, microphone)
    
    if response["success"]:
        print("인식된 텍스트: {}".format(response["transcription"]))
    else:
        print("에러: {}".format(response["error"]))

