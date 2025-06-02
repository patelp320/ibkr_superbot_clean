import yfinance as yf
from pathlib import Path
import pandas as pd

TICKERS = ["AAPL", "TSLA", "AMD", "NVDA", "META"]
SAVE_PATH = Path("local_cache/rsi_signals.txt")

def calculate_rsi(data, period=14):
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def scan_rsi():
    alerts = []
    for ticker in TICKERS:
        df = yf.download(ticker, period="1mo", interval="1d")
        df["RSI"] = calculate_rsi(df)
        rsi = df["RSI"].iloc[-1]
        if rsi < 30:
            alerts.append(f"🔻 Oversold: {ticker} RSI={rsi:.2f}")
        elif rsi > 70:
            alerts.append(f"🔺 Overbought: {ticker} RSI={rsi:.2f}")
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(alerts))
    print(f"✅ RSI signals written to {SAVE_PATH}")

if __name__ == "__main__":
    scan_rsi()
