import smtplib
from email.mime.text import MIMEText

EMAIL ="karthick03kumar082002@gmail.com"
APP_PASSWORD = "cxfg spyh ubkj vnrr"
def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
