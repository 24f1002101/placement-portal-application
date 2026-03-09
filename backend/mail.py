import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # ✅ add this

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_EMAIL = 'po_rgukt@gmail.com'

def send_email(to_email, subject, body):
    msg = MIMEMultipart('alternative')   # ✅ changed
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    html_part = MIMEText(body, 'html')   # ✅ tell it body is HTML
    msg.attach(html_part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")