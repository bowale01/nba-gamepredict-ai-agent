# -*- coding: utf-8 -*-
"""
Quick NBA Predictions Table - Shows predictions in table format
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
    """Generate NBA predictions and display in table format"""
    
    print("=" * 80)
    print("NBA PREDICTIONS - 48 HOUR WINDOW (Today + Tomorrow)")
    print("=" * 80)
    print()
    
    # Initialize predictor
    predictor = ReliableNBAPredictor(
        enable_agentic_ai=True,
        enable_player_props=True
    )
    
    # Generate predictions
    predictions = predictor.generate_daily_predictions()
    
    print("\n" + "=" * 80)
    print(f"Total predictions generated: {len(predictions)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
