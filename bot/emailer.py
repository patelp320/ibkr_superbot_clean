import smtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "patelp320@gmail.com"
SMTP_PASS = "jvwvjyqqiuwqcvxn"
EMAIL_TO  = "patelp320@gmail.com"

server = None

def connect():
    global server
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        print("📡 Connected to Gmail SMTP server.")
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")

def send_email(report_path="profit_report.txt"):
    try:
        with open(report_path, "r") as f:
            content = f.read()

        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = "📈 IBKR Superbot Report"
        msg["From"] = SMTP_USER
        msg["To"] = EMAIL_TO

        server.send_message(msg)
        print(f"📤 Email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
