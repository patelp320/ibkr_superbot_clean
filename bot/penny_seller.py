from ib_insync import IB, Stock
from pathlib import Path
from bot.config import IB_HOST, IB_PORT
from bot.emailer import send_email

def sell_open_positions():
    ib = IB()
    ib.connect(IB_HOST, IB_PORT, clientId=43)
    positions = ib.positions()
    closed = []

    for pos in positions:
        symbol = pos.contract.symbol
        quantity = pos.position
        if quantity <= 0: continue  # skip shorts or empty

        market_price = ib.reqMktData(pos.contract, '', False, False).last
        avg_cost = pos.avgCost
        pnl_percent = ((market_price - avg_cost) / avg_cost) * 100

        if pnl_percent > 6 or pnl_percent < -3:  # take profit or stop loss
            order = ib.marketOrder('SELL', quantity)
            ib.placeOrder(pos.contract, order)
            closed.append(f"{symbol} - Sold {quantity} shares at {market_price:.2f} (PnL: {pnl_percent:.2f}%)")

    ib.disconnect()
    if closed:
        Path("logs/penny_sells.log").write_text("\n".join(closed))
        send_email("💰 Penny Sell Report", "\n".join(closed))

if __name__ == "__main__":
    sell_open_positions()
