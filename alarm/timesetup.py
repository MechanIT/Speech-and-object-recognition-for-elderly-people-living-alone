import schedule
import time
from playsound import playsound

# 음성 파일 재생 함수
def play_sound():
    playsound('output1.wav')
    print("음성 파일이 재생되었습니다.")

schedule_time = "12:45"
schedule.every().day.at(schedule_time).do(play_sound)

print(f"{schedule_time}에 음성 파일이 재생되도록 설정되었습니다.")

# 스케줄을 지속적으로 확인
while True:
    schedule.run_pending()
    time.sleep(1)
