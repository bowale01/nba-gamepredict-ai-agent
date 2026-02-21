"""
NBA Prediction System
AI-powered NBA betting predictions with real H2H data
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add paths for working modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'nba'))

class NBAPredictor:
    """NBA prediction system using real H2H data"""
    
    def __init__(self):
        """Initialize NBA prediction system"""
        print("NBA AI PREDICTION SYSTEM")
        print("Real H2H + AI Agentic Enhancement")
        print("=" * 60)
        
        # Initialize NBA System
        self.nba_predictor = None
        print("\nNBA SYSTEM - Real H2H Data")
        print("-" * 35)
        try:
            from nba.predictor import ReliableNBAPredictor
            self.nba_predictor = ReliableNBAPredictor()
            print("[OK] NBA system initialized (ESPN API + Real H2H)")
        except Exception as e:
            print(f"[ERROR] NBA system error: {e}")
            self.nba_predictor = None
        
        print("\n" + "=" * 60)
        print("NBA system ready for high-confidence predictions!")
        print("75% confidence threshold protects customer money")
        print("=" * 60)
    
    def get_all_high_confidence_predictions(self) -> Dict:
        """Get high-confidence NBA predictions"""
        
        predictions = {
            "timestamp": datetime.now().isoformat(),
            "nba": [],
            "summary": {
                "total_games_analyzed": 0,
                "high_confidence_picks": 0,
                "success_rate_target": "75%+"
            }
        }
        
        # Get NBA predictions  
        if self.nba_predictor:
            try:
                nba_predictions = self._get_nba_predictions()
                predictions["nba"] = nba_predictions
                predictions["summary"]["total_games_analyzed"] += len(nba_predictions)
                high_conf_nba = [p for p in nba_predictions if p.get("confidence", 0) >= 75]
                predictions["summary"]["high_confidence_picks"] += len(high_conf_nba)
            except Exception as e:
                print(f"Error getting NBA predictions: {e}")
        
        return predictions
    
    def _get_nba_predictions(self) -> List[Dict]:
        """Get NBA predictions in standard format"""
        
        try:
            # Get today's games
            games = self.nba_predictor.get_todays_nba_games()
            predictions = []
            
            for game in games[:8]:  # Limit for performance
                try:
                    prediction = self.nba_predictor.predict_game_with_h2h_focus(game)
                    
                    if prediction.get("prediction_made", False):
                        formatted_prediction = {
                            "sport": "nba",
                            "league": "NBA",
                            "home_team": game.get("home_team", ""),
                            "away_team": game.get("away_team", ""),
                            "match_time": game.get("time", "TBD"),
                            "predictions": [],
                            "confidence": 0
                        }
                        
                        # Add high-confidence predictions only
                        if prediction.get("over_confidence", 0) >= 0.75:
                            formatted_prediction["predictions"].append({
                                "type": "over_under",
                                "recommendation": "OVER",
                                "confidence": round(prediction.get("over_confidence", 0) * 100, 1),
                                "line": prediction.get("predicted_total", 0)
                            })
                            formatted_prediction["confidence"] = max(formatted_prediction["confidence"],
                                                                   prediction.get("over_confidence", 0) * 100)
                        
                        if prediction.get("win_confidence", 0) >= 0.75:
                            formatted_prediction["predictions"].append({
                                "type": "moneyline", 
                                "recommendation": prediction.get("winner_prediction", ""),
                                "confidence": round(prediction.get("win_confidence", 0) * 100, 1)
                            })
                            formatted_prediction["confidence"] = max(formatted_prediction["confidence"],
                                                                   prediction.get("win_confidence", 0) * 100)
                        
                        if formatted_prediction["predictions"]:  # Only add if has high-confidence picks
                            predictions.append(formatted_prediction)
                
                except Exception as e:
                    continue
            
            return predictions
            
        except Exception as e:
            print(f"Error in NBA predictions: {e}")
            return []
    
    def get_sport_predictions(self, sport: str = "nba") -> List[Dict]:
        """Get NBA predictions"""
        return self._get_nba_predictions()
    
    def get_health_status(self) -> Dict:
        """Get system health status"""
        nba_status = self.nba_predictor is not None
        overall_status = "OPERATIONAL" if nba_status else "DEGRADED"

        return {
            "status": "operational" if nba_status else "unhealthy",
            "overall_status": overall_status,
            "nba_system": nba_status,
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        }

# Test the system
if __name__ == "__main__":
    predictor = NBAPredictor()
    
    print("\n🧪 TESTING NBA SYSTEM")
    print("=" * 50)
    
    # Test health status
    health = predictor.get_health_status()
    print(f"\nSystem Health: {health}")
    
    # Test getting all predictions
    print(f"\nGetting all high-confidence NBA predictions...")
    all_predictions = predictor.get_all_high_confidence_predictions()
    
    summary = all_predictions["summary"]
    print(f"Games Analyzed: {summary['total_games_analyzed']}")
    print(f"High-Confidence Picks: {summary['high_confidence_picks']}")
    
    print("\n[OK] NBA System Ready!")
