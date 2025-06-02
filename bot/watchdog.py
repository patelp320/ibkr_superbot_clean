import os
import time
import subprocess
from datetime import datetime

LOG_FILE = "/app/logs/bot.log"
MAX_MINUTES_IDLE = 15
CHECK_INTERVAL_SECONDS = 300  # every 5 minutes

def get_last_log_time():
    if not os.path.exists(LOG_FILE):
        return None
    t = os.path.getmtime(LOG_FILE)
    return datetime.fromtimestamp(t)

def restart_container():
    print("❗ Bot log inactive — restarting container...")
    subprocess.run(["/usr/bin/docker", "restart", "ibkr_superbot_clean-trader-1"])

while True:
    try:
        now = datetime.now()
        last_log_time = get_last_log_time()

        if not last_log_time:
            print("⚠️ No log file found. Skipping check...")
        else:
            idle_minutes = (now - last_log_time).total_seconds() / 60
            print(f"🕵️ Last log update: {last_log_time} ({idle_minutes:.1f} minutes ago)")
            if idle_minutes > MAX_MINUTES_IDLE:
                restart_container()
        
    except Exception as e:
        print("❌ Watchdog error:", e)

    time.sleep(CHECK_INTERVAL_SECONDS)
