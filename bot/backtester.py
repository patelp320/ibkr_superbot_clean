import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

TICKERS = Path("local_cache/tickers_weekly.txt")
RESULTS = Path("logs/backtest_results.csv")

def run():
    if not TICKERS.exists():
        print("❌ No tickers found to backtest.")
        return

    symbols = TICKERS.read_text().splitlines()
    results = []

    for symbol in symbols[:100]:  # Test top 100 first for speed
        try:
            data = yf.download(symbol, period="90d", interval="1d")
            if len(data) < 30:
                continue
            daily_returns = data["Close"].pct_change().dropna()
            win_rate = (daily_returns > 0.01).mean()
            avg_gain = daily_returns[daily_returns > 0.01].mean()
            results.append({
                "symbol": symbol,
                "win_rate": round(win_rate, 3),
                "avg_gain": round(avg_gain, 4),
            })
        except Exception as e:
            print(f"⚠️ {symbol} failed: {e}")

    df = pd.DataFrame(results)
    df = df.sort_values("win_rate", ascending=False)
    df.to_csv(RESULTS, index=False)
    print(f"✅ Backtest complete — saved to {RESULTS}")
