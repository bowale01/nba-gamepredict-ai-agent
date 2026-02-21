"""
Test NBA Player Props Feature
Testing the fastest growing NBA betting market
"""
from nba.predictor import ReliableNBAPredictor

print("🌟 TESTING NBA PLAYER PROPS FEATURE")
print("=" * 70)
print("Testing fastest growing NBA betting market")
print("Focus: LeBron, Curry, Jokic, and other stars")
print()

# Initialize predictor with Player Props enabled
predictor = ReliableNBAPredictor(enable_agentic_ai=False, enable_player_props=True)

# Test with Lakers vs Warriors (star-studded game)
test_game = {
    'id': 'test123',
    'home_team': 'Los Angeles Lakers',
    'away_team': 'Golden State Warriors',
    'home_team_id': 13,  # Lakers team ID
    'away_team_id': 9,   # Warriors team ID
    'home_abbreviation': 'LAL',
    'away_abbreviation': 'GSW',
    'venue': 'Crypto.com Arena',
    'status': 'Scheduled',
    'datetime': '2025-12-30T20:00:00Z'
}

print(f"\n🏀 Test Game: {test_game['away_team']} @ {test_game['home_team']}")
print("🌟 Expected Stars: LeBron James, Anthony Davis, Stephen Curry, Draymond Green")
print("=" * 70)

try:
    # Test player props analyzer directly
    if predictor.player_props_enabled and predictor.player_props_analyzer:
        print("\n📊 Fetching player props...")
        
        player_props = predictor.player_props_analyzer.get_star_players_props(
            test_game['home_team'],
            test_game['away_team'],
            test_game['home_team_id'],
            test_game['away_team_id']
        )
        
        print("\n" + "=" * 70)
        print("✅ PLAYER PROPS ANALYSIS RESULTS")
        print("=" * 70)
        
        if player_props:
            for props in player_props:
                predictor.player_props_analyzer.display_player_props(props)
                print()
        else:
            print("⚠️ No player props generated")
        
        print("=" * 70)
        print("✅ Player Props Feature Test Complete!")
        print()
        print("📊 Available Prop Types:")
        print("   • Points (Over/Under)")
        print("   • Rebounds (Over/Under)")
        print("   • Assists (Over/Under)")
        print("   • 3-Pointers Made (Over/Under)")
        print("   • PRA - Points + Rebounds + Assists (MOST POPULAR)")
        print()
        print("🔥 This is the FASTEST GROWING NBA betting market!")
        print("🔥 Especially popular on mobile betting apps")
        print("🔥 Bettors love betting on their favorite stars")
    else:
        print("❌ Player Props not enabled or not available")
        
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()
