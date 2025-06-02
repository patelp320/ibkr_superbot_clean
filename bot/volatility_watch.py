import yfinance as yf
from pathlib import Path
from datetime import datetime

WATCHLIST = Path("local_cache/watchlist_reddit.txt")
LOG_PATH = Path("logs/volatility_alerts.log")

def check_volatility(symbol):
    df = yf.download(symbol, period="1d", interval="5m")
    if df.empty or len(df) < 6: return None
    pct_change = ((df["Close"].iloc[-1] - df["Close"].iloc[-6]) / df["Close"].iloc[-6]) * 100
    if abs(pct_change) > 3:
        return f"{symbol} → Volatility Spike: {pct_change:.2f}% in last 30m"
    return None

def scan():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not WATCHLIST.exists(): return
    symbols = WATCHLIST.read_text().splitlines()
    results = [check_volatility(sym) for sym in symbols]
    results = [r for r in results if r]
    LOG_PATH.write_text("\n".join(results))
    print(f"✅ Volatility alerts: {len(results)} tickers flagged")

if __name__ == "__main__":
    scan()
