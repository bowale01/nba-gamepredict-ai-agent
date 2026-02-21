"""
Get today's NBA predictions with full forecasts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from nba.predictor import ReliableNBAPredictor

def get_today_predictions():
    print("=" * 80)
    print(f"🏀 NBA PREDICTIONS - {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 80)
    
    predictor = ReliableNBAPredictor(enable_agentic_ai=False)
    
    # Get predictions
    predictions = predictor.generate_daily_predictions()
    
    if not predictions:
        print("\n❌ No predictions generated")
        return
    
    # Show all predictions
    print(f"\n{'='*80}")
    print(f"📊 ALL PREDICTIONS ({len(predictions)} total)")
    print(f"{'='*80}\n")
    
    for i, pred in enumerate(predictions, 1):
        print(f"\n{'='*80}")
        print(f"Game {i}: {pred['away_team']} @ {pred['home_team']}")
        print(f"{'='*80}")
        print(f"🎯 Prediction: {pred['prediction']}")
        print(f"📊 Confidence: {pred['confidence']:.1f}%")
        print(f"💰 Market: {pred.get('market_type', 'N/A')}")
        
        if 'recommended_line' in pred:
            print(f"📈 Line: {pred['recommended_line']}")
        
        print(f"\n📊 Analysis:")
        print(f"   H2H Matches: {pred.get('h2h_matches_used', 'N/A')}")
        print(f"   Avg Total: {pred.get('avg_total_points', 'N/A')}")
        print(f"   Recent Form: {pred.get('recent_form', 'N/A')}")
        
        if 'reasoning' in pred:
            print(f"\n💡 Reasoning:")
            reasoning = pred['reasoning']
            if isinstance(reasoning, str):
                for line in reasoning.split('\n'):
                    if line.strip():
                        print(f"   {line.strip()}")
    
    # Show high confidence only
    high_conf = [p for p in predictions if p['confidence'] >= 75]
    
    print(f"\n{'='*80}")
    print(f"🎯 HIGH CONFIDENCE PICKS (75%+)")
    print(f"{'='*80}\n")
    
    if high_conf:
        print(f"✅ Found {len(high_conf)} high-confidence picks:\n")
        for i, pred in enumerate(high_conf, 1):
            print(f"{i}. {pred['away_team']} @ {pred['home_team']}")
            print(f"   🎯 {pred['prediction']}")
            print(f"   📊 {pred['confidence']:.1f}% confidence")
            print(f"   💰 {pred.get('market_type', 'N/A')}")
            print()
    else:
        print("⚠️  No predictions meet 75% confidence threshold today")
        print("💡 Our AI Agent protects your capital by only recommending high-quality bets\n")

if __name__ == "__main__":
    get_today_predictions()
