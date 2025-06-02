import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import datetime

TICKER_PATH = Path("local_cache/tickers_weekly.txt")
SAVE_PATH = Path("logs/predictions_daily.txt")

def get_features(df):
    df["return"] = df["Close"].pct_change()
    df["volatility"] = df["Close"].pct_change().rolling(5).std()
    df["momentum"] = df["Close"].rolling(5).mean() - df["Close"].rolling(20).mean()
    df["target"] = np.where(df["Close"].shift(-1) > df["Close"], 1, 0)
    return df[["return", "volatility", "momentum", "target"]].dropna()

def predict_ticker(ticker):
    try:
        df = yf.download(ticker, period="90d", progress=False)
        if len(df) < 30: return None
        data = get_features(df)
        if len(data) < 10: return None
        model = RandomForestClassifier(n_estimators=25)
        model.fit(data[["return", "volatility", "momentum"]][:-1], data["target"][:-1])
        prob = model.predict_proba([data[["return", "volatility", "momentum"]].iloc[-1]])[0][1]
        return (ticker, round(prob, 2))
    except: return None

def run():
    tickers = TICKER_PATH.read_text().splitlines() if TICKER_PATH.exists() else []
    results = []
    for t in tickers[:500]:
        r = predict_ticker(t)
        if r and r[1] > 0.6:
            results.append(r)
    results = sorted(results, key=lambda x: x[1], reverse=True)
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join([f"{t[0]} → {t[1]*100:.1f}% chance up tomorrow" for t in results]))
    print(f"✅ ML predictions saved → {SAVE_PATH}")

if __name__ == "__main__":
    run()
