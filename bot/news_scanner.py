import feedparser, requests, re
from textblob import TextBlob
from pathlib import Path
import pandas as pd

YAHOO = "https://finance.yahoo.com/rss/topstories"
REDDIT = "https://www.reddit.com/r/pennystocks/.rss"
CACHE = Path("logs/news_sentiment.csv")

def clean(t): return re.findall(r'\b[A-Z]{2,6}\b', t.upper())

def score(text): return TextBlob(text).sentiment.polarity

def fetch_feed(url):
    items = []
    feed = feedparser.parse(url)
    for e in feed.entries:
        symbols = clean(e.title + " " + e.get("summary", ""))
        sentiment = score(e.title + " " + e.get("summary", ""))
        for s in symbols:
            items.append({"symbol": s, "headline": e.title, "sentiment": sentiment})
    return items

def run():
    print("📰 Fetching news...")
    items = fetch_feed(YAHOO) + fetch_feed(REDDIT)
    df = pd.DataFrame(items)
    if not df.empty:
        df = df.groupby("symbol").agg({"sentiment": "mean"}).reset_index()
        df.to_csv(CACHE, index=False)
        print(f"✅ News sentiment cached → {CACHE}")
    else:
        print("⚠️ No news articles found.")

if __name__ == "__main__":
    run()
