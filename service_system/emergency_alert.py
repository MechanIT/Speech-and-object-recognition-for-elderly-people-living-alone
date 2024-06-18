import smtplib
from email.message import EmailMessage

# STMP 서버의 url과 port 번호
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# 이메일 계정 정보
EMAIL_ADDR = 'im3zero@sookmyung.ac.kr'  # 발신자 이메일 주소
EMAIL_PASSWORD = 'iihc nqvn oava pryw'  # 생성된 앱 비밀번호

def send_alert():
    print("비상 상황! 긴급 연락을 취합니다.")
    
    try:
        # 1. SMTP 서버 연결
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            # 2. SMTP 서버에 로그인
            smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)
            
            # 3. MIME 형태의 이메일 메세지 작성
            message = EmailMessage()
            message.set_content('비상 상황이 발생했습니다. 즉시 조치를 취하십시오. http://192.168.0.19:5000')
            message["Subject"] = "SOS : 사용자에게 비상 상황이 발생하였습니다"  # 메일 제목
            message["From"] = EMAIL_ADDR  # 발신자 이메일 주소
            message["To"] = 'tpdud0815@naver.com'  # 수신자 이메일 주소
            
            # 4. 서버로 메일 보내기
            smtp.send_message(message)
            print("이메일을 성공적으로 보냈습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {e}")

# 테스트 실행
send_alert()
