import subprocess

def main():
    try:
        # sound_generation 실행
        print("sound_generation.py 실행 중...")
        subprocess.run(['python', 'sound_generation.py'])

        # timesetup 실행
        print("timesetup.py 실행 중...")
        subprocess.run(['python', 'timesetup.py'])
        

        print("모든 스크립트가 성공적으로 실행되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
