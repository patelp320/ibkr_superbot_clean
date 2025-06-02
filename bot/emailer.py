import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_TO
from .options_finder import rank_options

def build_options_text():
    tickers = ["AAPL", "TSLA", "NVDA", "AMD", "SPY"]
    ranked = rank_options(tickers)
    text = ""
    for symbol, df in ranked:
        text += f"\n📈 {symbol} Weekly Options:\n"
        text += df.to_string(index=False)
        text += "\n"
    return text

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def send_penny_report():
    with open("local_cache/tickers_weekly.txt") as f:
        tickers = f.read()
    send_email("📈 Weekly Penny Stock Report", tickers)
