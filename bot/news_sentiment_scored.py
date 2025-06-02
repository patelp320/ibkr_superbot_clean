import feedparser, re, json
from datetime import datetime
from pathlib import Path

URLS = [
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL,TSLA,NVDA,AMD&region=US&lang=en-US",
    "https://www.marketwatch.com/rss/topstories"
]

KEYWORDS = {
    "bullish": ["beats", "growth", "surge", "record", "soars", "rally"],
    "bearish": ["misses", "loss", "drop", "decline", "cuts", "fall", "plunge"]
}

def score_sentiment(title):
    text = title.lower()
    pos = sum(kw in text for kw in KEYWORDS["bullish"])
    neg = sum(kw in text for kw in KEYWORDS["bearish"])
    return "bullish" if pos > neg else "bearish" if neg > pos else "neutral"

results = []
for url in URLS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        results.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", str(datetime.now())),
            "sentiment": score_sentiment(entry.title)
        })

out_path = Path("local_cache/news_sentiment_scored.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(results, indent=2))

print(f"✅ News sentiment scored ({len(results)} entries) ➜ {out_path}")
