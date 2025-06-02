import time
import traceback
from datetime import datetime

from bot.penny_scanner import main as run_penny_scanner
from bot.options_wheel import main as run_options_wheel
from bot.trade_logger import log_trade
# Optional: from emailer import send_report

SLEEP_MINUTES = 10

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {msg}")
    with open("logs/bot.log", "a") as f:
        f.write(f"{timestamp} {msg}\\n")

while True:
    try:
        log("✅ Running IBKR Superbot Cycle")

        log("[PENNY] Starting penny stock scan...")
        run_penny_scanner()
        log("[PENNY] Done.")

        log("[OPTIONS] Starting options wheel strategy...")
        run_options_wheel()
        log("[OPTIONS] Done.")

        # log_trade() or send_report() here if you want periodic reports
        from bot.profit_reporter import report_profits

        log("[REPORT] Generating profit report...")

        try:

            report_profits()

            log("[REPORT] Profit report complete.")

        except Exception as e:

            log(f"[REPORT] Error generating profit report: {e}")
    except Exception as e:
        err_msg = "".join(traceback.format_exception(None, e, e.__traceback__))
        log("❌ ERROR in strategy loop:\\n" + err_msg)
        # Optional: send_report(subject="Bot Error", body=err_msg)

    log(f"🕒 Sleeping for {SLEEP_MINUTES} minutes...\\n")
    time.sleep(SLEEP_MINUTES * 60)
