# -*- coding: utf-8 -*-
"""
Quick NBA Predictions Table - Shows ONLY the table (no detailed output)
REAL DATA ONLY - No mock data
"""

import sys
import os

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

def main():
    """Generate NBA predictions and display ONLY the table"""
    
    print("Fetching NBA games and generating predictions...")
    print("(This may take 2-3 minutes for 17 games)")
    print()
    
    # Initialize predictor (suppress detailed output)
    import io
    import contextlib
    
    # Capture detailed output
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        predictor = ReliableNBAPredictor(
            enable_agentic_ai=True,
            enable_player_props=True
        )
        
        # Generate predictions
        predictions = predictor.generate_daily_predictions()
    
    # Now show ONLY the table
    print("\n" + "=" * 120)
    print("NBA PREDICTIONS - REAL DATA ONLY (No Mock Data)")
    print("=" * 120)
    print(f"Total Games Analyzed: {len(predictions)}")
    print(f"High-Confidence Bets (75%+): {sum(1 for p in predictions if len(p.get('high_confidence_bets', [])) > 0)}")
    print("=" * 120)
    
    # Call the table printing function directly
    if predictions:
        predictor._print_predictions_table(predictions)
    else:
        print("\n❌ No predictions available - ESPN API may be unavailable")
        print("Please try again in a few minutes")

if __name__ == "__main__":
    main()
