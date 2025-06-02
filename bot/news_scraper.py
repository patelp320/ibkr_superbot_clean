import feedparser, re
from datetime import datetime
from pathlib import Path

FEEDS = [
    "https://finance.yahoo.com/news/rssindex",
    "https://www.marketwatch.com/rss/topstories",
    "https://www.reddit.com/r/stocks/.rss"
]

OUTPUT = Path("local_cache/news_sentiment.txt")

def extract_tickers(text):
    return re.findall(r'\b[A-Z]{2,5}\b', text)

def analyze_sentiment(title):
    bearish = ["drop", "fall", "down", "cut", "loss", "bearish", "sell"]
    bullish = ["rise", "gain", "up", "soar", "surge", "bullish", "buy"]
    title_lower = title.lower()
    if any(word in title_lower for word in bullish):
        return "bullish"
    if any(word in title_lower for word in bearish):
        return "bearish"
    return "neutral"

def run():
    results = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:
            title = entry.title
            sentiment = analyze_sentiment(title)
            tickers = extract_tickers(title)
            for t in tickers:
                results.append(f"{t},{sentiment},{title}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(results))
    print(f"🗞️ Parsed {len(results)} signals ➜ {OUTPUT}")

if __name__ == "__main__":
    run()
