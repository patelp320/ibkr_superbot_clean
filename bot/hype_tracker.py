import feedparser, re
from textblob import TextBlob
from pathlib import Path
from datetime import datetime

RSS_FEEDS = [
    "https://www.reddit.com/r/stocks/.rss",
    "https://www.reddit.com/r/wallstreetbets/.rss"
]
SAVE_PATH = Path("local_cache/hype_sentiment.txt")

def extract_tickers(text):
    return re.findall(r'\b[A-Z]{2,6}\b', text)

def score_sentiment(text):
    return TextBlob(text).sentiment.polarity

def scrape():
    tickers = {}
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            symbols = extract_tickers(entry.title + entry.description)
            score = score_sentiment(entry.title + entry.description)
            for sym in symbols:
                tickers[sym] = tickers.get(sym, 0) + score
    return sorted(tickers.items(), key=lambda x: x[1], reverse=True)

def save():
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    scored = scrape()
    lines = [f"{sym}: {score:.2f}" for sym, score in scored]
    SAVE_PATH.write_text("\n".join(lines))
    print(f"✅ Hype scores for {len(scored)} tickers saved to {SAVE_PATH}")

if __name__ == "__main__":
    save()
