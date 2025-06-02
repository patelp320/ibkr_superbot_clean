import yfinance as yf
import datetime

def fetch_weekly_options(ticker):
    stock = yf.Ticker(ticker)
    today = datetime.date.today()
    expirations = stock.options
    if not expirations:
        return []

    # Find the closest Friday
    friday = today + datetime.timedelta((4 - today.weekday()) % 7)
    friday_str = friday.strftime('%Y-%m-%d')
    if friday_str not in expirations:
        return []

    try:
        chain = stock.option_chain(friday_str)
        return chain.calls
    except Exception as e:
        print(f"❌ Failed for {ticker}: {e}")
        return []

def rank_options(tickers):
    results = []
    for t in tickers:
        calls = fetch_weekly_options(t)
        if calls is not None and not calls.empty:
            df = calls[(calls["volume"] > 50) & (calls["openInterest"] > 100)]
            df.loc[:, "yield"] = df["lastPrice"] / df["strike"]
            top = df.sort_values(by="yield", ascending=False).head(3)
            results.append((t, top[["strike", "lastPrice", "volume", "openInterest", "yield"]]))
    return results

if __name__ == "__main__":
    tickers = ["AAPL", "AMD", "TSLA", "SPY", "NVDA"]
    ranked = rank_options(tickers)
    for t, df in ranked:
        print(f"\n📈 {t} Options:\n", df.to_string(index=False))
