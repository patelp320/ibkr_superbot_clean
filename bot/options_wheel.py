from bot.options_finder import find_best_trades

def main():
    print("📈 Running real options strategy...")
    try:
        results = find_best_trades()
        print("✅ Top trade candidates:")
        print(results.head())
    except Exception as e:
        print(f"❌ Options strategy error: {e}")
