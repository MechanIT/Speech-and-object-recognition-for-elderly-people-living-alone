import speech_recognition as sr

from gtts import gTTS
import pygame
import io

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

def recognize_speech(callback, emergency_callback):
    # 음성을 텍스트로 반환
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("듣고 있어요...")
        audio = recognizer.listen(source)
        
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        # command = recognizer.recognize_google(audio)
        command = response["transcription"] 
        command = recognizer.recognize_google(audio, language='ko-KR')
        print(f"Recognized command: {command}")
        if "도와줘" in command:
            emergency_callback()
            return None
        return command
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API 요청 실패"
    except sr.UnknownValueError:
        response["error"] = "음성을 이해할 수 없음"
        callback()
        return None
    return response
