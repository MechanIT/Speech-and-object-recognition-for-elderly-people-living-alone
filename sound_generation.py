from gtts import gTTS

text = "안녕하세요, 좋은 아침입니다."

tts = gTTS(text=text, lang='ko')

output_path = "morning.wav"

tts.save(output_path)

print(f"음성 파일이 '{output_path}'로 저장되었습니다.")


text = "점심은 맛있게 드셨나요? 남은 시간도 행복하세요."

tts = gTTS(text=text, lang='ko')

output_path = "lunch.wav"

tts.save(output_path)

print(f"음성 파일이 '{output_path}'로 저장되었습니다.")

text = "저녁은 맛있게 드셨나요? 평안한 저녁시간 되세요."

tts = gTTS(text=text, lang='ko')

output_path = "dinner.wav"

tts.save(output_path)

print(f"음성 파일이 '{output_path}'로 저장되었습니다.")