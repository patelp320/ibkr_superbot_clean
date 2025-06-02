from ib_insync import IB, MarketOrder, Stock
from bot.scoring_engine import score_ticker
from bot.config import IB_HOST, IB_PORT
from bot.emailer import send_email
from pathlib import Path
import time

def execute_top_trades():
    ib = IB()
    ib.connect(IB_HOST, IB_PORT, clientId=42)
    tickers = Path("local_cache/tickers_weekly.txt").read_text().splitlines()
    scored = [score_ticker(t) for t in tickers[:100]]
    top = sorted(scored, key=lambda x: x[1], reverse=True)[:5]

    confirmations = []
    for symbol, score in top:
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            ib.qualifyContracts(contract)
            order = MarketOrder('BUY', 10)  # fixed quantity
            trade = ib.placeOrder(contract, order)
            while not trade.isDone():
                ib.sleep(1)
            confirmations.append(f"✅ Bought 10 shares of {symbol} (Score: {score})")
        except Exception as e:
            confirmations.append(f"❌ Failed {symbol}: {e}")

    ib.disconnect()
    result = "\n".join(confirmations)
    Path("logs/trade_exec.log").write_text(result)
    send_email("📈 Superbot Trades Executed", result)

if __name__ == "__main__":
    execute_top_trades()
