import yfinance as yf
import pandas as pd
from pathlib import Path
import datetime

PRED_PATH = Path("logs/predictions_daily.txt")
LOG_PATH = Path("logs/trade_log.csv")
TODAY = datetime.date.today()
YESTERDAY = TODAY - datetime.timedelta(days=1)

def load_predictions():
    if not PRED_PATH.exists(): return []
    return [line.split("→")[0].strip() for line in PRED_PATH.read_text().splitlines()]

def simulate():
    trades = []
    for ticker in load_predictions():
        try:
            df = yf.download(ticker, start=str(YESTERDAY), end=str(TODAY + datetime.timedelta(days=1)), progress=False)
            if len(df) < 2: continue
            buy = df["Open"].iloc[0]
            sell = df["Close"].iloc[-1]
            profit = (sell - buy) / buy * 1000  # ,000 per trade
            trades.append({"ticker": ticker, "buy": round(buy, 2), "sell": round(sell, 2), "profit": round(profit, 2)})
        except: continue
    df_log = pd.DataFrame(trades)
    if df_log.empty:
        print("⚠️ No trades simulated.")
        return
    df_log.to_csv(LOG_PATH, index=False)
    print(f"✅ {len(df_log)} simulated trades saved to {LOG_PATH}")

if __name__ == "__main__":
    simulate()
