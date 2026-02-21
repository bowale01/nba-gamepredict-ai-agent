"""
NBA Betting Odds API Integration
Fetches real NBA betting lines from sportsbooks for accurate predictions
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class NBABettingOddsAPI:
    """Integration with sports betting APIs to get real NBA odds"""
    
    def __init__(self):
        # The Odds API - Free tier: 500 requests/month
        self.odds_api_key = "YOUR_ODDS_API_KEY"  # User needs to get free key
        self.odds_base_url = "https://api.the-odds-api.com/v4/sports"
        
        # Backup: ESPN API for basic odds data
        self.espn_base_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
        
    def get_nba_betting_lines(self, date: str = None) -> List[Dict]:
        """Get NBA betting lines for specific date"""
        
        if not date:
            date = datetime.now().strftime('%Y%m%d')
            
        try:
            # Try The Odds API first (most accurate)
            odds_data = self._get_odds_api_data('basketball_nba', date)
            if odds_data:
                return self._parse_odds_api_response(odds_data)
                
            # Fallback to ESPN odds data
            print("⚠️  Using ESPN fallback for NBA betting lines")
            return self._get_espn_odds_fallback(date)
            
        except Exception as e:
            print(f"❌ Error fetching NBA betting lines: {e}")
            print(f"⚠️ REAL ODDS UNAVAILABLE - Predictions will use estimated lines")
            print(f"💡 Get free API key at https://the-odds-api.com (500 requests/month)")
            return []  # Return empty - NO MOCK DATA
    
    def _get_odds_api_data(self, sport: str, date: str) -> Optional[Dict]:
        """Fetch data from The Odds API"""
        
        # Check if API key is configured
        if self.odds_api_key == "YOUR_ODDS_API_KEY":
            return None
            
        url = f"{self.odds_base_url}/{sport}/odds"
        params = {
            'apiKey': self.odds_api_key,
            'regions': 'us',
            'markets': 'h2h,totals',  # Moneylines and Over/Under
            'oddsFormat': 'american',
            'dateFormat': 'iso'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️  NBA Odds API error: {e}")
            return None
    
    def _parse_odds_api_response(self, odds_data: List[Dict]) -> List[Dict]:
        """Parse The Odds API response into our format"""
        
        parsed_lines = []
        
        for game in odds_data:
            if not game.get('bookmakers'):
                continue
                
            # Get DraftKings or FanDuel odds (most reliable)
            bookmaker = None
            for bm in game['bookmakers']:
                if bm['key'] in ['draftkings', 'fanduel', 'betmgm']:
                    bookmaker = bm
                    break
            
            if not bookmaker:
                continue
                
            game_data = {
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'commence_time': game['commence_time'],
                'moneylines': {},
                'totals': {}
            }
            
            # Parse markets
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':  # Moneylines
                    for outcome in market['outcomes']:
                        team_name = outcome['name']
                        game_data['moneylines'][team_name] = outcome['price']
                        
                elif market['key'] == 'totals':  # Over/Under
                    for outcome in market['outcomes']:
                        if outcome['name'] == 'Over':
                            game_data['totals']['over'] = {
                                'line': outcome['point'],
                                'odds': outcome['price']
                            }
                        elif outcome['name'] == 'Under':
                            game_data['totals']['under'] = {
                                'line': outcome['point'],
                                'odds': outcome['price']
                            }
            
            parsed_lines.append(game_data)
        
        return parsed_lines
    
    def _get_espn_odds_fallback(self, date: str) -> List[Dict]:
        """Fallback to ESPN for basic NBA odds data"""
        
        try:
            url = f"{self.espn_base_url}/scoreboard"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            games_with_odds = []
            
            for event in data.get('events', []):
                if not event.get('competitions'):
                    continue
                    
                competition = event['competitions'][0]
                competitors = competition.get('competitors', [])
                
                if len(competitors) != 2:
                    continue
                    
                home_team = next((c['team']['displayName'] for c in competitors if c.get('homeAway') == 'home'), '')
                away_team = next((c['team']['displayName'] for c in competitors if c.get('homeAway') == 'away'), '')
                
                # ESPN sometimes has odds data
                odds_data = competition.get('odds', [])
                if odds_data:
                    odds = odds_data[0]
                    game_odds = {
                        'home_team': home_team,
                        'away_team': away_team,
                        'commence_time': event.get('date'),
                        'moneylines': {},
                        'totals': {}
                    }
                    
                    # Parse ESPN odds format
                    if 'overUnder' in odds:
                        game_odds['totals']['over'] = {
                            'line': odds['overUnder'],
                            'odds': -110  # Standard
                        }
                        game_odds['totals']['under'] = {
                            'line': odds['overUnder'],
                            'odds': -110  # Standard
                        }
                    
                    games_with_odds.append(game_odds)
            
            return games_with_odds
            
        except Exception as e:
            print(f"⚠️  ESPN NBA fallback error: {e}")
            return []
    
    def find_game_odds(self, home_team: str, away_team: str, all_odds: List[Dict]) -> Optional[Dict]:
        """Find betting odds for specific NBA game"""
        
        # Normalize team names for matching
        home_normalized = self._normalize_nba_team_name(home_team)
        away_normalized = self._normalize_nba_team_name(away_team)
        
        for game in all_odds:
            game_home = self._normalize_nba_team_name(game['home_team'])
            game_away = self._normalize_nba_team_name(game['away_team'])
            
            if (home_normalized in game_home or game_home in home_normalized) and \
               (away_normalized in game_away or game_away in away_normalized):
                return game
        
        return None
    
    def _normalize_nba_team_name(self, team_name: str) -> str:
        """Normalize NBA team names for matching"""
        
        # Remove common suffixes and normalize
        name = team_name.lower()
        
        # Handle common NBA team name variations
        name_mappings = {
            'lakers': 'los angeles lakers',
            'warriors': 'golden state warriors',
            'clippers': 'la clippers',
            'heat': 'miami heat',
            'celtics': 'boston celtics',
            'nets': 'brooklyn nets',
            'bulls': 'chicago bulls',
            'mavs': 'dallas mavericks',
            'mavericks': 'dallas mavericks'
        }
        
        for short_name, full_name in name_mappings.items():
            if short_name in name:
                return full_name
        
        return name

# Example usage
if __name__ == "__main__":
    api = NBABettingOddsAPI()
    
    print("🏀 Testing NBA Betting Odds API Integration")
    print("=" * 50)
    
    # Test NBA odds
    print("\n📊 NBA Betting Lines:")
    nba_odds = api.get_nba_betting_lines()
    
    for game in nba_odds[:3]:  # Show first 3 games
        print(f"\n🏀 {game['away_team']} @ {game['home_team']}")
        
        if game['totals']:
            total_line = game['totals']['over']['line']
            print(f"   💰 OVER/UNDER: {total_line} points")
        
        if game['moneylines']:
            print(f"   💰 MONEYLINES: Available")
    
    print("\n✅ NBA Integration ready - Get free API key for real odds!")
    print("📝 Visit: https://the-odds-api.com")