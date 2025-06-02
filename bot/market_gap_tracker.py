import yfinance as yf
from datetime import datetime, timedelta

SYMBOLS = ["AAPL", "TSLA", "MSFT", "AMZN"]
GAP_THRESHOLD = 0.03  # 3%

def detect_gaps():
    today = datetime.now().date()
    for symbol in SYMBOLS:
        data = yf.download(symbol, period="5d", interval="1d")
        if len(data) >= 2:
            prev_close = data['Close'].iloc[-2]
            today_open = data['Open'].iloc[-1]
            gap = abs(today_open - prev_close) / prev_close
            if gap.item() >= GAP_THRESHOLD:
                direction = "up" if today_open > prev_close else "down"
                print(f"📈 Gap on {symbol}: {gap*100:.2f}% {direction.upper()}")

if __name__ == "__main__":
    detect_gaps()
