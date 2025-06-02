from bot.emailer import send_email, build_options_text
from datetime import datetime

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    subject = f"📊 IBKR Superbot Daily Report - {now}"
    body = "💵 Today's Summary:\n\n- Penny stock scans complete.\n- Option wheel strategy ran.\n"
    body += "\n📌 Weekly High-Yield Option Picks:\n"
    body += build_options_text()

    send_email(subject, body)


def report_profits():
    from bot.emailer import send_email, build_options_text
    subject = '📈 Profit Report'
    body = build_options_text()
    send_email(subject, body)
