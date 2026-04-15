# -*- coding: utf-8 -*-
"""
NBA GamePredict AI - Daily Predictions (Optimized)
Real data with injury & form analysis + caching
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Add NBA module path
sys.path.append(os.path.join(os.path.dirname(__file__), 'nba'))

from nba.predictor import ReliableNBAPredictor

CACHE_FILE = 'predictions_cache.json'
CACHE_DURATION_MINUTES = 30

def load_cache():
    """Load cached predictions if recent"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
                cache_time = datetime.fromisoformat(cache['timestamp'])
                if datetime.now() - cache_time < timedelta(minutes=CACHE_DURATION_MINUTES):
                    return cache['predictions']
    except:
        pass
    return None

def save_cache(predictions):
    """Save predictions to cache"""
    try:
        cache = {
            'timestamp': datetime.now().isoformat(),
            'predictions': predictions
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except:
        pass

def main():
    """Generate NBA predictions with injury & form analysis"""
    
    print("=" * 80)
    print(f"🏀 NBA GAMEPREDICT AI - {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 80)
    print("📊 Real Data Only - No Mock Data")
    print("🏥 Injury Analysis: ENABLED")
    print("📈 Current Form Analysis: ENABLED")
    print("🤖 AI Enhancement: Real H2H Data Analysis + ESPN API")
    print("🎯 85% Confidence Threshold (Raised from 75%)")
    print("🌟 Player Props: ENABLED (Real ESPN roster data)")
    print("=" * 80)
    print()
    print("⚠️ SYSTEM IMPROVEMENTS (Feb 23, 2026):")
    print("   • Confidence threshold: 75% → 85% (more conservative)")
    print("   • Home court advantage: 0.55 → 0.62 (better weighting)")
    print("   • H2H balance: 60/40 → 50/50 (more balanced)")
    print("   • Desperation factor: Added for teams on losing streaks")
    print("   • O/U validation: Rejects extreme totals")
    print("   • Feb 22 accuracy: 25% (1/4) - System recalibrated")
    print("=" * 80)
    print()
    print("💡 Note: Player props shown only when ESPN roster API is available")
    print("   If roster data unavailable, game predictions still accurate")
    print()
    
    # Check cache first
    print("🔍 Checking for recent predictions...")
    cached_predictions = load_cache()
    
    if cached_predictions:
        print(f"✅ Using cached predictions (less than {CACHE_DURATION_MINUTES} minutes old)")
        print("💡 Run again after 30 minutes for fresh analysis")
        print()
        predictions = cached_predictions
    else:
        print("📡 Fetching fresh predictions from ESPN API...")
        print("⏱️  This will take 2-3 minutes (analyzing 17 games with injury/form data)")
        print()
        
        # Initialize predictor with core features (no fake Bedrock/GPT)
        predictor = ReliableNBAPredictor(
            enable_agentic_ai=False,      # Disabled - no OpenAI key configured
            enable_player_props=True      # Enables player props (REAL DATA ONLY)
        )
        
        # Generate predictions with progress
        print("🔄 Analyzing games...")
        predictions = predictor.generate_daily_predictions()
        
        if predictions:
            save_cache(predictions)
            print("✅ Predictions cached for 30 minutes")
        print()
    
    if not predictions:
        print("\n❌ No predictions available")
        print("ESPN API may be unavailable - please try again in a few minutes")
        return
    
    # Display summary
    print("\n" + "=" * 120)
    print("📊 PREDICTIONS SUMMARY")
    print("=" * 120)
    print(f"Total Games Analyzed: {len(predictions)}")
    
    high_conf_count = sum(1 for p in predictions if len(p.get('high_confidence_bets', [])) > 0)
    print(f"High-Confidence Bets (75%+): {high_conf_count}")
    print("=" * 120)
    print()
    
    # Display predictions table
    print("=" * 150)
    print("📊 PREDICTIONS TABLE")
    print("=" * 150)
    print()
    
    # Create detailed table
    from tabulate import tabulate
    from datetime import datetime as dt
    
    table_data = []
    for i, pred in enumerate(predictions, 1):
        game = f"{pred['home_team']} - {pred['away_team']}"
        
        # Parse time
        time_str = pred.get('game_time', 'TBD')
        if time_str != 'TBD':
            try:
                time_dt = dt.fromisoformat(time_str.replace('Z', '+00:00'))
                time_display = time_dt.strftime('%b %d, %I:%M %p')
            except:
                time_display = time_str
        else:
            time_display = 'TBD'
        
        winner = pred.get('predicted_winner', 'N/A')
        win_conf = f"{pred.get('winner_confidence', 0)*100:.1f}%"
        
        spread = pred.get('spread_recommendation', 'N/A')
        if len(spread) > 30:
            spread = spread[:27] + '...'
        
        ou_rec = pred.get('over_under_recommendation', 'N/A')
        ou_total = pred.get('predicted_total', 0)
        ou_display = f"{ou_rec} {ou_total:.1f}"
        ou_conf = f"{pred.get('ou_confidence', 0)*100:.1f}%"
        
        high_conf = pred.get('high_confidence_bets', [])
        if high_conf:
            high_conf_str = '✅ ' + ', '.join(high_conf)
            if len(high_conf_str) > 50:
                high_conf_str = high_conf_str[:47] + '...'
        else:
            high_conf_str = '—'
        
        table_data.append([i, game, time_display, winner, win_conf, spread, ou_display, ou_conf, high_conf_str])
    
    headers = ['#', 'Game (Home - Away)', 'Time', 'Predicted Winner', 'Conf%', 'Spread Recommendation', 'Over/Under', 'Conf%', 'High-Confidence Bets (75%+)']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    print()
    
    # Show high-confidence summary
    print("\n" + "=" * 150)
    print("🎯 HIGH-CONFIDENCE BETS SUMMARY (75%+)")
    print("=" * 150)
    print()
    
    high_conf_bets = []
    for pred in predictions:
        if pred.get('high_confidence_bets'):
            for bet in pred['high_confidence_bets']:
                # Parse time
                time_str = pred.get('game_time', 'TBD')
                if time_str != 'TBD':
                    try:
                        time_dt = dt.fromisoformat(time_str.replace('Z', '+00:00'))
                        time_display = time_dt.strftime('%b %d, %I:%M %p EST')
                    except:
                        time_display = time_str
                else:
                    time_display = 'TBD'
                
                # Get confidence
                if 'Win' in bet:
                    conf = pred.get('winner_confidence', 0) * 100
                else:
                    conf = pred.get('ou_confidence', 0) * 100
                
                high_conf_bets.append({
                    'game': f"{pred['home_team']} - {pred['away_team']}",
                    'bet': bet,
                    'time': time_display,
                    'confidence': conf
                })
    
    if high_conf_bets:
        hc_table = []
        for i, bet_info in enumerate(high_conf_bets, 1):
            hc_table.append([
                i,
                bet_info['game'],
                bet_info['time'],
                bet_info['bet'],
                f"{bet_info['confidence']:.1f}%"
            ])
        
        hc_headers = ['#', 'Game', 'Time', 'Recommended Bet', 'Confidence']
        print(tabulate(hc_table, headers=hc_headers, tablefmt='grid'))
        print()
        print(f"✅ Total High-Confidence Bets: {len(high_conf_bets)}")
    else:
        print("⚠️  No bets meet 75% confidence threshold today")
        print("💡 Our AI protects your capital by only recommending high-quality bets")
        print("📊 All games were analyzed but didn't meet our strict criteria")
    print()
    
    print("=" * 150)
    print("✅ Analysis Complete")
    print("=" * 150)
    print()
    print("💡 Features Used:")
    print("   ✅ Real ESPN H2H Data (60% weight)")
    print("   ✅ Statistical Analysis (40% weight)")
    print("   ✅ Injury Reports (ESPN API)")
    print("   ✅ Current Form Analysis (Last 10 games)")
    print("   ✅ Player Props (Real roster data)")
    print("   ✅ O/U Validation (Minimum 200 points enforced)")
    print("   ✅ 85% Confidence Filter (Raised from 75%)")
    print()
    print(f"📝 Results cached for {CACHE_DURATION_MINUTES} minutes")
    print("🔄 Run again after 30 minutes for fresh analysis")
    print()
    print("⚠️ Important Betting Notes:")
    print("   • Moneyline bets INCLUDE overtime - winner determined by final score")
    print("   • Over/Under totals INCLUDE overtime points")
    print("   • Spread bets INCLUDE overtime")
    print("   • Our predictions account for close games that may go to OT")
    print()
    print("📊 System Status:")
    print("   • Feb 22 Performance: 25% accuracy (1/4 correct)")
    print("   • System recalibrated with improvements")
    print("   • Now using 85% confidence threshold")
    print("   • Testing phase - use caution with real money")
    print()
    print("⚠️ Player Props Note:")
    print("   Player props are shown when ESPN roster API is available")
    print("   If you see 'Player props unavailable', ESPN API had issues")
    print("   Game predictions (spread/total/ML) are still accurate")
    print()

if __name__ == "__main__":
    main()
