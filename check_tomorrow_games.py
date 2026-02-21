"""Quick test: Check NBA games available for tomorrow"""
from datetime import datetime, timedelta
import requests

tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
print(f"Checking NBA games for TOMORROW: {tomorrow}")
print("=" * 60)

# NBA
nba_url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={tomorrow}"
resp = requests.get(nba_url)
nba_games = resp.json().get("events", [])
print(f"\nNBA: {len(nba_games)} games")
for game in nba_games:
    comp = game.get('competitions', [{}])[0]
    competitors = comp.get('competitors', [])
    if len(competitors) >= 2:
        away = competitors[0].get('team', {}).get('displayName', 'Away')
        home = competitors[1].get('team', {}).get('displayName', 'Home')
        print(f"  - {away} @ {home}")

print("\n" + "=" * 60)
print("SUMMARY: Your agent automatically fetches NBA games for whatever date")
print("you specify. Just change the date parameter in the API call!")
