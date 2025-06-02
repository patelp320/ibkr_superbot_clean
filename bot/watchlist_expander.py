import requests, re, feedparser
from pathlib import Path

REDDIT_RSS = "https://www.reddit.com/r/pennystocks/.rss"
SAVE_PATH = Path("local_cache/watchlist_reddit.txt")

def clean_symbols(text):
    return re.findall(r'\b[A-Z]{2,6}\b', text)

def expand_watchlist():
    feed = feedparser.parse(REDDIT_RSS)
    tickers = set()
    for entry in feed.entries:
        tickers.update(clean_symbols(entry.title + " " + entry.get("summary", "")))
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(sorted(tickers)))
    print(f"✅ Watchlist ({len(tickers)} symbols) saved to {SAVE_PATH}")

if __name__ == "__main__":
    expand_watchlist()
