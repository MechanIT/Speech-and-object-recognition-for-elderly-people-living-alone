from gtts import gTTS

text = "점심은 맛있게 드셨나요? 남은 시간도 행복하세요."

tts = gTTS(text=text, lang='ko')

output_path = "output2.wav"

tts.save(output_path)

print(f"음성 파일이 '{output_path}'로 저장되었습니다.")


#실행하기위해 해야하는 것
#1. pip install gtts
#2. 실행 !!!!!!