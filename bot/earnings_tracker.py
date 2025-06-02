import yfinance as yf
from datetime import datetime

def fetch_earnings(ticker="AAPL"):
    stock = yf.Ticker(ticker)
    earnings = stock.calendar
    print(f"Earnings calendar for {ticker}:")
    print(earnings)

if __name__ == "__main__":
    fetch_earnings()
