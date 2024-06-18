import smtplib
from email.message import EmailMessage

# STMP 서버의 url과 port 번호
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# 이메일 계정 정보
EMAIL_ADDR = 'wltnslagg@sookmyung.ac.kr' # 사용자의 최측근 혹은 지자체 행정안전 관련 부서
EMAIL_PASSWORD = 'fdtkexjgfususojy'

def send_alert():
    print("비상 상황! 긴급 연락을 취합니다.")
    
    # 1. SMTP 서버 연결
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        # 2. SMTP 서버에 로그인
        smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)
        
        # 3. MIME 형태의 이메일 메세지 작성
        message = EmailMessage()
        message.set_content('비상 상황이 발생했습니다. 즉시 조치를 취하십시오.')
        message["Subject"] = "SOS : 사용자에게 비상 상황이 발생하였습니다" # 보내지는 메일 제목
        message["From"] = EMAIL_ADDR  # 보내는 사람의 이메일 계정
        message["To"] = 'wltnslagg@naver.com'  # 받는 사람의 이메일 계정
        
        # 4. 서버로 메일 보내기
        smtp.send_message(message)
        print("이메일을 성공적으로 보냈습니다.")
