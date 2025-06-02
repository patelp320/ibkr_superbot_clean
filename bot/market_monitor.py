import yfinance as yf
import time

SYMBOLS = ["TSLA", "AAPL", "NVDA", "AMZN"]
LOG = "logs/market_activity.log"

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def scan():
    for symbol in SYMBOLS:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("regularMarketPrice") or info.get("previousClose")
            volume = info.get("volume", 0)
            log(f"{symbol} | Price: {price} | Volume: {volume}")
        except Exception as e:
            log(f"{symbol} scan failed: {e}")

if __name__ == "__main__":
    scan()
