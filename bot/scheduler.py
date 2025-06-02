import schedule, time
from datetime import datetime
from bot.penny_scanner import aggregate
from bot.options_wheel import run_wheel_strategy
from bot.emailer import send_email
from bot.profit_reporter import report_profits
from bot.feed_scraper import expand_watchlist
from bot.news_sentiment import analyze_news
from bot.market_gap_tracker import detect_gaps
from bot.sector_strength import analyze_sector

def run_scans():
    print(f"✅ Running scans from scheduler... ({datetime.now()})")
    aggregate()
    expand_watchlist()
    analyze_news()

def run_trading_logic():
    run_wheel_strategy()
    detect_gaps()
    analyze_sector()

def weekly_report():
    report_profits()
    send_email("📊 Weekly Trading Summary", "Report attached.")

# Run scans every day including weekends
schedule.every().day.at("08:00").do(run_scans)       # Morning pre-market scans
schedule.every().day.at("12:00").do(run_scans)       # Midday refresh
schedule.every().day.at("16:00").do(run_scans)       # After close scan

# Run trading logic weekdays only
schedule.every().monday.at("09:30").do(run_trading_logic)
schedule.every().tuesday.at("09:30").do(run_trading_logic)
schedule.every().wednesday.at("09:30").do(run_trading_logic)
schedule.every().thursday.at("09:30").do(run_trading_logic)
schedule.every().friday.at("09:30").do(run_trading_logic)

# Weekly summary email every Friday at 6 PM EST
schedule.every().friday.at("18:00").do(weekly_report)

while True:
    schedule.run_pending()
    time.sleep(30)

# New Scheduled Jobs
import bot.penny_ranker as penny_ranker
import bot.trade_logger as trade_logger

def run_additional_jobs():
    print("📊 Running penny ranker...")
    penny_ranker.rank_tickers()
    print("📝 Trade logger module loaded (manual trigger only).")

schedule.every().day.at("07:15").do(run_additional_jobs)

import subprocess
schedule.every().day.at('08:45').do(lambda: subprocess.run(['python3', '-m', 'bot.rsi_signal']))
schedule.every().monday.at('09:00').do(lambda: subprocess.run(['python3', '-m', 'bot.earnings_calendar']))


schedule.every().day.at('10:00').do(lambda: subprocess.run(['python3', '-m', 'bot.golden_cross']))
schedule.every().day.at('10:15').do(lambda: subprocess.run(['python3', '-m', 'bot.volume_surge']))

