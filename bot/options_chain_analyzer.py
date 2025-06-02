import yfinance as yf

def analyze_chain(ticker="AAPL"):
    stock = yf.Ticker(ticker)
    options = stock.options
    print(f"Options chain for {ticker}: {options}")

if __name__ == "__main__":
    analyze_chain()
