import schedule
import time
from playsound import playsound

# 음성 파일 재생 함수
def play_sound(file_name):
    playsound(file_name)
    print(f"{file_name} 음성 파일이 재생되었습니다.")

# 스케줄 설정 함수
def setup_schedule():
    # 재생할 파일과 시간 목록
    schedule_times = [
        ("morning.wav", "09:00"),
        ("lunch.wav", "12:45"),
        ("dinner.wav", "18:30")
    ]

    for file_name, schedule_time in schedule_times:
        schedule.every().day.at(schedule_time).do(play_sound, file_name)
        print(f"{schedule_time}에 {file_name} 음성 파일이 재생되도록 설정되었습니다.")

    # 스케줄을 지속적으로 확인하여 실행
    while True:
        schedule.run_pending()
        time.sleep(1)

# 이 파일이 직접 실행될 때만 스케줄을 설정하고 실행
if __name__ == "__main__":
    setup_schedule()
