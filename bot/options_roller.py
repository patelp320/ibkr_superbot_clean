from ib_insync import IB, Option, util
from datetime import date, timedelta
from bot.config import IB_HOST, IB_PORT
from bot.emailer import send_email

def get_open_positions():
    try:
        return open("local_cache/open_options.txt").read().splitlines()
    except:
        return []

def roll_put(symbol, strike, expiry, new_expiry, premium):
    ib = IB()
    ib.connect(IB_HOST, IB_PORT, clientId=45)
    old_option = Option(symbol=symbol, lastTradeDateOrContractMonth=expiry, strike=strike, right='P', exchange='SMART')
    ib.qualifyContracts(old_option)
    ib.closePosition(old_option)

    new_option = Option(symbol=symbol, lastTradeDateOrContractMonth=new_expiry, strike=strike, right='P', exchange='SMART')
    ib.qualifyContracts(new_option)
    order = ib.limitOrder('SELL', 1, premium)
    ib.placeOrder(new_option, order)
    ib.disconnect()
    return f"Rolled PUT {symbol} ${strike} from {expiry} ➜ {new_expiry} @ ${premium}"

def run():
    entries = get_open_positions()
    logs = []
    for line in entries:
        try:
            sym, strike, expiry, new_expiry, premium = line.split(',')
            logs.append(roll_put(sym.strip(), float(strike), expiry.strip(), new_expiry.strip(), float(premium)))
        except Exception as e:
            logs.append(f"⚠️ Roll failed: {line} -> {e}")
    if logs:
        send_email("🔁 Rolled Options Summary", "\n".join(logs))

if __name__ == "__main__":
    run()
