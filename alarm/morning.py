from gtts import gTTS

text = "안녕하세요, 좋은 아침입니다."

tts = gTTS(text=text, lang='ko')

output_path = "output1.wav"

tts.save(output_path)

print(f"음성 파일이 '{output_path}'로 저장되었습니다.")


#실행하기위해 해야하는 것
#1. pip install gtts
#2. 실행 !!!!!!