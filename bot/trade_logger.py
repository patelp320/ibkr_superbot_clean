import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/trades.json")

def log_trade(ticker, action, price, quantity):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    trade = {
        "timestamp": datetime.utcnow().isoformat(),
        "ticker": ticker,
        "action": action,
        "price": price,
        "quantity": quantity
    }
    trades = []
    if LOG_PATH.exists():
        trades = json.loads(LOG_PATH.read_text())
    trades.append(trade)
    LOG_PATH.write_text(json.dumps(trades, indent=2))
