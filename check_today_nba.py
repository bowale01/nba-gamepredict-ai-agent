"""
Check today's NBA games and their H2H data quality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from nba.nba_h2h_collector import NBAH2HCollector
from nba.predictor import ReliableNBAPredictor

def check_today_nba():
    print("=" * 80)
    print(f"🏀 CHECKING TODAY'S NBA GAMES - {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 80)
    
    predictor = ReliableNBAPredictor(enable_agentic_ai=True)
    collector = NBAH2HCollector()
    
    # Get today's games
    games = predictor.get_todays_nba_games()
    
    if not games:
        print("\n❌ No NBA games found for today")
        return
    
    print(f"\n✅ Found {len(games)} NBA games today\n")
    
    real_h2h_count = 0
    fallback_count = 0
    
    for i, game in enumerate(games, 1):
        home_team = game.get("home_team", "Unknown")
        away_team = game.get("away_team", "Unknown")
        
        print(f"\n{'='*80}")
        print(f"Game {i}: {away_team} @ {home_team}")
        print(f"{'='*80}")
        
        # Get H2H data
        h2h_matches = collector.get_team_h2h_data(home_team, away_team)
        
        if h2h_matches:
            num_matches = len(h2h_matches)
            
            # Check if it's real data or fallback
            first_match = h2h_matches[0] if h2h_matches else {}
            is_fallback = first_match.get("data_source") == "fallback"
            
            if is_fallback:
                print(f"⚠️  FALLBACK DATA (Simulated): {num_matches} matches")
                fallback_count += 1
            else:
                print(f"✅ REAL ESPN DATA: {num_matches} matches")
                real_h2h_count += 1
            
            # Show sample matches
            print(f"\n📊 Sample H2H Matches:")
            for match in h2h_matches[:3]:
                date = match.get("date", "Unknown")
                home = match.get("home_team", "Unknown")
                away = match.get("away_team", "Unknown")
                home_score = match.get("home_score", 0)
                away_score = match.get("away_score", 0)
                print(f"   {date}: {away} {away_score} @ {home} {home_score}")
        else:
            print(f"❌ No H2H data available")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"Total Games: {len(games)}")
    print(f"✅ Real ESPN H2H Data: {real_h2h_count}")
    print(f"⚠️  Fallback (Simulated) Data: {fallback_count}")
    print(f"❌ No Data: {len(games) - real_h2h_count - fallback_count}")
    
    if real_h2h_count > 0:
        print(f"\n✅ SUCCESS: Found {real_h2h_count} games with REAL ESPN H2H data")
    else:
        print(f"\n❌ WARNING: All games using fallback or no H2H data")

if __name__ == "__main__":
    check_today_nba()
