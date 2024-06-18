import subprocess


def main():
    try:
        # sound_generation 실행
        print("sound_generation.py 실행 중...")
        subprocess.run(['python', 'sound_generation.py'])

        # timesetup 실행
        print("timesetup.py 실행 중...")
        subprocess.run(['python', 'timesetup.py'])

        # # tts_stt_tts 실행
        # print("tts_stt_tts.py 실행 중...")
        # subprocess.run(['python', 'tts_stt_tts.py'])

        # # speech_management 실행
        # print("speech_management.py 실행 중...")
        # subprocess.run(['python', 'speech_management.py'])

        # # my_speech_recognition 실행
        # print("my_speech_recognition.py 실행 중...")
        # subprocess.run(['python', 'my_speech_recognition.py'])

        # print("emergency_alert.py 실행 중...")
        # subprocess.run(['python', 'emergency_alert.py'])

        # # webpage_view 실행
        # print("webpage_view.py 실행 중...")
        # subprocess.run(['python', 'webpage_view.py'])

        

        print("모든 스크립트가 성공적으로 실행되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
