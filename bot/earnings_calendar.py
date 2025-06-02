import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://www.earningswhispers.com/calendar"
SAVE_PATH = Path("local_cache/earnings_calendar.txt")

def scrape_earnings():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div[class*='calendar-day']")
    results = []

    for item in items[:5]:
        date = item.select_one(".calendar-date").text.strip()
        tickers = [el.text.strip() for el in item.select(".ticker")]
        results.append(f"{date}: {', '.join(tickers)}")

    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text("\n".join(results))
    print(f"✅ Earnings data saved to {SAVE_PATH}")

if __name__ == "__main__":
    scrape_earnings()
