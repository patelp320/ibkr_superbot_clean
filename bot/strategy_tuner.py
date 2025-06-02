import json
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("logs/strategy_tuning.log")
TRADE_LOG = Path("logs/trade_logs.json")

def tune_strategy():
    if not TRADE_LOG.exists():
        print("❌ No trade logs to tune strategy.")
        return

    trades = json.loads(TRADE_LOG.read_text()).get("trades", [])
    if not trades:
        print("⚠️ No recent trades found.")
        return

    avg_pnl = sum(t["pnl"] for t in trades) / len(trades)
    new_risk_level = "high" if avg_pnl > 50 else "low"
    
    # Simulate tuning (write to log)
    with LOG_PATH.open("a") as log:
        log.write(f"[{datetime.now()}] Adjusted strategy to risk level: {new_risk_level} (Avg PnL = {avg_pnl:.2f})\n")

    print(f"🔧 Strategy tuned: risk level set to {new_risk_level}")

if __name__ == "__main__":
    tune_strategy()
