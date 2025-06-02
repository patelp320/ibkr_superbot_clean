import pandas as pd

def find_best_trades():
    # Dummy trade logic for testing
    data = {
        "ticker": ["AAPL", "MSFT", "TSLA"],
        "strike": [180, 310, 180],
        "lastPrice": [3.5, 4.2, 6.1],
        "expDate": ["2025-06-14", "2025-06-14", "2025-06-14"]
    }
    df = pd.DataFrame(data)
    df.loc[:, "yield"] = df["lastPrice"] / df["strike"]
    return df

def rank_options(df):
    # Dummy ranker: sort by yield descending
    df = df.copy()
    df["score"] = df["yield"]
    return df.sort_values(by="score", ascending=False)
