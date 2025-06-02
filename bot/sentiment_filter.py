import pandas as pd
from pathlib import Path

CACHE = Path("logs/news_sentiment.csv")

def get_sentiment(symbol):
    try:
        df = pd.read_csv(CACHE)
        row = df[df.symbol == symbol.upper()]
        if not row.empty:
            return float(row.sentiment.values[0])
    except Exception:
        pass
    return 0  # Neutral fallback
