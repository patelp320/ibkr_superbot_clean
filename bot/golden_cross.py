import yfinance as yf
from pathlib import Path

TICKERS = ["AAPL", "TSLA", "AMD", "NVDA", "META"]
SAVE_PATH = Path("local_cache/golden_cross.txt")

def golden_cross():
    results = []
    for ticker in TICKERS:
        df = yf.download(ticker, period="1y")
        df["MA50"] = df["Close"].rolling(window=50).mean()
        df["MA200"] = df["Close"].rolling(window=200).mean()

        if df["MA50"].iloc[-2] < df["MA200"].iloc[-2] and df["MA50"].iloc[-1] > df["MA200"].iloc[-1]:
            results.append(f"🟢 Golden Cross detected: {ticker}")

    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(results))
    print(f"✅ Golden Cross results saved to {SAVE_PATH}")

if __name__ == "__main__":
    golden_cross()
