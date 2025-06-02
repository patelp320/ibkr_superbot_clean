import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.gurufocus.com/insider/summary"

def fetch_insider_activity():
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(URL, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")[1:6]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 3:
                print(f"🕵️ {cols[0].text.strip()} | {cols[1].text.strip()} | {cols[3].text.strip()}")

if __name__ == "__main__":
    fetch_insider_activity()
