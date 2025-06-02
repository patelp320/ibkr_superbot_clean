import yfinance as yf
import datetime
from pathlib import Path

TICKER_PATH = Path("local_cache/tickers_weekly.txt")
RANKED_PATH = Path("local_cache/top_ranked.txt")
END = datetime.date.today()
START = END - datetime.timedelta(days=90)

def get_tickers():
    return TICKER_PATH.read_text().splitlines() if TICKER_PATH.exists() else []

def score_ticker(ticker):
    try:
        df = yf.download(ticker, start=str(START), end=str(END), progress=False)
        if df.empty or len(df) < 30: return None
        change = (df["Close"][-1] - df["Close"][0]) / df["Close"][0]
        volatility = df["Close"].pct_change().std()
        momentum = df["Close"].rolling(5).mean().iloc[-1] - df["Close"].rolling(20).mean().iloc[-1]
        score = (change * 100) + (momentum * 10) - (volatility * 50)
        return (ticker, round(score, 2))
    except: return None

def run():
    results = []
    for t in get_tickers()[:1000]:
        r = score_ticker(t)
        if r: results.append(r)
    ranked = sorted(results, key=lambda x: x[1], reverse=True)[:25]
    RANKED_PATH.parent.mkdir(parents=True, exist_ok=True)
    RANKED_PATH.write_text("\n".join([f"{t[0]} → Score: {t[1]}" for t in ranked]))
    print(f"✅ Ranked top {len(ranked)} stocks → saved to {RANKED_PATH}")

if __name__ == "__main__":
    run()
