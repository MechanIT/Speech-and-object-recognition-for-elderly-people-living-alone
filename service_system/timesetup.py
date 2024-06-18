import schedule
import time
from pydub import AudioSegment
from pydub.playback import play
import subprocess
import concurrent.futures


# 음성 파일 재생 함수
def play_sound(file_name):
    try:
        audio = AudioSegment.from_file(file_name)
        play(audio)
        print(f"{file_name} 음성 파일이 재생되었습니다.")
        # 음성 파일 재생 후 다음 작업 실행
        run_next_script()
    except Exception as e:
        print(f"오류 발생: {e}")

# 다음 작업을 실행하는 함수
def run_next_script():
    # tts_stt_tts 실행
    print("tts_stt_tts.py 실행 중...")
    result = subprocess.run(['python', 'tts_stt_tts.py'], capture_output=True, text=True)

    if "음성 인식 성공" in result.stdout:  # tts_stt_tts.py가 "음성 인식 성공"을 출력하면
        print("음성이 인식되었습니다. 나머지 스크립트는 실행되지 않습니다.")
    else:
        # 나머지 스크립트 실행
        print("speech_management.py 실행 중...")
        subprocess.run(['python', 'speech_management.py'])

        print("my_speech_recognition.py 실행 중...")
        subprocess.run(['python', 'my_speech_recognition.py'])

        print("emergency_alert.py 실행 중...")
        subprocess.run(['python', 'emergency_alert.py'])

        print("webpage_view.py 실행 중...")
        subprocess.run(['python', 'webpage_view.py'])

        print("모든 스크립트가 성공적으로 실행되었습니다.")

# 스케줄 설정 함수
def setup_schedule(executor):
    # 재생할 파일과 시간 목록 (테스트를 위해 가까운 시간으로 설정)
    schedule_times = [
        ("morning.wav", time.strftime("%H:%M:%S", time.localtime(time.time() + 120))), #("morning.wav", "09:00:00")
        ("lunch.wav", time.strftime("%H:%M:%S", time.localtime(time.time() + 60))), #("lunch.wav", "12:00:00")
        ("dinner.wav", time.strftime("%H:%M:%S", time.localtime(time.time() + 5))) #("dinner.wav", "18:00:00")
    ]


    for file_name, schedule_time in schedule_times:
        schedule.every().day.at(schedule_time).do(executor.submit, play_sound, file_name)
        print(f"{schedule_time}에 {file_name} 음성 파일이 재생되도록 설정되었습니다.")

    # 스케줄을 지속적으로 확인하여 실행
    while True:
        schedule.run_pending()
        time.sleep(1)

# 이 파일이 직접 실행될 때만 스케줄을 설정하고 실행
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        setup_schedule(executor)
