import yfinance as yf
from datetime import datetime
from bot.emailer import send_email

WATCHLIST = ["TSLA", "AAPL", "NVDA", "AMZN"]
THRESHOLD = 1.5  # 1.5x average volume

def check_unusual_activity():
    msg_lines = []
    for symbol in WATCHLIST:
        try:
            data = yf.Ticker(symbol).history(period="7d", interval="1d")
            if len(data) < 2:
                continue
            avg_vol = data["Volume"][:-1].mean()
            latest_vol = data["Volume"][-1]
            if latest_vol > THRESHOLD * avg_vol:
                msg_lines.append(f"{symbol}: Volume spike! {latest_vol:,} vs avg {int(avg_vol):,}")
        except Exception as e:
            msg_lines.append(f"{symbol}: Error - {e}")
    if msg_lines:
        send_email("📈 Anomaly Alert: Unusual Activity Detected", "\n".join(msg_lines))

if __name__ == "__main__":
    check_unusual_activity()
