import pandas as pd

def connect():
    print("📧 Dummy connect() executed")

def send_email(report_path="profit_report.txt"):
    print(f"📤 Dummy email sent with: {report_path}")

def generate_profit_report(results=None):
    print("📊 Generating profit report...")
    try:
        if results is None:
            print("⚠️ No results provided. Skipping report.")
            return

        # Convert list of dicts to DataFrame if needed
        if isinstance(results, list):
            if len(results) == 0:
                print("⚠️ Empty results list.")
                return
            elif isinstance(results[0], dict):
                results = pd.DataFrame(results)
            else:
                print("❌ Invalid data structure.")
                return

        lines = [
            "Ticker | Strike | Premium | Exp Date   | Yield",
            "------------------------------------------------"
        ]

        for _, row in results.iterrows():
            lines.append(f"{row['ticker']:6} | {row['strike']:6} | {row['lastPrice']:7} | {row['expDate']} | {row['yield']:.2%}")

        with open("profit_report.txt", "w") as f:
            f.write("\n".join(lines))

        print("📄 profit_report.txt saved.")
    except Exception as e:
        print(f"❌ Error writing profit report: {e}")
