import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import yfinance as yf

LOG_PATH = Path("logs/trade_log.csv")
LEARN_PATH = Path("logs/learning_summary.csv")

def evaluate():
    if not LOG_PATH.exists():
        print("❌ No trade logs to learn from.")
        return

    df = pd.read_csv(LOG_PATH)
    df["date"] = pd.to_datetime(df["date"])
    recent = df[df["date"] >= datetime.now() - timedelta(days=3)]

    if recent.empty:
        print("📭 No recent trades to evaluate.")
        return

    feedback = []
    for _, row in recent.iterrows():
        ticker = row["ticker"]
        entry_price = row["entry"]
        signal_type = row["type"]

        data = yf.download(ticker, period="2d", interval="1d")
        if data.empty or "Close" not in data:
            continue

        recent_close = data["Close"].iloc[-1]
        profit = recent_close - entry_price if signal_type == "call" else entry_price - recent_close
        score = 1 if profit > 0 else -1

        feedback.append({
            "ticker": ticker,
            "type": signal_type,
            "entry": entry_price,
            "close": recent_close,
            "profit": profit,
            "score": score
        })

    if feedback:
        df_feedback = pd.DataFrame(feedback)
        df_feedback.to_csv(LEARN_PATH, index=False)
        print(f"✅ Learning summary saved to {LEARN_PATH}")
    else:
        print("📭 No useful feedback today.")
