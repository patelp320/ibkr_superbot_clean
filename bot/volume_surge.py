import yfinance as yf
from pathlib import Path

TICKERS = ["AAPL", "TSLA", "AMD", "NVDA", "META"]
SAVE_PATH = Path("local_cache/volume_surge.txt")

def detect_surges():
    alerts = []
    for ticker in TICKERS:
        df = yf.download(ticker, period="2w")
        avg_vol = df["Volume"].rolling(window=10).mean()
        if df["Volume"].iloc[-1] > avg_vol.iloc[-1] * 1.5:
            alerts.append(f"📈 {ticker}: Volume Surge ({df['Volume'].iloc[-1]})")

    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(alerts))
    print(f"✅ Volume Surge results saved to {SAVE_PATH}")

if __name__ == "__main__":
    detect_surges()
