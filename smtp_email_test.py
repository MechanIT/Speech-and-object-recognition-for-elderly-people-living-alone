import smtplib
from email.message import EmailMessage

# STMP 서버의 url과 port 번호
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# SMTP 서버 연결
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

EMAIL_ADDR = 'wltnslagg@sookmyung.ac.kr'
EMAIL_PASSWORD = 'fdtkexjgfususojy' #fdtk exjg fusu sojy #'wlrno4720'

# SMTP 서버에 로그인
smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

# MIME 형태의 이메일 메세지 작성
message = EmailMessage()
message.set_content('hello from local python')
message["Subject"] = "smtp - send an email "
message["From"] = EMAIL_ADDR  #보내는 사람의 이메일 계정
message["To"] = 'wltnslagg@naver.com'

# 서버로 메일 보내기
smtp.send_message(message)

# 메일을 보내면 서버와의 연결 끊기
smtp.quit()
