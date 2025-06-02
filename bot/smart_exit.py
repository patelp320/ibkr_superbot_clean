import pandas as pd, yfinance as yf, ta
from pathlib import Path
from datetime import datetime

WATCHLIST = Path("local_cache/watchlist_reddit.txt")
LOG_PATH = Path("logs/exit_signals.log")

def analyze_exit(symbol):
    df = yf.download(symbol, period="7d", interval="30m")
    if df.empty or "Close" not in df: return None
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["MACD"] = ta.trend.macd_diff(df["Close"])
    rsi = df["RSI"].iloc[-1]
    macd = df["MACD"].iloc[-1]
    if rsi > 70 or macd < 0:
        return f"{symbol} → EXIT: RSI={rsi:.1f}, MACD={macd:.2f}"
    return None

def run_exit_checks():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not WATCHLIST.exists(): return
    symbols = WATCHLIST.read_text().splitlines()
    results = []
    for sym in symbols:
        res = analyze_exit(sym)
        if res: results.append(res)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_PATH.write_text(f"[{timestamp}]\n" + "\n".join(results) + "\n")
    print(f"✅ {len(results)} exit signals written to {LOG_PATH}")

if __name__ == "__main__":
    run_exit_checks()
