import yfinance as yf

def analyze_sector(sector_tickers=["XLF", "XLK", "XLE"]):
    for ticker in sector_tickers:
        data = yf.download(ticker, period="1mo", auto_adjust=True)
        if not data.empty and "Close" in data.columns:
            first = float(data["Close"].iloc[0])
            last = float(data["Close"].iloc[-1])
            pct = (last - first) / first * 100
            print(f"Sector: {ticker}, Monthly Change: {pct:.2f}%")
        else:
            print(f"⚠️ No data available for {ticker}")

if __name__ == "__main__":
    analyze_sector()
