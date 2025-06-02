import re, requests, feedparser
from bs4 import BeautifulSoup
from pathlib import Path

YAHOO_URL = "https://finance.yahoo.com/trending-tickers"
FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_price_u10,sh_avgvol_o1000"
REDDIT_RSS = "https://www.reddit.com/r/pennystocks/.rss"
SAVE_PATH = Path("local_cache/tickers_weekly.txt")

def clean_symbols(text):
    return re.findall(r'\b[A-Z]{2,6}\b', text)

def yahoo():
    html = requests.get(YAHOO_URL, headers={"User-Agent": "Mozilla"}).text
    return clean_symbols(html)

def finviz():
    html = requests.get(FINVIZ_URL, headers={"User-Agent": "Mozilla"}).text
    soup = BeautifulSoup(html, "html.parser")
    return [a.text for a in soup.select("a.screener-link") if re.fullmatch(r"[A-Z]{2,6}", a.text)]

def reddit():
    feed = feedparser.parse(REDDIT_RSS)
    titles = " ".join(entry.title for entry in feed.entries)
    return clean_symbols(titles)

def aggregate():
    tickers = set(yahoo() + finviz() + reddit())
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(sorted(tickers)))
    print(f"✅ Ticker list ({len(tickers)} symbols) saved to {SAVE_PATH}")

if __name__ == "__main__":
    aggregate()



def expand_watchlist():
    print('⚠️ expand_watchlist() is not yet implemented.')

