import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from pathlib import Path

YAHOO_NEWS = "https://finance.yahoo.com/"
SAVE_PATH = Path("local_cache/news_sentiment.txt")

def fetch_news():
    html = requests.get(YAHOO_NEWS, headers={"User-Agent": "Mozilla"}).text
    soup = BeautifulSoup(html, "html.parser")
    return [a.text for a in soup.select("h3") if a.text.strip()]

def analyze_news():
    headlines = fetch_news()
    scored = [(h, round(TextBlob(h).sentiment.polarity, 3)) for h in headlines]
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join([f"{h} | Sentiment: {s}" for h, s in scored]))
    print(f"🗞️ Parsed {len(scored)} signals ➜ {SAVE_PATH}")

if __name__ == "__main__":
    analyze_news()
