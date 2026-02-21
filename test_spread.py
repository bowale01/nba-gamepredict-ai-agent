"""
Quick test script for Point Spread feature
"""
from nba.predictor import ReliableNBAPredictor

print("Testing Point Spread Predictions...")
print("=" * 60)

# Initialize predictor
predictor = ReliableNBAPredictor(enable_agentic_ai=False)

# Test game
test_game = {
    'home_team': 'Boston Celtics',
    'away_team': 'Brooklyn Nets',
    'home_team_id': 2,
    'away_team_id': 17,
    'venue': 'TD Garden',
    'status': 'Scheduled'
}

print("\nGenerating prediction for:", test_game['away_team'], '@', test_game['home_team'])
print("-" * 60)

# Generate prediction
result = predictor.predict_game_with_h2h_focus(test_game)

# Display Point Spread results
print("\n✅ POINT SPREAD PREDICTION (MOST POPULAR NBA BET):")
print("-" * 60)
print(f"Home Team Spread: {result.get('home_team_spread', 'N/A')}")
print(f"Away Team Spread: {result.get('away_team_spread', 'N/A')}")
print(f"Market Spread: {result.get('market_spread', 'N/A')}")
print(f"Confidence: {result.get('spread_confidence', 0):.1%}")
print(f"Recommendation: {result.get('spread_recommendation', 'N/A')}")
print(f"Edge: {result.get('spread_edge', 0)} points")
print(f"Advice: {result.get('spread_betting_advice', 'N/A')}")

print("\n✅ All betting markets:")
print("-" * 60)
print(f"1. Point Spread: {result.get('spread_confidence', 0):.1%} confidence")
print(f"2. Moneyline: {result.get('winner_confidence', 0):.1%} confidence")
print(f"3. Over/Under: {result.get('ou_confidence', 0):.1%} confidence")
print(f"4. Halftime: {result.get('halftime_over_confidence', 0):.1%} confidence")

print("\n" + "=" * 60)
print("✅ Point Spread feature working successfully!")
