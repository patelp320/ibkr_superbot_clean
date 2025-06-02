import pandas as pd, yfinance as yf
from pathlib import Path
from bot.emailer import send_email

def score_ticker(ticker):
    try:
        data = yf.Ticker(ticker).history(period="10d", interval="1d")
        if data.empty or len(data) < 5:
            return (ticker, 0)
        momentum = (data["Close"][-1] - data["Close"][-5]) / data["Close"][-5]
        avg_vol = data["Volume"].mean()
        latest_vol = data["Volume"].iloc[-1]
        volume_ratio = latest_vol / avg_vol if avg_vol else 0
        score = (momentum * 100) + (volume_ratio * 10)
        return (ticker, round(score, 2))
    except:
        return (ticker, 0)

def run_scoring():
    tickers = Path("local_cache/tickers_weekly.txt").read_text().splitlines()
    scored = [score_ticker(t) for t in tickers[:100]]  # Limit for performance
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:10]
    Path("logs/top_scores.txt").write_text("\n".join(f"{s[0]}: {s[1]}" for s in top))
    send_email("📊 Penny Stock Score Report", "\n".join(f"{s[0]}: {s[1]}" for s in top))

if __name__ == "__main__":
    run_scoring()
