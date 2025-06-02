from bot.penny_scanner import main as run_penny_scanner
from bot.options_wheel import main as run_options_wheel
from bot.reporter import connect, send_email, generate_profit_report
from datetime import datetime
import time
import pandas as pd

while True:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Running IBKR Superbot Cycle")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [PENNY] Starting penny stock scan...")
    run_penny_scanner()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [PENNY] Done.")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [OPTIONS] Starting options wheel strategy...")
    try:
        results = run_options_wheel()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [OPTIONS] Done.")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [REPORT] Generating profit report...")
        results_df = pd.DataFrame(results)
        generate_profit_report(results_df)
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [REPORT] Error generating profit report: {e}")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🕒 Sleeping for 10 minutes...\n")
    time.sleep(600)
