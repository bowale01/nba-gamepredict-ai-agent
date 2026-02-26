"""
Test injury checking functionality
"""

from nba.agentic_ai_enhancer import NBAAugenticAIEnhancer
import os

def test_injury_checking():
    """Test real injury data fetching"""
    
    print("🏥 Testing NBA Injury Checking")
    print("=" * 60)
    
    # Initialize AI enhancer
    api_key = os.getenv('OPENAI_API_KEY')
    enhancer = NBAAugenticAIEnhancer(api_key)
    
    # Test with a few teams
    test_teams = [
        'Los Angeles Lakers',
        'Boston Celtics',
        'Golden State Warriors',
        'Phoenix Suns'
    ]
    
    for team in test_teams:
        print(f"\n🏀 Checking injuries for: {team}")
        print("-" * 60)
        
        injuries = enhancer._fetch_team_injuries(team)
        
        if injuries:
            print(f"✅ Found {len(injuries)} injury reports:")
            for injury in injuries:
                player = injury.get('player', 'Unknown')
                status = injury.get('status', 'Unknown')
                injury_type = injury.get('type', 'Unknown')
                position = injury.get('position', 'N/A')
                
                print(f"   • {player} ({position}) - {status}")
                print(f"     Type: {injury_type}")
        else:
            print(f"   ℹ️ No injuries reported (or API unavailable)")
    
    # Test injury impact calculation
    print("\n" + "=" * 60)
    print("🎯 Testing Injury Impact on Game Prediction")
    print("=" * 60)
    
    sample_game = {
        'home_team': 'Los Angeles Lakers',
        'away_team': 'Boston Celtics',
        'date': '2026-02-21'
    }
    
    injury_analysis = enhancer._assess_nba_injuries(sample_game)
    
    print(f"\n📊 Injury Analysis Results:")
    print(f"   Home Impact Score: {injury_analysis.get('home_impact_score', 0):.2f}")
    print(f"   Away Impact Score: {injury_analysis.get('away_impact_score', 0):.2f}")
    print(f"   Net Advantage: {injury_analysis.get('net_advantage', 'neutral')}")
    print(f"   Confidence Adjustment: {injury_analysis.get('confidence_impact', 0):.2%}")
    print(f"   Total Points Impact: {injury_analysis.get('total_points_impact', 0):.1f}")
    
    if injury_analysis.get('key_players_out'):
        print(f"\n⚠️ Key Players Out:")
        for player in injury_analysis['key_players_out']:
            print(f"   • {player['name']} ({player['position']}) - {player['status']}")
            print(f"     Impact Score: {player['impact']:.2f}")
    
    print(f"\n📝 Summary: {injury_analysis.get('injury_summary', 'No summary')}")
    
    # Test current form analysis
    print("\n" + "=" * 60)
    print("📈 Testing Current Form Analysis")
    print("=" * 60)
    
    form_analysis = enhancer._analyze_recent_performance(sample_game)
    
    print(f"\n🏠 {sample_game['home_team']} Form:")
    home_form = form_analysis.get('home_team_form', {})
    if isinstance(home_form, dict):
        print(f"   Record (Last 10): {home_form.get('wins', 0)}-{home_form.get('losses', 0)}")
        print(f"   Last 5 Games: {form_analysis.get('home_last_5', 'N/A')}")
        print(f"   Current Streak: {form_analysis.get('home_streak', 'N/A')}")
        print(f"   Avg Points Scored: {home_form.get('avg_points_scored', 0):.1f}")
        print(f"   Avg Points Allowed: {home_form.get('avg_points_allowed', 0):.1f}")
        print(f"   Point Differential: {home_form.get('point_differential', 0):+.1f}")
        print(f"   Form Score: {form_analysis.get('home_form_score', 0):.2f}/10")
    
    print(f"\n✈️ {sample_game['away_team']} Form:")
    away_form = form_analysis.get('away_team_form', {})
    if isinstance(away_form, dict):
        print(f"   Record (Last 10): {away_form.get('wins', 0)}-{away_form.get('losses', 0)}")
        print(f"   Last 5 Games: {form_analysis.get('away_last_5', 'N/A')}")
        print(f"   Current Streak: {form_analysis.get('away_streak', 'N/A')}")
        print(f"   Avg Points Scored: {away_form.get('avg_points_scored', 0):.1f}")
        print(f"   Avg Points Allowed: {away_form.get('avg_points_allowed', 0):.1f}")
        print(f"   Point Differential: {away_form.get('point_differential', 0):+.1f}")
        print(f"   Form Score: {form_analysis.get('away_form_score', 0):.2f}/10")
    
    print(f"\n⚖️ Form Comparison:")
    print(f"   Momentum Advantage: {form_analysis.get('momentum_advantage', 'neutral')}")
    print(f"   Confidence Adjustment: {form_analysis.get('confidence_adjustment', 0):+.2%}")
    print(f"\n📝 Form Summary:")
    print(f"   {form_analysis.get('form_summary', 'No summary')}")
    
    print("\n" + "=" * 60)
    print("✅ Injury and form checking tests complete!")

if __name__ == "__main__":
    test_injury_checking()
