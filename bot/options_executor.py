from ib_insync import IB, Option, util
from datetime import date, timedelta
from bot.config import IB_HOST, IB_PORT
from bot.emailer import send_email

def get_targets():
    try:
        return open("local_cache/options_targets.txt").read().splitlines()
    except:
        return []

def place_put(contract_symbol, strike, expiry, premium):
    ib = IB()
    ib.connect(IB_HOST, IB_PORT, clientId=44)
    option = Option(symbol=contract_symbol, lastTradeDateOrContractMonth=expiry, strike=strike, right='P', exchange='SMART')
    ib.qualifyContracts(option)
    order = ib.limitOrder('SELL', 1, premium)
    ib.placeOrder(option, order)
    ib.disconnect()
    return f"Sold 1 PUT on {contract_symbol} ${strike} exp {expiry} @ ${premium}"

def run():
    targets = get_targets()
    results = []
    for line in targets:
        try:
            sym, strike, expiry, premium = line.split(',')
            results.append(place_put(sym.strip(), float(strike), expiry.strip(), float(premium)))
        except Exception as e:
            results.append(f"⚠️ Failed: {line} -> {e}")
    if results:
        send_email("📊 Options Trades Executed", "\n".join(results))

if __name__ == "__main__":
    run()
