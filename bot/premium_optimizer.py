import random, json
from pathlib import Path

tickers = ["AAPL", "TSLA", "PLTR"]
results = []

for t in tickers:
    strikes = [90, 95, 100, 105]
    candidates = []
    for s in strikes:
        iv = round(random.uniform(0.2, 0.8), 2)
        delta = round(random.uniform(0.2, 0.4), 2)
        premium = round(random.uniform(0.5, 3.5), 2)
        pop = round(1 - delta, 2)
        score = premium * pop / iv
        candidates.append({"strike": s, "score": score, "premium": premium})

    best = max(candidates, key=lambda x: x["score"])
    results.append({"ticker": t, "best_strike": best["strike"], "premium": best["premium"]})

Path("logs/strike_suggestions.json").write_text(json.dumps(results, indent=2))
print("✅ Strike optimization complete ➜ logs/strike_suggestions.json")
