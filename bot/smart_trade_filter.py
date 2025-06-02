import random

def evaluate_trade(probability_threshold=0.75):
    simulated_probability = random.uniform(0, 1)
    if simulated_probability > probability_threshold:
        print(f"✅ Trade Accepted (Simulated Probability: {simulated_probability:.2f})")
    else:
        print(f"❌ Trade Rejected (Simulated Probability: {simulated_probability:.2f})")

if __name__ == "__main__":
    evaluate_trade()
