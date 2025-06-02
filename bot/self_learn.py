import json
from pathlib import Path

TRADE_LOG = Path("logs/trade_logs.json")

def evaluate_trades():
    if not TRADE_LOG.exists():
        print("❌ No trade logs found.")
        return

    with open(TRADE_LOG) as f:
        data = json.load(f)

    trades = data.get("trades", [])
    total_pnl = sum(t["pnl"] for t in trades)
    winners = [t for t in trades if t["pnl"] > 0]
    losers = [t for t in trades if t["pnl"] <= 0]

    print(f"🧠 Adaptive logic updated from {len(trades)} trades.")
    print(f"✅ Win rate: {len(winners)}/{len(trades)} | Total PnL: $")

if __name__ == "__main__":
    evaluate_trades()
