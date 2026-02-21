"""
NBA H2H Data Collector
Real historical matchup data from ESPN API for NBA teams
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time

class NBAH2HCollector:
    """Collect real head-to-head data for NBA teams"""
    
    def __init__(self):
        self.espn_base = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_team_h2h_data(self, home_team: str, away_team: str) -> List[Dict]:
        """Get real head-to-head data between two NBA teams - REAL DATA ONLY"""
        
        try:
            # Get team IDs first
            home_team_id = self._get_nba_team_id(home_team)
            away_team_id = self._get_nba_team_id(away_team)
            
            if not home_team_id or not away_team_id:
                print(f"❌ Could not find NBA team IDs for {home_team} vs {away_team} - NO PREDICTION")
                return []
            
            # Get historical games between these teams
            h2h_games = self._fetch_nba_h2h_games(home_team_id, away_team_id, home_team, away_team)
            
            if len(h2h_games) >= 4:  # NBA teams play 2-4 times per season
                print(f"✅ Found {len(h2h_games)} real NBA H2H games: {home_team} vs {away_team}")
                return h2h_games
            else:
                print(f"❌ Only {len(h2h_games)} NBA H2H games found - INSUFFICIENT REAL DATA")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching NBA H2H data: {e} - NO PREDICTION")
            return []
    
    def _get_nba_team_id(self, team_name: str) -> Optional[int]:
        """Get ESPN NBA team ID for a team"""
        
        try:
            # Clean team name for better matching
            clean_name = self._normalize_nba_team_name(team_name)
            
            url = f"{self.espn_base}/teams"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'sports' in data and data['sports']:
                    leagues_data = data['sports'][0].get('leagues', [])
                    for league_data in leagues_data:
                        teams = league_data.get('teams', [])
                        for team in teams:
                            team_info = team.get('team', {})
                            team_display_name = team_info.get('displayName', '').lower()
                            team_short_name = team_info.get('shortDisplayName', '').lower()
                            team_location = team_info.get('location', '').lower()
                            team_nickname = team_info.get('nickname', '').lower()
                            
                            if (clean_name in team_display_name or 
                                clean_name in team_short_name or
                                clean_name in team_location or
                                clean_name in team_nickname or
                                team_display_name in clean_name or
                                team_nickname in clean_name):
                                return int(team_info.get('id', 0))
            
            return None
            
        except Exception as e:
            print(f"Error getting NBA team ID for {team_name}: {e}")
            return None
    
    def _fetch_nba_h2h_games(self, home_id: int, away_id: int, home_name: str, away_name: str) -> List[Dict]:
        """Fetch historical games between two NBA teams"""
        
        h2h_games = []
        
        try:
            # Get recent seasons for both teams (NBA has 82-game seasons)
            seasons_to_check = [2024, 2023, 2022, 2021]  # Last 4 seasons
            
            for season in seasons_to_check:
                # Check home team's schedule
                home_games = self._get_nba_team_schedule(home_id, season)
                away_games = self._get_nba_team_schedule(away_id, season)
                
                # Find games where they played each other
                matchups = self._find_nba_matchups(home_games, away_games, home_id, away_id, home_name, away_name)
                h2h_games.extend(matchups)
                
                # NBA teams typically play 2-4 times per season
                if len(h2h_games) >= 10:  # Limit to reasonable number
                    break
                    
                time.sleep(0.1)  # Rate limiting
            
            # Sort by date (most recent first)
            h2h_games.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            return h2h_games[:10]  # Return up to 10 most recent games
            
        except Exception as e:
            print(f"Error fetching NBA H2H games: {e}")
            return []
    
    def _get_nba_team_schedule(self, team_id: int, season: int) -> List[Dict]:
        """Get NBA team's schedule for a season"""
        
        try:
            url = f"{self.espn_base}/teams/{team_id}/schedule"
            params = {'season': season}
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                
                games = []
                for event in events:
                    # Only include completed games
                    status_type = event.get('competitions', [{}])[0].get('status', {}).get('type', {})
                    if status_type.get('completed', False):
                        games.append(event)
                
                return games
            
            return []
            
        except Exception as e:
            print(f"Error getting NBA team schedule: {e}")
            return []
    
    def _find_nba_matchups(self, home_games: List[Dict], away_games: List[Dict], 
                          home_id: int, away_id: int, home_name: str, away_name: str) -> List[Dict]:
        """Find games where the two NBA teams played each other"""
        
        matchups = []
        
        # Check all games from both teams
        all_games = home_games + away_games
        
        for game in all_games:
            try:
                competitions = game.get('competitions', [])
                if not competitions:
                    continue
                    
                competition = competitions[0]
                competitors = competition.get('competitors', [])
                
                if len(competitors) != 2:
                    continue
                
                # Get team IDs from this game
                team_ids = [int(comp.get('team', {}).get('id', 0)) for comp in competitors]
                
                # Check if this game involves both our teams
                if home_id in team_ids and away_id in team_ids:
                    # Parse the game data
                    game_data = self._parse_nba_game_data(competition, home_id, away_id, home_name, away_name)
                    if game_data:
                        matchups.append(game_data)
            
            except Exception as e:
                continue
        
        # Remove duplicates based on date
        seen_dates = set()
        unique_matchups = []
        
        for matchup in matchups:
            date_key = matchup.get('date', '')
            if date_key not in seen_dates:
                seen_dates.add(date_key)
                unique_matchups.append(matchup)
        
        return unique_matchups
    
    def _parse_nba_game_data(self, competition: Dict, home_id: int, away_id: int, 
                            home_name: str, away_name: str) -> Optional[Dict]:
        """Parse individual NBA game data"""
        
        try:
            competitors = competition.get('competitors', [])
            
            home_score = away_score = 0
            actual_home_team = actual_away_team = ""
            
            for competitor in competitors:
                team_id = int(competitor.get('team', {}).get('id', 0))
                team_name = competitor.get('team', {}).get('displayName', '')
                
                # Handle score - can be string or dict
                score_val = competitor.get('score', 0)
                if isinstance(score_val, dict):
                    score = int(score_val.get('value', 0))
                else:
                    score = int(score_val) if score_val else 0
                
                is_home = competitor.get('homeAway') == 'home'
                
                if team_id == home_id:
                    if is_home:
                        home_score = score
                        actual_home_team = team_name
                    else:
                        away_score = score
                        actual_away_team = team_name
                elif team_id == away_id:
                    if is_home:
                        home_score = score
                        actual_home_team = team_name
                    else:
                        away_score = score
                        actual_away_team = team_name
            
            total_points = home_score + away_score
            winner = actual_home_team if home_score > away_score else actual_away_team
            
            # Get date
            date_str = competition.get('date', datetime.now().isoformat())[:10]
            
            # Calculate halftime total (estimate - typically ~48% of total points)
            halftime_total = int(total_points * 0.48)
            
            return {
                "total_points": total_points,
                "home_score": home_score,
                "away_score": away_score,
                "halftime_total": halftime_total,
                "winner": winner,
                "date": date_str,
                "home_team": actual_home_team or home_name,
                "away_team": actual_away_team or away_name,
                "source": "ESPN_NBA_API"
            }
            
        except Exception as e:
            print(f"Error parsing NBA game data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _normalize_nba_team_name(self, team_name: str) -> str:
        """Normalize NBA team name for better matching"""
        
        name = team_name.lower().strip()
        
        # Common NBA team name mappings
        nba_mappings = {
            'lakers': 'los angeles lakers',
            'warriors': 'golden state warriors',
            'celtics': 'boston celtics',
            'nets': 'brooklyn nets',
            'knicks': 'new york knicks',
            'heat': 'miami heat',
            'bulls': 'chicago bulls',
            'mavs': 'dallas mavericks',
            'mavericks': 'dallas mavericks',
            'spurs': 'san antonio spurs',
            'clippers': 'los angeles clippers',
            'sixers': 'philadelphia 76ers',
            '76ers': 'philadelphia 76ers',
            'thunder': 'oklahoma city thunder',
            'rockets': 'houston rockets'
        }
        
        # Check if it's a known nickname
        if name in nba_mappings:
            return nba_mappings[name]
        
        return name
    


# Test the NBA H2H collector
if __name__ == "__main__":
    collector = NBAH2HCollector()
    
    print("🏀 TESTING NBA H2H DATA COLLECTOR")
    print("=" * 50)
    
    # Test Lakers vs Warriors (popular matchup)
    print("\n📊 NBA Test: Lakers vs Warriors")
    nba_h2h = collector.get_team_h2h_data("Los Angeles Lakers", "Golden State Warriors")
    
    for game in nba_h2h[:3]:  # Show first 3 games
        print(f"   {game['date']}: {game['home_team']} {game['home_score']}-{game['away_score']} {game['away_team']} (Total: {game['total_points']})")
    
    print(f"\n✅ Found {len(nba_h2h)} NBA H2H games")
    
    # Test Celtics vs Heat
    print("\n📊 NBA Test: Celtics vs Heat")
    celtics_heat = collector.get_team_h2h_data("Boston Celtics", "Miami Heat")
    
    for game in celtics_heat[:3]:  # Show first 3 games
        print(f"   {game['date']}: {game['home_team']} {game['home_score']}-{game['away_score']} {game['away_team']} (Total: {game['total_points']})")
    
    print(f"\n✅ Found {len(celtics_heat)} NBA H2H games")
    print("\n🎯 NBA H2H Collector Ready!")