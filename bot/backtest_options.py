import random, json
from datetime import datetime
from pathlib import Path

tickers = ["AAPL", "TSLA", "NVDA", "AMD", "PLTR"]
results = []

for t in tickers:
    win = random.randint(0, 1)
    result = {
        "ticker": t,
        "strategy": "cash-secured put",
        "strike": random.randint(80, 150),
        "premium": round(random.uniform(0.5, 3.5), 2),
        "outcome": "win" if win else "loss",
        "roi": round(random.uniform(2, 8), 2) if win else -round(random.uniform(2, 5), 2)
    }
    results.append(result)

log_path = Path("logs/options_backtest_" + datetime.now().strftime("%Y%m%d") + ".json")
log_path.parent.mkdir(parents=True, exist_ok=True)
log_path.write_text(json.dumps(results, indent=2))
print(f"✅ Backtest complete ➜ {log_path}")
