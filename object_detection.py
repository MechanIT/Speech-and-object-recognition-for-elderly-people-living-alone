import subprocess

def run_detection():
    command = [
        'python', 'detect.py',
        '--weights', 'best_final.pt',
        '--conf', '0.25',
        '--img-size', '640',
        '--source', '0'  # 카메라 소스
    ]
    
    # 지정된 인수와 함께 detect.py 호출
    subprocess.run(command)

if __name__ == "__main__":
    run_detection()