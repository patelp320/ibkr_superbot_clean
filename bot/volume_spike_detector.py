import yfinance as yf

def detect_volume_spike(ticker="AAPL"):
    data = yf.download(ticker, period="5d", interval="1m")
    avg_volume = data["Volume"].mean()
    spike = data[data["Volume"] > 2 * avg_volume]
    print(f"Volume spikes for {ticker}:")
    print(spike[["Volume"]])

if __name__ == "__main__":
    detect_volume_spike()
