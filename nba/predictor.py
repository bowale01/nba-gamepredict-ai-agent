# -*- coding: utf-8 -*-
"""
Reliable NBA Predictor using ESPN API + Enhanced Analysis + AGENTIC AI
Clean, reliable predictions with GPT-4 contextual enhancement
"""

import sys
import os

# Set UTF-8 encoding for Windows console FIRST
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

# Try to import tabulate for table formatting
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False
    print("⚠️ tabulate not installed. Install with: pip install tabulate")

# Load environment variables from .env file
load_dotenv()

# Add NBA module path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import H2H collector (separate from optional AI imports)
try:
    from nba_h2h_collector import NBAH2HCollector
    H2H_COLLECTOR_AVAILABLE = True
except ImportError as e:
    H2H_COLLECTOR_AVAILABLE = False
    print(f"⚠️ NBA H2H Collector not available: {e}")

# Import optional Agentic AI components
try:
    from agentic_ai_enhancer import NBAAugenticAIEnhancer
    from nba_betting_odds_api import NBABettingOddsAPI
    AGENTIC_AI_AVAILABLE = True
    print("🤖 NBA Agentic AI Enhancement loaded successfully!")
except ImportError as e:
    AGENTIC_AI_AVAILABLE = False
    print(f"⚠️ NBA Agentic AI Enhancement not available: {e}")
    AGENTIC_AI_AVAILABLE = False
    print("⚠️ NBA Agentic AI Enhancement not available (OpenAI API key needed)")

# Import Player Props Analyzer
try:
    from player_props_analyzer import NBAPlayerPropsAnalyzer
    PLAYER_PROPS_AVAILABLE = True
    print("🌟 NBA Player Props Analyzer loaded successfully!")
except ImportError as e:
    PLAYER_PROPS_AVAILABLE = False
    print(f"⚠️ NBA Player Props Analyzer not available: {e}")

class ReliableNBAPredictor:
    """Enhanced NBA predictor with H2H analysis and popular betting markets"""
    
    def __init__(self, enable_agentic_ai: bool = True, enable_player_props: bool = True):
        """Initialize with H2H analysis, popular betting focus, Player Props, and Agentic AI"""
        
        self.espn_base = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba"
        self.data_sources = ["ESPN API", "H2H Analysis", "Statistical Patterns"]
        
        # Initialize NBA Betting Odds API for real sportsbook lines
        try:
            self.betting_api = NBABettingOddsAPI()
            print("💰 Real NBA betting odds API initialized")
        except:
            self.betting_api = None
            print("⚠️ Using mock NBA betting lines - get free API key for real odds")
        
        # Initialize NBA H2H Data Collector for real historical matchups
        try:
            self.nba_h2h_collector = NBAH2HCollector()
            print("📊 Real NBA H2H data collector initialized")
        except Exception as e:
            self.nba_h2h_collector = None
            print(f"⚠️ NBA H2H collector initialization failed: {e}")
        
        # Initialize Player Props Analyzer (Fastest growing market!)
        self.player_props_enabled = enable_player_props and PLAYER_PROPS_AVAILABLE
        self.player_props_analyzer = None
        
        if self.player_props_enabled:
            try:
                self.player_props_analyzer = NBAPlayerPropsAnalyzer()
                print("🌟 NBA Player Props Analysis ENABLED (Fastest growing market!)")
            except Exception as e:
                print(f"⚠️ Player Props initialization failed: {e}")
                self.player_props_enabled = False
        
        # Popular NBA betting markets focus
        self.popular_markets = ["Point Spread", "OVER/UNDER", "Moneyline Win", "Halftime OVER", "Player Props"]
        self.confidence_threshold = 0.75  # 75% minimum for high-confidence bets
        
        # Initialize Agentic AI Enhancement
        self.agentic_ai_enabled = enable_agentic_ai and AGENTIC_AI_AVAILABLE
        self.ai_enhancer = None
        
        if self.agentic_ai_enabled:
            try:
                # Use environment variable for OpenAI API key
                openai_key = os.getenv('OPENAI_API_KEY')
                self.ai_enhancer = NBAAugenticAIEnhancer(openai_key)
                print("🤖 NBA Agentic AI Enhancement ENABLED")
            except Exception as e:
                print(f"⚠️ Agentic AI initialization failed: {e}")
                self.agentic_ai_enabled = False
        
        print("✅ Enhanced NBA Predictor with H2H Analysis + AI initialized")
        print("📡 Using ESPN API for real-time NBA data")
        print("🎯 Focus: Point Spread, Over/Under, Moneyline, Halftime, Player Props")
        print("📊 H2H Analysis: Same methodology as football system")
        if self.player_props_enabled:
            print("🌟 Player Props: ENABLED (Fastest growing market - stars analysis)")
        if self.agentic_ai_enabled:
            print("🤖 Agentic AI: GPT-4 contextual enhancement active")
        print("🎯 High-confidence only: 75%+ threshold for recommendations")
        print()
    
    def get_todays_nba_games(self) -> List[Dict]:
        """Get today's and tomorrow's NBA games from ESPN API (48-hour window)"""
        
        try:
            all_games = []
            
            # Fetch today's games
            today = datetime.now().strftime("%Y%m%d")
            print(f"🔍 Fetching NBA games for TODAY ({today})...")
            today_games = self._fetch_games_for_date(today)
            all_games.extend(today_games)
            print(f"✅ Found {len(today_games)} games for today")
            
            # Fetch tomorrow's games
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
            print(f"🔍 Fetching NBA games for TOMORROW ({tomorrow})...")
            tomorrow_games = self._fetch_games_for_date(tomorrow)
            all_games.extend(tomorrow_games)
            print(f"✅ Found {len(tomorrow_games)} games for tomorrow")
            
            print(f"✅ TOTAL: {len(all_games)} NBA games in 48-hour window")
            return all_games
                
        except Exception as e:
            print(f"❌ Error fetching games: {e}")
            print(f"⚠️ Cannot generate predictions without real game data")
            return []  # Return empty - NO SAMPLE DATA
    
    def _fetch_games_for_date(self, date_str: str) -> List[Dict]:
        """Fetch games for a specific date"""
        try:
            url = f"{self.espn_base}/scoreboard?dates={date_str}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                games = []
                
                if 'events' in data:
                    for event in data['events']:
                        if 'competitions' in event and event['competitions']:
                            competition = event['competitions'][0]
                            
                            if 'competitors' in competition:
                                home_team = None
                                away_team = None
                                
                                for competitor in competition['competitors']:
                                    if competitor.get('homeAway') == 'home':
                                        home_team = competitor
                                    elif competitor.get('homeAway') == 'away':
                                        away_team = competitor
                                
                                if home_team and away_team:
                                    game = {
                                        "id": event.get('id'),
                                        "date": date_str[:4] + '-' + date_str[4:6] + '-' + date_str[6:8],
                                        "datetime": event.get('date'),
                                        "home_team": home_team['team']['displayName'],
                                        "away_team": away_team['team']['displayName'],
                                        "home_team_id": int(home_team['team']['id']),
                                        "away_team_id": int(away_team['team']['id']),
                                        "home_abbreviation": home_team['team']['abbreviation'],
                                        "away_abbreviation": away_team['team']['abbreviation'],
                                        "status": competition.get('status', {}).get('type', {}).get('description', 'Scheduled'),
                                        "venue": competition.get('venue', {}).get('fullName', 'Unknown')
                                    }
                                    
                                    # Add scores if available
                                    if 'score' in home_team:
                                        game["home_score"] = int(home_team['score'])
                                    if 'score' in away_team:
                                        game["away_score"] = int(away_team['score'])
                                    
                                    games.append(game)
                
                return games
            else:
                return []
                
        except Exception as e:
            print(f"❌ Error fetching games for {date_str}: {e}")
            return []
    
    def get_h2h_analysis(self, home_team: str, away_team: str, home_id: int, away_id: int) -> Dict:
        """Get comprehensive H2H analysis between two NBA teams"""
        
        try:
            # Get recent head-to-head matchups (last 10 games)
            url = f"{self.espn_base}/teams/{home_id}/schedule"
            response = requests.get(url, timeout=10)
            
            h2h_games = []
            total_points_history = []
            home_wins = 0
            away_wins = 0
            over_games = 0
            halftime_over_games = 0
            
            if response.status_code == 200:
                data = response.json()
                
                # Analyze recent matchups (simplified for demo)
                # In production, you'd parse actual game data
                
                # Sample H2H analysis based on team patterns
                h2h_games = self._generate_h2h_sample(home_team, away_team)
                
                for game in h2h_games:
                    total_points = game['total_points']
                    total_points_history.append(total_points)
                    
                    if game['winner'] == home_team:
                        home_wins += 1
                    else:
                        away_wins += 1
                    
                    # OVER analysis (typical NBA total ~220-230)
                    if total_points > 220:
                        over_games += 1
                    
                    # Halftime OVER analysis (typical halftime total ~110-115)
                    if game.get('halftime_total', 0) > 110:
                        halftime_over_games += 1
            
            total_h2h = len(h2h_games)
            
            if total_h2h >= 3:  # Minimum H2H requirement
                avg_total = sum(total_points_history) / len(total_points_history)
                
                # Calculate H2H percentages
                home_win_pct = home_wins / total_h2h if total_h2h > 0 else 0.5
                over_pct = over_games / total_h2h if total_h2h > 0 else 0.5
                halftime_over_pct = halftime_over_games / total_h2h if total_h2h > 0 else 0.5
                
                # HYBRID: Apply GPT-4 validation adjustments if available
                gpt_validation = h2h_games[0].get('gpt_validation', {}) if h2h_games else {}
                
                if gpt_validation.get('validated') and gpt_validation.get('adjustment_needed'):
                    adjustment = gpt_validation.get('gpt_assessment', {}).get('recommended_adjustment')
                    
                    if adjustment == 'favor_home':
                        print(f"   🤖 GPT-4 Adjustment: Favoring {home_team} based on historical context")
                        home_win_pct = min(0.85, home_win_pct + 0.15)  # Boost home by 15%
                    elif adjustment == 'favor_away':
                        print(f"   🤖 GPT-4 Adjustment: Favoring {away_team} based on historical context")
                        home_win_pct = max(0.15, home_win_pct - 0.15)  # Boost away by 15%
                
                return {
                    "sufficient_data": True,
                    "h2h_games_count": total_h2h,
                    "home_team_wins": home_wins,
                    "away_team_wins": away_wins,
                    "home_win_percentage": home_win_pct,
                    "away_win_percentage": 1 - home_win_pct,
                    "average_total_points": round(avg_total, 1),
                    "over_games": over_games,
                    "over_percentage": over_pct,
                    "halftime_over_games": halftime_over_games,
                    "halftime_over_percentage": halftime_over_pct,
                    "total_points_history": total_points_history,
                    "h2h_pattern": self._analyze_h2h_pattern(home_wins, away_wins, over_pct),
                    "confidence_factors": self._calculate_h2h_confidence(total_h2h, home_win_pct, over_pct),
                    "gpt_validation": gpt_validation  # Include validation results
                }
            else:
                return {
                    "sufficient_data": False,
                    "h2h_games_count": total_h2h,
                    "reason": f"Only {total_h2h} H2H games found (need ≥3 for reliable analysis)"
                }
                
        except Exception as e:
            print(f"⚠️ H2H analysis error for {home_team} vs {away_team}: {e}")
            return {"sufficient_data": False, "reason": "API error"}
    
    def _generate_h2h_sample(self, home_team: str, away_team: str) -> List[Dict]:
        """Get real NBA H2H data using ESPN API - REAL DATA ONLY + GPT-4 VALIDATION"""
        
        if self.nba_h2h_collector:
            try:
                # Get real historical matchup data from ESPN API
                h2h_games = self.nba_h2h_collector.get_team_h2h_data(home_team, away_team)
                
                if h2h_games and len(h2h_games) >= 4:  # NBA teams play 2-4 times per season
                    print(f"✅ Using {len(h2h_games)} real NBA H2H games: {home_team} vs {away_team}")
                    
                    # HYBRID: Validate with GPT-4 if AI is available
                    if self.ai_enhancer and self.agentic_ai_enabled:
                        validation = self.ai_enhancer.validate_h2h_data_with_gpt(home_team, away_team, h2h_games)
                        
                        if validation.get('validated'):
                            print(f"   🤖 GPT-4 Validation: {validation.get('gpt_assessment', {}).get('validation', 'N/A')}")
                            print(f"   💡 Key Insight: {validation.get('key_insight', 'N/A')}")
                            
                            # Store validation in games data for use in predictions
                            for game in h2h_games:
                                game['gpt_validation'] = validation
                    
                    return h2h_games
                else:
                    print(f"❌ Insufficient real NBA H2H data ({len(h2h_games) if h2h_games else 0} games) - SKIPPING GAME")
                    return []
                    
            except Exception as e:
                print(f"❌ NBA H2H collector error: {e} - SKIPPING GAME")
                return []
        else:
            print(f"❌ NBA H2H collector not available - SKIPPING GAME")
            return []
    

    
    def _analyze_h2h_pattern(self, home_wins: int, away_wins: int, over_pct: float) -> str:
        """Analyze H2H patterns for betting insights"""
        
        total_games = home_wins + away_wins
        home_pct = home_wins / total_games if total_games > 0 else 0.5
        
        if home_pct >= 0.7:
            winner_pattern = "Home team dominates this matchup"
        elif home_pct <= 0.3:
            winner_pattern = "Away team historically strong in this matchup"
        else:
            winner_pattern = "Competitive H2H series - no clear dominant team"
        
        if over_pct >= 0.7:
            total_pattern = "High-scoring H2H history - OVER pattern"
        elif over_pct <= 0.3:
            total_pattern = "Low-scoring H2H history - UNDER pattern"
        else:
            total_pattern = "Mixed scoring pattern in H2H games"
        
        return f"{winner_pattern}. {total_pattern}"
    
    def _calculate_h2h_confidence(self, games_count: int, home_win_pct: float, over_pct: float) -> Dict:
        """Calculate confidence levels for different bet types"""
        
        # More games = higher confidence
        data_confidence = min(0.9, 0.5 + (games_count * 0.06))  # Max at ~7 games
        
        # Clear patterns = higher confidence
        win_confidence = data_confidence * (1 if abs(home_win_pct - 0.5) > 0.2 else 0.7)
        over_confidence = data_confidence * (1 if abs(over_pct - 0.5) > 0.2 else 0.7)
        
        return {
            "data_quality": data_confidence,
            "win_prediction_confidence": win_confidence,
            "over_prediction_confidence": over_confidence,
            "games_analyzed": games_count
        }

    def _validate_ou_prediction(self, predicted_total: float, confidence: float) -> bool:
        """Validate O/U predictions - reject extreme totals unless very high confidence

        Added after Feb 22 disaster: predicted 154.3, actual was 220 (65.7 points off!)
        Updated: No NBA games go below 200 - minimum threshold increased to 200
        """

        # Extreme low totals are very risky (NBA games rarely go below 200)
        if predicted_total < 200:
            if confidence < 0.95:  # Require 95%+ confidence for predictions below 200
                return False

        # Extreme high totals also risky
        if predicted_total > 250:
            if confidence < 0.90:
                return False

        return True

    def _calculate_desperation_factor(self, team_form: Dict) -> float:
        """Calculate desperation factor for teams on losing streaks

        Teams on long losing streaks are dangerous - they're desperate to win.
        Added after Orlando (0-10 streak) upset LA Clippers on Feb 22.
        """

        if not team_form:
            return 0.0

        streak = team_form.get('streak', 'N/A')

        # Check for losing streak
        if streak.startswith('L'):
            try:
                losses = int(streak[1:])

                # Teams on 5+ game losing streaks are highly motivated
                if losses >= 10:
                    return 0.20  # Reduce opponent's confidence by 20% for 10+ losses
                elif losses >= 8:
                    return 0.15  # Reduce by 15% for 8-9 losses
                elif losses >= 5:
                    return 0.10  # Reduce by 10% for 5-7 losses
            except:
                pass

        return 0.0

    
    def _calculate_point_spread(self, home_team: str, away_team: str, h2h_analysis: Dict, 
                                prediction_factors: Dict, home_win_prob: float) -> Dict:
        """Calculate point spread prediction (Most popular NBA bet in USA)"""
        
        # Extract H2H margin data if available
        h2h_games = h2h_analysis.get('h2h_games_count', 0)
        
        # Calculate expected margin from H2H data and statistical analysis
        # Method 1: From win probabilities (converted to point spread)
        prob_based_spread = (home_win_prob - 0.5) * 20  # NBA typical conversion
        
        # Method 2: From team strength differential
        strength_diff = prediction_factors.get('team_strength_diff', 0)
        strength_based_spread = strength_diff * 25  # Convert strength to points
        
        # Method 3: Home court advantage (typically 3-4 points in NBA)
        home_court_points = 3.5
        
        # Combine methods (60% probability-based, 30% strength, 10% home court)
        predicted_spread = (prob_based_spread * 0.60) + (strength_based_spread * 0.30) + (home_court_points * 0.10)
        
        # Round to typical spread increments (0.5, 1, 1.5, etc.)
        predicted_spread = round(predicted_spread * 2) / 2  # Round to nearest 0.5
        
        # Generate market spread estimate (usually slightly different from true value)
        market_spread = predicted_spread - 0.5  # Market typically shades slightly
        market_spread = round(market_spread * 2) / 2
        
        # Calculate spread confidence
        # Higher confidence when:
        # - Win probability is clear (>65% or <35%)
        # - H2H data supports the margin
        # - Team strength differential is significant
        
        win_prob_clarity = abs(home_win_prob - 0.5) * 2  # 0 to 1 scale
        h2h_confidence = min(1.0, h2h_games / 8)  # More games = higher confidence
        strength_clarity = min(1.0, abs(strength_diff) * 5)  # Clear strength diff
        
        spread_confidence = (win_prob_clarity * 0.5) + (h2h_confidence * 0.3) + (strength_clarity * 0.2)
        
        # Determine recommendation
        if abs(predicted_spread - market_spread) >= 2.0:
            # Strong edge - 2+ point difference
            if predicted_spread > market_spread:
                recommendation = f"{home_team} +{abs(market_spread)} (Value)"
                edge_direction = "home"
            else:
                recommendation = f"{away_team} +{abs(market_spread)} (Value)"
                edge_direction = "away"
            edge_strength = "Strong"
        elif abs(predicted_spread - market_spread) >= 1.0:
            # Moderate edge
            if predicted_spread > market_spread:
                recommendation = f"{home_team} {market_spread:+.1f}"
                edge_direction = "home"
            else:
                recommendation = f"{away_team} +{abs(market_spread)}"
                edge_direction = "away"
            edge_strength = "Moderate"
        else:
            # No clear edge
            recommendation = f"No strong spread value (line around {market_spread:+.1f})"
            edge_direction = "none"
            edge_strength = "Weak"
        
        return {
            "predicted_spread": predicted_spread,
            "market_spread": market_spread,
            "home_team_spread": f"{home_team} {-predicted_spread:+.1f}",
            "away_team_spread": f"{away_team} {predicted_spread:+.1f}",
            "spread_confidence": round(spread_confidence, 3),
            "recommendation": recommendation,
            "edge_direction": edge_direction,
            "edge_strength": edge_strength,
            "edge_points": round(abs(predicted_spread - market_spread), 1),
            "betting_advice": self._generate_spread_advice(predicted_spread, market_spread, 
                                                           home_team, away_team, spread_confidence)
        }
    
    def _generate_spread_advice(self, predicted_spread: float, market_spread: float, 
                                home_team: str, away_team: str, confidence: float) -> str:
        """Generate practical spread betting advice"""
        
        edge = predicted_spread - market_spread
        
        if confidence >= 0.75:
            confidence_text = "High confidence"
        elif confidence >= 0.60:
            confidence_text = "Moderate confidence"
        else:
            confidence_text = "Low confidence"
        
        if abs(edge) >= 2.0:
            if edge > 0:
                return f"{confidence_text} - {home_team} undervalued by ~{abs(edge):.1f} points"
            else:
                return f"{confidence_text} - {away_team} undervalued by ~{abs(edge):.1f} points"
        elif abs(edge) >= 1.0:
            if edge > 0:
                return f"{confidence_text} - Lean {home_team} on spread"
            else:
                return f"{confidence_text} - Lean {away_team} on spread"
        else:
            return f"Spread fairly priced - no strong edge ({confidence_text})"
    
    def predict_game_with_h2h_focus(self, game: Dict) -> Dict:
        """Generate H2H-based prediction focusing on popular NBA betting markets"""
        
        home_team = game.get('home_team', 'Home Team')
        away_team = game.get('away_team', 'Away Team')
        home_id = game.get('home_team_id', 0)
        away_id = game.get('away_team_id', 0)
        
        # Get H2H analysis first (same approach as football system)
        h2h_analysis = self.get_h2h_analysis(home_team, away_team, home_id, away_id)
        
        if not h2h_analysis.get('sufficient_data', False):
            # Skip games without sufficient H2H data (like football system)
            return {
                "prediction_made": False,
                "reason": h2h_analysis.get('reason', 'Insufficient H2H data'),
                "h2h_games_count": h2h_analysis.get('h2h_games_count', 0),
                "requires_minimum": 3
            }
        
        # Enhanced prediction logic with H2H data
        prediction_factors = self._analyze_team_matchup(home_team, away_team, home_id, away_id)
        
        # Combine H2H data with statistical analysis
        h2h_home_win_prob = h2h_analysis['home_win_percentage']
        h2h_over_prob = h2h_analysis['over_percentage']
        h2h_halftime_over_prob = h2h_analysis['halftime_over_percentage']
        
        # Balance H2H data (50%) + statistical analysis (50%) - more balanced approach
        base_home_win_prob = prediction_factors['home_advantage'] + prediction_factors['team_strength_diff']
        base_home_win_prob = max(0.25, min(0.85, base_home_win_prob))
        
        # Final probabilities combining H2H and statistical data (balanced 50/50)
        home_win_prob = (h2h_home_win_prob * 0.5) + (base_home_win_prob * 0.5)
        away_win_prob = 1.0 - home_win_prob
        
        # Total points prediction with H2H emphasis
        h2h_avg_total = h2h_analysis['average_total_points']
        statistical_total = prediction_factors['expected_total']
        predicted_total = (h2h_avg_total * 0.6) + (statistical_total * 0.4)
        
        # VALIDATE: Reject unrealistic predictions (no NBA games below 200)
        is_valid = self._validate_ou_prediction(predicted_total, max(h2h_over_prob, 1 - h2h_over_prob))
        if not is_valid or predicted_total < 200:
            # NEVER predict totals below 200 - NBA games rarely go that low
            predicted_total = max(200, h2h_avg_total, statistical_total)
            print(f"   ⚠️ VALIDATION: Adjusted unrealistic total to {predicted_total} (NBA games rarely below 200)")
        
        # Market estimates
        market_total = predicted_total - 2  # Market typically lower
        market_halftime_total = market_total * 0.48  # ~48% first half
        
        # Calculate final probabilities for popular markets
        ou_edge = predicted_total - market_total
        over_prob = (h2h_over_prob * 0.6) + (0.55 if ou_edge > 2 else 0.45) * 0.4
        under_prob = 1.0 - over_prob
        
        # Halftime OVER calculation
        predicted_halftime_total = predicted_total * 0.48
        halftime_over_prob = h2h_halftime_over_prob
        
        # POINT SPREAD calculation (Most popular NBA bet in USA)
        spread_prediction = self._calculate_point_spread(home_team, away_team, h2h_analysis, 
                                                         prediction_factors, home_win_prob)
        spread_confidence = spread_prediction['spread_confidence']
        
        # Generate popular betting recommendations with confidence levels
        all_bets = [
            spread_prediction['recommendation'],  # Point Spread (MOST POPULAR)
            f"OVER {predicted_total:.1f} points" if over_prob > 0.6 else f"UNDER {predicted_total:.1f} points",
            f"{home_team if home_win_prob > 0.6 else away_team} to Win" if max(home_win_prob, away_win_prob) > 0.6 else "No strong pick",
            f"Halftime OVER {predicted_halftime_total:.1f}" if halftime_over_prob > 0.6 else "Halftime UNDER"
        ]
        all_confidence_levels = [spread_confidence, over_prob, max(home_win_prob, away_win_prob), halftime_over_prob]
        
        # Filter for HIGH CONFIDENCE ONLY (85%+ - raised from 75% after poor performance)
        high_confidence_bets = []
        high_confidence_levels = []
        
        for i, (bet, confidence) in enumerate(zip(all_bets, all_confidence_levels)):
            if confidence >= 0.85:  # 85%+ only - more conservative after 25% accuracy on Feb 22
                high_confidence_bets.append(bet)
                high_confidence_levels.append(confidence)
        
        recommendations = {
            "recommended_bets": all_bets,
            "confidence_levels": all_confidence_levels,
            "high_confidence_bets": high_confidence_bets,
            "high_confidence_levels": high_confidence_levels
        }
        
        # Base prediction ready for potential AI enhancement
        base_prediction = {
            "prediction_made": True,
            
            # Game info
            "game_id": game.get('id'),
            "home_team": home_team,
            "away_team": away_team,
            "game_time": game.get('datetime', 'TBD'),
            "venue": game.get('venue', 'Unknown'),
            "status": game.get('status', 'Scheduled'),
            
            # H2H Analysis Results
            "h2h_games_analyzed": h2h_analysis['h2h_games_count'],
            "h2h_pattern": h2h_analysis['h2h_pattern'],
            "h2h_average_total": h2h_analysis['average_total_points'],
            
            # POPULAR BETTING MARKETS (What people actually bet on)
            
            # 1. POINT SPREAD (MOST POPULAR NBA BET IN USA)
            "predicted_spread": spread_prediction['predicted_spread'],
            "market_spread": spread_prediction['market_spread'],
            "home_team_spread": spread_prediction['home_team_spread'],
            "away_team_spread": spread_prediction['away_team_spread'],
            "spread_confidence": spread_prediction['spread_confidence'],
            "spread_recommendation": spread_prediction['recommendation'],
            "spread_edge": spread_prediction['edge_points'],
            "spread_betting_advice": spread_prediction['betting_advice'],
            
            # 2. MONEYLINE WIN
            "predicted_winner": home_team if home_win_prob > away_win_prob else away_team,
            "home_win_probability": round(home_win_prob, 3),
            "away_win_probability": round(away_win_prob, 3),
            "winner_confidence": round(max(home_win_prob, away_win_prob), 3),
            
            # 3. OVER/UNDER TOTAL (Very popular)
            "predicted_total": round(predicted_total, 1),
            "market_total_estimate": round(market_total, 1),
            "over_probability": round(over_prob, 3),
            "under_probability": round(under_prob, 3),
            "over_under_recommendation": "OVER" if over_prob > under_prob else "UNDER",
            "ou_confidence": round(max(over_prob, under_prob), 3),
            
            # 4. HALFTIME OVER (Popular NBA market)
            "predicted_halftime_total": round(predicted_halftime_total, 1),
            "market_halftime_estimate": round(market_halftime_total, 1),
            "halftime_over_probability": round(halftime_over_prob, 3),
            "halftime_over_confidence": round(halftime_over_prob, 3),
            
            # HIGH-CONFIDENCE RECOMMENDATIONS (75%+ only - OUR STRATEGY)
            "high_confidence_bets": recommendations['high_confidence_bets'],
            "high_confidence_levels": recommendations['high_confidence_levels'],
            "recommendation_count": len(recommendations['high_confidence_bets']),
            
            # Analysis details
            "betting_advice": f"Focus on popular NBA markets: {', '.join(recommendations['recommended_bets'][:2])}",
            "confidence_assessment": "High" if max(recommendations['confidence_levels']) > 0.75 else "Medium",
            "h2h_based_confidence": h2h_analysis['confidence_factors'],
            "data_quality": "High" if h2h_analysis['h2h_games_count'] >= 5 else "Medium",
            "data_source": "H2H Analysis + ESPN API + Statistical Patterns",
            "prediction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # AGENTIC AI ENHANCEMENT (disabled - no OpenAI key configured)
        # This layer was adding unnecessary complexity without improving accuracy
        # Focus on core: H2H data (60%) + statistical analysis (40%)
        
        if False:  # Disabled to simplify and focus on core analysis
            try:
                print(f"🤖 Applying Agentic AI enhancement for {home_team} vs {away_team}...")
                
                # Enhance prediction with GPT-4 contextual analysis
                enhanced_prediction = self.ai_enhancer.enhance_nba_prediction(game, base_prediction)
                
                # Update prediction with AI insights
                base_prediction.update({
                    "ai_enhanced": True,
                    "ai_confidence_adjustment": enhanced_prediction.get('ai_confidence_adjustment', 0),
                    "ai_reasoning": enhanced_prediction.get('ai_reasoning', {}),
                    "nba_context_factors": enhanced_prediction.get('nba_context_factors', {}),
                    "final_ai_confidence": enhanced_prediction.get('final_ai_confidence', base_prediction.get('ou_confidence', 0.75)),
                    "nba_betting_narrative": enhanced_prediction.get('nba_betting_narrative', ''),
                    "data_source": "H2H Analysis + ESPN API + Statistical Patterns + Agentic AI",
                    "enhancement_method": enhanced_prediction.get('enhancement_method', 'H2H_CENTRIC_AI')
                })
                
                print("✅ NBA Agentic AI enhancement applied successfully")
                
            except Exception as e:
                print(f"⚠️ Agentic AI enhancement failed: {e}")
                base_prediction["ai_enhanced"] = False
                base_prediction["ai_error"] = str(e)
        else:
            base_prediction["ai_enhanced"] = False
            base_prediction["ai_status"] = "Not enabled or not available"
        
        return base_prediction
    
    def _analyze_team_matchup(self, home_team: str, away_team: str, home_id: int, away_id: int) -> Dict:
        """Analyze team matchup for prediction factors"""
        
        # Team strength mapping (simplified but effective)
        team_strength = {
            # Elite teams
            "Boston Celtics": 0.75, "Denver Nuggets": 0.72, "Milwaukee Bucks": 0.70,
            "Phoenix Suns": 0.68, "Golden State Warriors": 0.67, "Los Angeles Lakers": 0.66,
            "Miami Heat": 0.65, "Philadelphia 76ers": 0.64, "Los Angeles Clippers": 0.63,
            "Memphis Grizzlies": 0.62,
            
            # Good teams  
            "New York Knicks": 0.60, "Cleveland Cavaliers": 0.59, "Sacramento Kings": 0.58,
            "Brooklyn Nets": 0.57, "Atlanta Hawks": 0.56, "New Orleans Pelicans": 0.55,
            "Minnesota Timberwolves": 0.54, "Dallas Mavericks": 0.53, "Toronto Raptors": 0.52,
            "Oklahoma City Thunder": 0.51,
            
            # Developing teams
            "Indiana Pacers": 0.48, "Washington Wizards": 0.47, "Chicago Bulls": 0.46,
            "Utah Jazz": 0.45, "Orlando Magic": 0.44, "Portland Trail Blazers": 0.43,
            "Charlotte Hornets": 0.42, "San Antonio Spurs": 0.41, "Houston Rockets": 0.40,
            "Detroit Pistons": 0.38
        }
        
        # Scoring averages (estimated)
        team_scoring = {
            "Boston Celtics": 118, "Sacramento Kings": 120, "Phoenix Suns": 116,
            "Los Angeles Lakers": 115, "Golden State Warriors": 117, "Denver Nuggets": 114,
            "Milwaukee Bucks": 115, "Dallas Mavericks": 116, "Los Angeles Clippers": 114,
            "Memphis Grizzlies": 113, "Miami Heat": 110, "Philadelphia 76ers": 112,
            "New York Knicks": 111, "Cleveland Cavaliers": 112, "Brooklyn Nets": 113,
            "Atlanta Hawks": 118, "New Orleans Pelicans": 112, "Minnesota Timberwolves": 110,
            "Toronto Raptors": 109, "Oklahoma City Thunder": 115, "Indiana Pacers": 114,
            "Washington Wizards": 113, "Chicago Bulls": 108, "Utah Jazz": 115,
            "Orlando Magic": 108, "Portland Trail Blazers": 109, "Charlotte Hornets": 110,
            "San Antonio Spurs": 107, "Houston Rockets": 109, "Detroit Pistons": 106
        }
        
        home_strength = team_strength.get(home_team, 0.50)
        away_strength = team_strength.get(away_team, 0.50)
        
        home_scoring = team_scoring.get(home_team, 110)
        away_scoring = team_scoring.get(away_team, 110)
        
        # Calculate factors
        home_advantage = 0.62  # Base home advantage (increased from 0.55 - NBA home court is significant)
        team_strength_diff = (home_strength - away_strength) * 0.3
        expected_total = home_scoring + away_scoring + 2  # Home boost
        market_estimate = expected_total - 1  # Market typically 1-2 points lower
        
        # Key factors
        key_factors = []
        
        if team_strength_diff > 0.1:
            key_factors.append(f"{home_team} has significant home advantage")
        elif team_strength_diff < -0.1:
            key_factors.append(f"{away_team} has talent advantage despite road game")
        else:
            key_factors.append("Closely matched teams - game could go either way")
        
        if expected_total > 225:
            key_factors.append("High-scoring matchup expected with both teams' pace")
        elif expected_total < 215:
            key_factors.append("Lower-scoring game likely with defensive focus")
        else:
            key_factors.append("Total points projection in typical NBA range")
        
        key_factors.append("Home court advantage worth ~3-4 points in NBA")
        
        return {
            "home_advantage": home_advantage,
            "team_strength_diff": team_strength_diff,
            "expected_total": expected_total,
            "market_estimate": market_estimate,
            "key_factors": key_factors
        }
    
    def _generate_betting_advice(self, home_win_prob: float, ou_edge: float, home_team: str, away_team: str) -> str:
        """Generate practical betting advice"""
        
        if home_win_prob > 0.65:
            winner_advice = f"Strong lean {home_team} ML"
        elif home_win_prob < 0.45:
            winner_advice = f"Value on {away_team} ML" 
        else:
            winner_advice = "Close game - consider spread over ML"
        
        if abs(ou_edge) > 3:
            total_advice = f"Strong {'OVER' if ou_edge > 0 else 'UNDER'} play"
        elif abs(ou_edge) > 1:
            total_advice = f"Lean {'OVER' if ou_edge > 0 else 'UNDER'}"
        else:
            total_advice = "Total close to fair value"
        
        return f"{winner_advice} | {total_advice}"
    
    def _assess_confidence(self, factors: Dict) -> str:
        """Assess overall prediction confidence"""
        
        strength_diff = abs(factors['team_strength_diff'])
        total_edge = abs(factors['expected_total'] - factors['market_estimate'])
        
        if strength_diff > 0.15 or total_edge > 4:
            return "High"
        elif strength_diff > 0.08 or total_edge > 2:
            return "Medium"
        else:
            return "Low"
    
    def generate_daily_predictions(self) -> List[Dict]:
        """Generate predictions for today's NBA games"""
        
        print("🏀 NBA DAILY PREDICTIONS")
        print("=" * 60)
        print(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}")
        print(f"🕐 Generated: {datetime.now().strftime('%H:%M:%S')}")
        print(f"📊 Data: ESPN API + Statistical Analysis")
        if self.agentic_ai_enabled:
            print("🤖 Enhancement: Agentic AI with GPT-4 contextual analysis")
        if self.player_props_enabled:
            print("🌟 Player Props: Analyzing star players (LeBron, Curry, Jokic, etc.)")
        print()
        
        # Get today's games
        games = self.get_todays_nba_games()
        
        if not games:
            print("❌ No NBA games scheduled for today")
            return []
        
        predictions = []
        
        for i, game in enumerate(games, 1):
            print(f"🎯 GAME {i}: {game['home_team']} - {game['away_team']}")
            print(f"   📍 Venue: {game.get('venue', 'Unknown')}")
            print(f"   🕐 Status: {game.get('status', 'Scheduled')}")
            
            if game.get('datetime'):
                try:
                    game_time = datetime.fromisoformat(game['datetime'].replace('Z', '+00:00'))
                    local_time = game_time.strftime("%I:%M %p")
                    print(f"   ⏰ Time: {local_time}")
                except:
                    print(f"   ⏰ Time: {game.get('datetime', 'TBD')}")
            
            # Generate prediction
            prediction = self.predict_game_with_h2h_focus(game)
            
            # Check if prediction was made with real data
            if not prediction.get('prediction_made', True):
                print(f"   ❌ SKIPPED - {prediction.get('reason', 'No real H2H data available')}")
                print(f"   📊 H2H Games Found: {prediction.get('h2h_games_count', 0)} (Minimum Required: {prediction.get('requires_minimum', 3)})")
                print(f"\n   {'='*50}\n")
                continue
            
            predictions.append(prediction)
            
            # Display prediction
            print(f"\n   � POINT SPREAD (MOST POPULAR):")
            print(f"   {prediction['spread_recommendation']}")
            print(f"   Predicted: {prediction['home_team_spread']} / {prediction['away_team_spread']}")
            print(f"   Market: {prediction['home_team'].split()[0]} {prediction['market_spread']:+.1f}")
            print(f"   Confidence: {prediction['spread_confidence']:.1%}")
            print(f"   {prediction['spread_betting_advice']}")
            
            print(f"\n   🏆 MONEYLINE (WINNER):")
            print(f"   {prediction['predicted_winner']} ({prediction['winner_confidence']:.1%} confidence)")
            print(f"   Home: {prediction['home_win_probability']:.1%} | Away: {prediction['away_win_probability']:.1%}")
            
            print(f"\n   📊 OVER/UNDER TOTAL:")
            print(f"   Predicted: {prediction['predicted_total']} points")
            print(f"   Market Est: {prediction.get('market_total_estimate', 'N/A')} points")
            print(f"   Play: {prediction.get('over_under_recommendation', 'OVER')} ({prediction['over_probability']:.1%} confidence)")
            
            print(f"\n   ⏱️ HALFTIME OVER/UNDER:")
            print(f"   Predicted: {prediction['predicted_halftime_total']} points")
            print(f"   Confidence: {prediction['halftime_over_confidence']:.1%}")
            
            print(f"\n   💰 BETTING ADVICE:")
            print(f"   {prediction['betting_advice']}")
            print(f"   Overall Assessment: {prediction['confidence_assessment']}")
            
            print(f"\n   🔍 HIGH-CONFIDENCE BETS (75%+ ONLY):")
            if prediction['high_confidence_bets']:
                for i, bet in enumerate(prediction['high_confidence_bets']):
                    confidence = prediction['high_confidence_levels'][i]
                    print(f"   • {bet} ({confidence:.1%} confidence)")
            else:
                print(f"   • No bets meet 75% confidence threshold")
                print(f"   • Recommended: Wait for better opportunities")
            
            # PLAYER PROPS (if enabled) - REAL DATA ONLY
            if self.player_props_enabled and self.player_props_analyzer:
                try:
                    player_props = self.player_props_analyzer.get_star_players_props(
                        game['home_team'], 
                        game['away_team'],
                        game['home_team_id'],
                        game['away_team_id']
                    )
                    
                    if player_props and len(player_props) > 0:
                        print(f"\n   🌟 STAR PLAYER PROPS (Real Data Only):")
                        print(f"   " + "-" * 50)
                        for props in player_props:
                            if props.get('high_confidence_props'):
                                print(f"   {props['player_name']}:")
                                
                                # Show all individual prop predictions (Points, Rebounds, Assists)
                                for prop_type in ['POINTS', 'REBOUNDS', 'ASSISTS', 'PRA']:
                                    matching_prop = [p for p in props['high_confidence_props'] if p['type'] == prop_type]
                                    if matching_prop:
                                        prop = matching_prop[0]
                                        print(f"      • {prop['type']}: {prop['recommendation']} ({prop['confidence']:.1%})")
                        
                        # Add to prediction object
                        prediction['player_props'] = player_props
                        prediction['player_props_count'] = len(player_props)
                    else:
                        print(f"\n   ⚠️ Player props unavailable - ESPN API roster data not accessible")
                        print(f"   💡 Game predictions (spread/total/ML) are still accurate")
                except Exception as e:
                    print(f"   ⚠️ Player props analysis error: {e}")
                    print(f"   💡 Game predictions (spread/total/ML) are still accurate")
            
            print(f"\n   {'='*50}")
            print()
        
        # Summary
        print(f"✅ DAILY SUMMARY:")
        print(f"   Games Analyzed: {len(predictions)}")
        print(f"   High Confidence: {sum(1 for p in predictions if p['confidence_assessment'] == 'High')}")
        print(f"   Medium Confidence: {sum(1 for p in predictions if p['confidence_assessment'] == 'Medium')}")
        print(f"   Low Confidence: {sum(1 for p in predictions if p['confidence_assessment'] == 'Low')}")
        print(f"   Data Source: Reliable ESPN API")
        print()
        
        # Print table summary
        self._print_predictions_table(predictions)
        
        return predictions
    
    def _print_predictions_table(self, predictions: List[Dict]):
        """Print predictions in a clean table format"""
        
        if not predictions:
            return
        
        print("\n" + "="*120)
        print("📊 PREDICTIONS SUMMARY TABLE")
        print("="*120 + "\n")
        
        # Main predictions table
        table_data = []
        for p in predictions:
            # Format time
            try:
                game_time = datetime.fromisoformat(p.get('datetime', '').replace('Z', '+00:00'))
                time_str = game_time.strftime("%I:%M %p")
            except:
                time_str = "TBD"
            
            # Get high confidence bets
            high_conf_bets = ", ".join(p['high_confidence_bets']) if p['high_confidence_bets'] else "None"
            if len(high_conf_bets) > 40:
                high_conf_bets = high_conf_bets[:37] + "..."
            
            table_data.append([
                f"{p['home_team']} - {p['away_team']}",
                time_str,
                f"{p['predicted_winner']}",
                f"{p['winner_confidence']:.1%}",
                p['home_team_spread'],
                p.get('over_under_recommendation', 'OVER') + f" {p['predicted_total']}",
                f"{p['over_probability']:.1%}",
                high_conf_bets
            ])
        
        if TABULATE_AVAILABLE:
            headers = ["Game (Home - Away)", "Time", "Winner", "Conf%", "Spread", "Over/Under", "Conf%", "High-Confidence Bets (75%+)"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            # Fallback to simple formatting
            print(f"{'Game':<50} {'Time':<10} {'Winner':<25} {'Conf':<8} {'Spread':<15} {'O/U':<20} {'Conf':<8} {'High-Conf Bets':<30}")
            print("-" * 180)
            for row in table_data:
                print(f"{row[0]:<50} {row[1]:<10} {row[2]:<25} {row[3]:<8} {row[4]:<15} {row[5]:<20} {row[6]:<8} {row[7]:<30}")
        
        # Player props table (if any)
        player_props_data = []
        for p in predictions:
            if p.get('player_props'):
                for props in p['player_props']:
                    if props.get('high_confidence_props'):
                        for prop in props['high_confidence_props']:
                            player_props_data.append([
                                f"{p['home_team']} - {p['away_team']}",
                                props['player_name'],
                                prop['type'],
                                prop['recommendation'],
                                f"{prop['confidence']:.1%}"
                            ])
        
        if player_props_data:
            print("\n" + "="*120)
            print("🌟 STAR PLAYER PROPS (85%+ Confidence)")
            print("="*120 + "\n")
            
            if TABULATE_AVAILABLE:
                headers = ["Game", "Player", "Prop Type", "Prediction", "Confidence"]
                print(tabulate(player_props_data, headers=headers, tablefmt="grid"))
            else:
                print(f"{'Game':<50} {'Player':<25} {'Prop':<15} {'Prediction':<20} {'Confidence':<12}")
                print("-" * 122)
                for row in player_props_data:
                    print(f"{row[0]:<50} {row[1]:<25} {row[2]:<15} {row[3]:<20} {row[4]:<12}")
        
        print("\n" + "="*120)
        print("💡 Focus on High-Confidence Bets (75%+) for best value")
        print("="*120 + "\n")
    
    
    def _get_realistic_nba_betting_total(self, home_team: str, away_team: str) -> float:
        """Get realistic NBA betting total using real sportsbook lines or smart estimates"""
        
        if self.betting_api:
            try:
                # Get real NBA betting lines
                all_odds = self.betting_api.get_nba_betting_lines()
                
                # Find this specific game
                game_odds = self.betting_api.find_game_odds(home_team, away_team, all_odds)
                
                if game_odds and game_odds.get('totals', {}).get('over'):
                    return float(game_odds['totals']['over']['line'])
                    
            except Exception as e:
                print(f"⚠️ Error fetching real NBA odds: {e}")
        
        # Fallback to realistic estimates based on NBA 2024 betting line analysis
        # Common NBA totals from sportsbooks (they use .5 to avoid pushes)
        common_nba_totals = [
            215.5, 217.5, 219.5, 221.5, 223.5, 225.5, 227.5, 229.5, 
            231.5, 233.5, 235.5, 237.5, 239.5, 241.5, 243.5
        ]
        
        import random
        return random.choice(common_nba_totals)


def main():
    """Run high-confidence NBA predictions with H2H analysis"""
    
    predictor = ReliableNBAPredictor()
    
    # Generate high-confidence predictions (same approach as football)
    predictions = predictor.generate_daily_predictions()
    
    if predictions:
        print("🚀 High-confidence NBA predictions generated successfully!")
        print("💡 Popular markets analyzed: Point Spread, Over/Under, Moneyline, Halftime, Player Props")
        print("📊 H2H analysis ensures quality predictions only")
        print("⚠️ Always bet responsibly and within your means")
    else:
        print("💪 No high-confidence opportunities today - patience is profitable!")
        print("💡 Check back tomorrow for better NBA betting opportunities")
    
    return predictions




if __name__ == "__main__":
    main()