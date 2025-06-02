from datetime import datetime, timedelta
from pathlib import Path
from bot.emailer import send_email

LOG_DIR = Path("logs")
OUT_FILE = LOG_DIR / "weekly_summary.txt"

def summarize():
    end = datetime.today()
    start = end - timedelta(days=7)
    lines = []

    for log_file in LOG_DIR.glob("*.log"):
        lines.append(f"\n📁 {log_file.name}")
        with open(log_file) as f:
            for line in f:
                try:
                    timestamp = datetime.strptime(line[1:20], "%Y-%m-%d %H:%M:%S")
                    if start <= timestamp <= end:
                        lines.append(line.strip())
                except:
                    continue

    summary = "\n".join(lines) or "No log entries found this week."
    OUT_FILE.write_text(summary)
    send_email("🗂 Weekly Superbot Summary", summary)

if __name__ == "__main__":
    summarize()
