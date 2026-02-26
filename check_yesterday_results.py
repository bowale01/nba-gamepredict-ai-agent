# -*- coding: utf-8 -*-
"""
Check yesterday's NBA game results
"""

import requests
from datetime import datetime, timedelta

def check_yesterday():
    """Check yesterday's completed games"""
    
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y%m%d')
    
    print("=" * 80)
    print(f"🏀 NBA RESULTS - {yesterday.strftime('%B %d, %Y')}")
    print("=" * 80)
    print()
    
    url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={date_str}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'events' in data:
                completed = 0
                
                for event in data['events']:
                    competition = event.get('competitions', [{}])[0]
                    status = competition.get('status', {})
                    
                    competitors = competition.get('competitors', [])
                    
                    if len(competitors) == 2:
                        home_team = next((c for c in competitors if c.get('homeAway') == 'home'), None)
                        away_team = next((c for c in competitors if c.get('homeAway') == 'away'), None)
                        
                        if home_team and away_team:
                            home_name = home_team.get('team', {}).get('displayName', 'Unknown')
                            away_name = away_team.get('team', {}).get('displayName', 'Unknown')
                            home_score = home_team.get('score', 'N/A')
                            away_score = away_team.get('score', 'N/A')
                            
                            is_completed = status.get('type', {}).get('completed', False)
                            status_text = status.get('type', {}).get('description', 'Unknown')
                            
                            if is_completed:
                                completed += 1
                                total = int(home_score) + int(away_score) if home_score != 'N/A' else 'N/A'
                                winner = home_name if int(home_score) > int(away_score) else away_name
                                
                                # Check for overtime
                                periods = competition.get('status', {}).get('period', 4)
                                overtime_text = ""
                                if periods > 4:
                                    ot_count = periods - 4
                                    overtime_text = f" (OT)" if ot_count == 1 else f" ({ot_count}OT)"
                                
                                print(f"✅ {home_name} {home_score} - {away_score} {away_name}{overtime_text}")
                                print(f"   Winner: {winner}{overtime_text}")
                                print(f"   Total Points: {total}")
                                if overtime_text:
                                    print(f"   ⚠️  Game went to overtime - Moneyline bets include OT")
                                print()
                            else:
                                print(f"⏳ {away_name} @ {home_name}")
                                print(f"   Status: {status_text}")
                                if home_score != 'N/A':
                                    print(f"   Score: {away_name} {away_score} - {home_score} {home_name}")
                                print()
                
                print("=" * 80)
                print(f"Completed Games: {completed}")
                print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_yesterday()
