# -*- coding: utf-8 -*-
"""
Validate Predictions Against Actual Results
Checks accuracy of our high-confidence predictions
"""

import sys
import os
import json
from datetime import datetime, timedelta
import requests

# Set UTF-8 encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def get_completed_games(date_str):
    """Fetch completed games from ESPN for a specific date"""
    try:
        url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={date_str}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            games = []
            
            if 'events' in data:
                for event in data['events']:
                    competition = event.get('competitions', [{}])[0]
                    status = competition.get('status', {})
                    
                    # Only get completed games
                    if status.get('type', {}).get('completed', False):
                        competitors = competition.get('competitors', [])
                        
                        if len(competitors) == 2:
                            home_team = next((c for c in competitors if c.get('homeAway') == 'home'), None)
                            away_team = next((c for c in competitors if c.get('homeAway') == 'away'), None)
                            
                            if home_team and away_team:
                                home_score = int(home_team.get('score', 0))
                                away_score = int(away_team.get('score', 0))
                                
                                # Check for overtime
                                periods = competition.get('status', {}).get('period', 4)
                                went_to_ot = periods > 4
                                ot_count = periods - 4 if went_to_ot else 0
                                
                                game_info = {
                                    'home_team': home_team.get('team', {}).get('displayName', 'Unknown'),
                                    'away_team': away_team.get('team', {}).get('displayName', 'Unknown'),
                                    'home_score': home_score,
                                    'away_score': away_score,
                                    'total_points': home_score + away_score,
                                    'winner': home_team.get('team', {}).get('displayName') if home_score > away_score else away_team.get('team', {}).get('displayName'),
                                    'margin': abs(home_score - away_score),
                                    'went_to_ot': went_to_ot,
                                    'ot_count': ot_count
                                }
                                games.append(game_info)
            
            return games
        else:
            print(f"⚠️ Could not fetch games for {date_str}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching completed games: {e}")
        return []

def load_predictions():
    """Load our cached predictions"""
    try:
        if os.path.exists('predictions_cache.json'):
            with open('predictions_cache.json', 'r') as f:
                cache = json.load(f)
                return cache.get('predictions', [])
    except:
        pass
    return []

def validate_predictions():
    """Validate our predictions against actual results"""
    
    print("=" * 100)
    print("🎯 PREDICTION VALIDATION - Checking Accuracy")
    print("=" * 100)
    print()
    
    # Get yesterday's date (games we predicted)
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y%m%d')
    
    print(f"📅 Checking games from: {yesterday.strftime('%B %d, %Y')}")
    print()
    
    # Fetch actual results
    print("📡 Fetching actual game results from ESPN...")
    actual_games = get_completed_games(date_str)
    
    if not actual_games:
        print("❌ No completed games found for yesterday")
        print("💡 Games might not be finished yet or ESPN API unavailable")
        return
    
    print(f"✅ Found {len(actual_games)} completed games")
    print()
    
    # Load our predictions
    predictions = load_predictions()
    
    if not predictions:
        print("⚠️ No cached predictions found")
        print("💡 Run get_today_nba_predictions.py first to generate predictions")
        return
    
    print(f"📊 Loaded {len(predictions)} predictions from cache")
    print()
    
    # Match predictions with actual results
    print("=" * 100)
    print("🔍 VALIDATION RESULTS")
    print("=" * 100)
    print()
    
    correct_predictions = 0
    total_high_conf_predictions = 0
    
    for actual in actual_games:
        # Find matching prediction
        pred = None
        for p in predictions:
            if (p.get('home_team') == actual['home_team'] and 
                p.get('away_team') == actual['away_team']):
                pred = p
                break
        
        if not pred:
            continue
        
        # Check if we had high-confidence predictions for this game
        high_conf_bets = pred.get('high_confidence_bets', [])
        
        if not high_conf_bets:
            continue
        
        print(f"🏀 {actual['home_team']} vs {actual['away_team']}")
        print(f"   Final Score: {actual['home_team']} {actual['home_score']} - {actual['away_score']} {actual['away_team']}")
        if actual.get('went_to_ot'):
            ot_text = "OT" if actual['ot_count'] == 1 else f"{actual['ot_count']}OT"
            print(f"   ⚠️  Game went to {ot_text} - Moneyline bets include overtime")
        print(f"   Total Points: {actual['total_points']}")
        print(f"   Winner: {actual['winner']}")
        print()
        
        # Check each high-confidence bet
        for bet in high_conf_bets:
            total_high_conf_predictions += 1
            
            # Check moneyline predictions
            if "to Win" in bet:
                predicted_winner = bet.replace(" to Win", "")
                if predicted_winner == actual['winner']:
                    ot_note = " (includes OT)" if actual.get('went_to_ot') else ""
                    print(f"   ✅ CORRECT: {bet}{ot_note}")
                    print(f"      Predicted: {predicted_winner} | Actual: {actual['winner']}")
                    correct_predictions += 1
                else:
                    ot_note = " (includes OT)" if actual.get('went_to_ot') else ""
                    print(f"   ❌ INCORRECT: {bet}{ot_note}")
                    print(f"      Predicted: {predicted_winner} | Actual: {actual['winner']}")
            
            # Check over/under predictions
            elif "OVER" in bet or "UNDER" in bet:
                if "OVER" in bet:
                    predicted_total = float(bet.split("OVER ")[1].split(" ")[0])
                    if actual['total_points'] > predicted_total:
                        print(f"   ✅ CORRECT: {bet}")
                        print(f"      Predicted: OVER {predicted_total} | Actual: {actual['total_points']}")
                        correct_predictions += 1
                    else:
                        print(f"   ❌ INCORRECT: {bet}")
                        print(f"      Predicted: OVER {predicted_total} | Actual: {actual['total_points']}")
                
                elif "UNDER" in bet:
                    predicted_total = float(bet.split("UNDER ")[1].split(" ")[0])
                    if actual['total_points'] < predicted_total:
                        print(f"   ✅ CORRECT: {bet}")
                        print(f"      Predicted: UNDER {predicted_total} | Actual: {actual['total_points']}")
                        correct_predictions += 1
                    else:
                        print(f"   ❌ INCORRECT: {bet}")
                        print(f"      Predicted: UNDER {predicted_total} | Actual: {actual['total_points']}")
            
            # Check halftime predictions
            elif "Halftime" in bet:
                print(f"   ⏭️  SKIPPED: {bet} (halftime data not available)")
            
            print()
        
        print("-" * 100)
        print()
    
    # Summary
    print("=" * 100)
    print("📊 ACCURACY SUMMARY")
    print("=" * 100)
    print()
    
    if total_high_conf_predictions > 0:
        accuracy = (correct_predictions / total_high_conf_predictions) * 100
        
        print(f"Total High-Confidence Predictions: {total_high_conf_predictions}")
        print(f"Correct Predictions: {correct_predictions}")
        print(f"Incorrect Predictions: {total_high_conf_predictions - correct_predictions}")
        print()
        print(f"🎯 ACCURACY: {accuracy:.1f}%")
        print()
        
        if accuracy >= 75:
            print("✅ EXCELLENT! System is performing above 75% threshold")
        elif accuracy >= 60:
            print("✅ GOOD! System is performing well")
        elif accuracy >= 50:
            print("⚠️  FAIR - System needs improvement")
        else:
            print("❌ POOR - System needs significant improvement")
    else:
        print("⚠️ No high-confidence predictions to validate")
        print("💡 System correctly avoided making predictions when confidence was low")
    
    print()
    print("=" * 100)
    print("💡 Note: This validation only checks high-confidence bets (75%+)")
    print("   The system protects your capital by rejecting low-confidence predictions")
    print("=" * 100)

if __name__ == "__main__":
    validate_predictions()
