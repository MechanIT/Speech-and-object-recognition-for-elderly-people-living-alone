import pyaudio
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import time
import os

# 모델과 프로세서 로드
model_name = "kresnik/wav2vec2-large-xlsr-korean"
local_model_dir = "./models"

if not os.path.exists(local_model_dir):
    os.makedirs(local_model_dir)

model_path = os.path.join(local_model_dir, model_name.replace("/", "_") + ".safetensors")
processor_path = os.path.join(local_model_dir, model_name.replace("/", "_") + "_processor")

if not os.path.exists(model_path):
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    model.save_pretrained(local_model_dir)
else:
    model = Wav2Vec2ForCTC.from_pretrained(local_model_dir)

if not os.path.exists(processor_path):
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    processor.save_pretrained(local_model_dir)
else:
    processor = Wav2Vec2Processor.from_pretrained(local_model_dir)

# PyAudio 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 10  # 10초 동안 녹음

# 전체 오디오 데이터를 저장할 리스트
audio_frames = []

def recognize_audio(model, processor, audio_data):
    inputs = processor(audio_data, sampling_rate=RATE, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription

def callback(in_data, frame_count, time_info, status):
    audio_frames.append(np.frombuffer(in_data, dtype=np.int16))
    return (in_data, pyaudio.paContinue)

if __name__ == "__main__":
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    print("녹음중...")
    stream.start_stream()

    # 10초 동안 녹음
    time.sleep(RECORD_SECONDS)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # 전체 오디오 데이터를 하나의 배열로 결합
    audio_data = np.hstack(audio_frames)
    audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize to [-1, 1]

    # 음성 인식 및 결과 출력
    transcription = recognize_audio(model, processor, audio_data)
    print("텍스트로 출력:", transcription)
    print("텍스트 출력이 끝났습니다.")
