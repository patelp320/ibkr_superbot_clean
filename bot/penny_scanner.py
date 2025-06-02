# from bot.emailer import send_penny_report
import requests, re
from bot.sentiment_filter import get_sentiment
from bs4 import BeautifulSoup
from pathlib import Path
# from .emailer import send_penny_report

YAHOO_URL = "https://finance.yahoo.com/trending-tickers"
FINVIZ_URL = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_price_u10,sh_avgvol_o1000"
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

def aggregate():
    tickers = set(yahoo() + finviz())

    tickers = [t for t in tickers if get_sentiment(t) > -0.2]
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(sorted(tickers)))
    print(f"✅ Ticker list ({len(tickers)} symbols) saved to {SAVE_PATH}")

if __name__ == "__main__":
    aggregate()
    send_penny_report()

# ✅ Added by setup script to enable core.py entry
def main():
    print("Running penny scanner main()")
    aggregate()
