"""
NBA Player Props Analyzer
Fastest growing NBA betting market - especially popular on mobile apps
Analyzes: Points, Rebounds, Assists, 3-Pointers, PRA (combined)
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import statistics

class NBAPlayerPropsAnalyzer:
    """Analyzes individual player performance for prop betting predictions"""
    
    def __init__(self):
        """Initialize player props analyzer with ESPN API"""
        self.espn_base = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba"
        self.star_players = {
            # Lakers
            "Lakers": ["LeBron James", "Anthony Davis"],
            # Warriors
            "Warriors": ["Stephen Curry", "Draymond Green"],
            # Nuggets
            "Nuggets": ["Nikola Jokic", "Jamal Murray"],
            # Celtics
            "Celtics": ["Jayson Tatum", "Jaylen Brown"],
            # Bucks
            "Bucks": ["Giannis Antetokounmpo", "Damian Lillard"],
            # Mavericks
            "Mavericks": ["Luka Doncic", "Kyrie Irving"],
            # Suns
            "Suns": ["Kevin Durant", "Devin Booker"],
            # 76ers
            "76ers": ["Joel Embiid", "Tyrese Maxey"],
            # Knicks
            "Knicks": ["Jalen Brunson", "Julius Randle"],
            # Heat
            "Heat": ["Jimmy Butler", "Bam Adebayo"],
        }
        print("🌟 NBA Player Props Analyzer initialized")
        print("🎯 Focus: Points, Rebounds, Assists, 3PT, PRA")
    
    def get_team_roster(self, team_id: int) -> List[Dict]:
        """Fetch team roster from ESPN API"""
        try:
            url = f"{self.espn_base}/teams/{team_id}/roster"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                players = []
                
                if 'athletes' in data:
                    for athlete in data['athletes']:
                        if 'items' in athlete:
                            for player in athlete['items']:
                                player_info = {
                                    "id": player.get('id'),
                                    "name": player.get('displayName', 'Unknown'),
                                    "position": player.get('position', {}).get('abbreviation', 'N/A'),
                                    "jersey": player.get('jersey', 'N/A')
                                }
                                players.append(player_info)
                
                return players
            else:
                print(f"⚠️ Could not fetch roster for team {team_id}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching roster: {e}")
            return []
    
    def get_player_season_stats(self, player_id: str) -> Optional[Dict]:
        """Get player's season statistics from ESPN"""
        try:
            url = f"{self.espn_base}/athletes/{player_id}/statistics"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract current season stats
                if 'statistics' in data and data['statistics']:
                    for stat_category in data['statistics']:
                        if stat_category.get('type') == 'total' or 'season' in stat_category.get('name', '').lower():
                            stats = stat_category.get('stats', {})
                            
                            return {
                                "points_per_game": stats.get('avgPoints', 0),
                                "rebounds_per_game": stats.get('avgRebounds', 0),
                                "assists_per_game": stats.get('avgAssists', 0),
                                "threes_per_game": stats.get('avg3PointFieldGoalsMade', 0),
                                "minutes_per_game": stats.get('avgMinutes', 0),
                                "games_played": stats.get('gamesPlayed', 0)
                            }
                
                return None
            else:
                return None
                
        except Exception as e:
            print(f"⚠️ Could not fetch stats for player {player_id}: {e}")
            return None
    
    def predict_player_props(self, player_name: str, player_stats: Dict, 
                            opponent_team: str, home_away: str) -> Dict:
        """Generate prop predictions for a player"""
        
        if not player_stats:
            return {"props_available": False, "reason": "No stats available"}
        
        # Base stats from season averages
        ppg = player_stats.get('points_per_game', 0)
        rpg = player_stats.get('rebounds_per_game', 0)
        apg = player_stats.get('assists_per_game', 0)
        threes_pg = player_stats.get('threes_per_game', 0)
        
        # Adjustments based on home/away
        home_boost = 1.05 if home_away == 'home' else 0.95  # 5% boost at home
        
        # Adjust for opponent defense (simplified - would use real defensive ratings)
        opponent_adjustment = 1.0  # Could be enhanced with real data
        
        # Calculate predicted lines
        predicted_points = ppg * home_boost * opponent_adjustment
        predicted_rebounds = rpg * home_boost * opponent_adjustment
        predicted_assists = apg * home_boost * opponent_adjustment
        predicted_threes = threes_pg * home_boost * opponent_adjustment
        predicted_pra = predicted_points + predicted_rebounds + predicted_assists
        
        # Market lines (typically slightly below actual averages)
        market_points = predicted_points - 1.5
        market_rebounds = predicted_rebounds - 0.5
        market_assists = predicted_assists - 0.5
        market_threes = predicted_threes - 0.5
        market_pra = predicted_pra - 2.5
        
        # Calculate confidence (based on consistency - simplified)
        # Higher averages = more consistent = higher confidence
        points_confidence = min(0.85, 0.55 + (ppg / 50))  # Max 85%
        rebounds_confidence = min(0.80, 0.55 + (rpg / 20))
        assists_confidence = min(0.80, 0.55 + (apg / 15))
        threes_confidence = min(0.75, 0.50 + (threes_pg / 8))
        pra_confidence = min(0.80, 0.60 + ((ppg + rpg + apg) / 100))
        
        # Determine recommendations (Over/Under based on edge)
        props = {
            "player_name": player_name,
            "props_available": True,
            
            # POINTS
            "points": {
                "predicted": round(predicted_points, 1),
                "market_line": round(market_points, 1),
                "recommendation": "OVER" if predicted_points > market_points + 1 else "UNDER" if predicted_points < market_points - 1 else "PASS",
                "confidence": round(points_confidence, 3),
                "edge": round(predicted_points - market_points, 1)
            },
            
            # REBOUNDS
            "rebounds": {
                "predicted": round(predicted_rebounds, 1),
                "market_line": round(predicted_rebounds - 0.5, 1),
                "recommendation": "OVER" if predicted_rebounds > predicted_rebounds - 0.5 + 0.5 else "PASS",
                "confidence": round(rebounds_confidence, 3),
                "edge": round(0.5, 1)
            },
            
            # ASSISTS
            "assists": {
                "predicted": round(predicted_assists, 1),
                "market_line": round(predicted_assists - 0.5, 1),
                "recommendation": "OVER" if predicted_assists > predicted_assists - 0.5 + 0.5 else "PASS",
                "confidence": round(assists_confidence, 3),
                "edge": round(0.5, 1)
            },
            
            # 3-POINTERS
            "threes": {
                "predicted": round(predicted_threes, 1),
                "market_line": round(predicted_threes - 0.5, 1),
                "recommendation": "OVER" if predicted_threes > predicted_threes - 0.5 + 0.5 else "PASS",
                "confidence": round(threes_confidence, 3),
                "edge": round(0.5, 1)
            },
            
            # PRA (Points + Rebounds + Assists) - Very popular combo prop
            "pra": {
                "predicted": round(predicted_pra, 1),
                "market_line": round(market_pra, 1),
                "recommendation": "OVER" if predicted_pra > market_pra + 2 else "UNDER" if predicted_pra < market_pra - 2 else "PASS",
                "confidence": round(pra_confidence, 3),
                "edge": round(predicted_pra - market_pra, 1)
            },
            
            # High confidence props only (75%+)
            "high_confidence_props": []
        }
        
        # Filter for high confidence recommendations
        for prop_type in ['points', 'rebounds', 'assists', 'threes', 'pra']:
            prop_data = props[prop_type]
            if prop_data['confidence'] >= 0.75 and prop_data['recommendation'] in ['OVER', 'UNDER']:
                props['high_confidence_props'].append({
                    "type": prop_type.upper(),
                    "recommendation": f"{prop_data['recommendation']} {prop_data['market_line']}",
                    "confidence": prop_data['confidence'],
                    "predicted": prop_data['predicted']
                })
        
        return props
    
    def get_star_players_props(self, home_team: str, away_team: str, 
                               home_team_id: int, away_team_id: int) -> List[Dict]:
        """Get prop predictions for star players in the game"""
        
        all_props = []
        
        # Identify star players for each team
        home_stars = self._get_team_stars(home_team)
        away_stars = self._get_team_stars(away_team)
        
        print(f"\n🌟 Analyzing star player props for {away_team} @ {home_team}")
        
        if not home_stars and not away_stars:
            print(f"   ⚠️ No star players identified for these teams")
            # Use mock data for demonstration
            return self._get_mock_player_props(home_team, away_team)
        
        # Get home team roster
        home_roster = self.get_team_roster(home_team_id)
        away_roster = self.get_team_roster(away_team_id)
        
        # If rosters are empty, use mock data
        if not home_roster and not away_roster:
            print(f"   ⚠️ Could not fetch rosters, using mock data for demonstration")
            return self._get_mock_player_props(home_team, away_team)
        
        # Analyze home team stars
        for star_name in home_stars:
            player = self._find_player_in_roster(star_name, home_roster)
            if player:
                print(f"   📊 Analyzing {star_name} (Home)")
                stats = self.get_player_season_stats(player['id'])
                if stats:
                    props = self.predict_player_props(star_name, stats, away_team, 'home')
                    all_props.append(props)
        
        # Analyze away team stars
        for star_name in away_stars:
            player = self._find_player_in_roster(star_name, away_roster)
            if player:
                print(f"   📊 Analyzing {star_name} (Away)")
                stats = self.get_player_season_stats(player['id'])
                if stats:
                    props = self.predict_player_props(star_name, stats, home_team, 'away')
                    all_props.append(props)
        
        # If no props generated, use mock data
        if not all_props:
            print(f"   ⚠️ No real stats available, using mock data for demonstration")
            return self._get_mock_player_props(home_team, away_team)
        
        return all_props
    
    def _get_mock_player_props(self, home_team: str, away_team: str) -> List[Dict]:
        """Generate mock player props for demonstration purposes"""
        
        mock_props = []
        
        # Get star players for both teams
        home_stars = self._get_team_stars(home_team)
        away_stars = self._get_team_stars(away_team)
        
        all_stars = []
        if home_stars:
            all_stars.extend([(star, 'home') for star in home_stars[:2]])  # Top 2 home stars
        if away_stars:
            all_stars.extend([(star, 'away') for star in away_stars[:2]])  # Top 2 away stars
        
        # Mock stats for popular NBA stars
        star_stats = {
            "LeBron James": {"ppg": 25.5, "rpg": 7.2, "apg": 8.1, "3pg": 1.8},
            "Anthony Davis": {"ppg": 24.3, "rpg": 12.1, "apg": 3.5, "3pg": 0.8},
            "Stephen Curry": {"ppg": 27.4, "rpg": 4.5, "apg": 5.8, "3pg": 4.2},
            "Draymond Green": {"ppg": 8.6, "rpg": 7.5, "apg": 6.2, "3pg": 0.7},
            "Nikola Jokic": {"ppg": 29.5, "rpg": 13.7, "apg": 10.2, "3pg": 1.2},
            "Jamal Murray": {"ppg": 21.2, "rpg": 4.1, "apg": 6.5, "3pg": 2.4},
            "Jayson Tatum": {"ppg": 26.8, "rpg": 8.3, "apg": 4.9, "3pg": 3.1},
            "Jaylen Brown": {"ppg": 23.7, "rpg": 5.8, "apg": 3.6, "3pg": 2.2},
            "Giannis Antetokounmpo": {"ppg": 31.2, "rpg": 11.5, "apg": 6.1, "3pg": 0.5},
            "Damian Lillard": {"ppg": 25.8, "rpg": 4.3, "apg": 7.2, "3pg": 3.5},
            "Luka Doncic": {"ppg": 33.5, "rpg": 9.2, "apg": 9.8, "3pg": 3.8},
            "Kyrie Irving": {"ppg": 26.1, "rpg": 5.1, "apg": 5.5, "3pg": 2.9},
            "Kevin Durant": {"ppg": 28.7, "rpg": 6.8, "apg": 5.3, "3pg": 2.1},
            "Devin Booker": {"ppg": 27.3, "rpg": 4.5, "apg": 6.9, "3pg": 2.7},
        }
        
        for star_name, location in all_stars:
            if star_name in star_stats:
                stats_data = star_stats[star_name]
                mock_stats = {
                    "points_per_game": stats_data["ppg"],
                    "rebounds_per_game": stats_data["rpg"],
                    "assists_per_game": stats_data["apg"],
                    "threes_per_game": stats_data["3pg"],
                    "minutes_per_game": 35.0,
                    "games_played": 45
                }
                
                opponent = away_team if location == 'home' else home_team
                props = self.predict_player_props(star_name, mock_stats, opponent, location)
                mock_props.append(props)
        
        return mock_props
    
    def _get_team_stars(self, team_name: str) -> List[str]:
        """Get list of star players for a team"""
        # Extract team nickname (e.g., "Los Angeles Lakers" -> "Lakers")
        for nickname, stars in self.star_players.items():
            if nickname in team_name:
                return stars
        return []
    
    def _find_player_in_roster(self, player_name: str, roster: List[Dict]) -> Optional[Dict]:
        """Find a player in the roster by name"""
        for player in roster:
            if player['name'] == player_name or player_name in player['name']:
                return player
        return None
    
    def display_player_props(self, props: Dict):
        """Display player prop predictions in a readable format"""
        
        if not props.get('props_available', False):
            print(f"   ⚠️ No props available: {props.get('reason', 'Unknown')}")
            return
        
        print(f"\n   🎯 {props['player_name']} - PLAYER PROPS")
        print(f"   " + "=" * 50)
        
        # Points
        pts = props['points']
        print(f"   📊 POINTS: {pts['recommendation']} {pts['market_line']} ({pts['confidence']:.1%})")
        print(f"      Predicted: {pts['predicted']} | Edge: {pts['edge']:+.1f}")
        
        # Rebounds
        reb = props['rebounds']
        print(f"   🏀 REBOUNDS: {reb['recommendation']} {reb['market_line']} ({reb['confidence']:.1%})")
        print(f"      Predicted: {reb['predicted']}")
        
        # Assists
        ast = props['assists']
        print(f"   🎯 ASSISTS: {ast['recommendation']} {ast['market_line']} ({ast['confidence']:.1%})")
        print(f"      Predicted: {ast['predicted']}")
        
        # 3-Pointers
        threes = props['threes']
        print(f"   🎯 3-POINTERS: {threes['recommendation']} {threes['market_line']} ({threes['confidence']:.1%})")
        print(f"      Predicted: {threes['predicted']}")
        
        # PRA (Most popular combo)
        pra = props['pra']
        print(f"   🔥 PRA (Pts+Reb+Ast): {pra['recommendation']} {pra['market_line']} ({pra['confidence']:.1%})")
        print(f"      Predicted: {pra['predicted']} | Edge: {pra['edge']:+.1f}")
        
        # High confidence recommendations
        if props['high_confidence_props']:
            print(f"\n   ✅ HIGH CONFIDENCE PROPS (75%+):")
            for prop in props['high_confidence_props']:
                print(f"      • {prop['type']}: {prop['recommendation']} ({prop['confidence']:.1%})")
        else:
            print(f"\n   ⚠️ No props meet 75% confidence threshold")
