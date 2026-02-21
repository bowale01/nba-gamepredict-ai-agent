"""
NBA PREDICTION CONFIDENCE BREAKDOWN
====================================

IMPORTANT: Each game has MULTIPLE predictions, each with its OWN confidence level!
"""

# ============================================================================
# EXAMPLE: BOSTON CELTICS vs BROOKLYN NETS
# ============================================================================

game_predictions = {
    # 1. WINNER PREDICTION (Moneyline)
    "winner": {
        "prediction": "Boston Celtics",
        "confidence": 78.2,  # ← This is WINNER confidence only
        "home_probability": 78.2,
        "away_probability": 21.8,
        "meets_threshold": True  # ✅ 78.2% >= 75%
    },
    
    # 2. TOTAL POINTS PREDICTION (Over/Under)
    "total_points": {
        "predicted_total": 228.4,
        "recommendation": "OVER",
        "over_confidence": 60.0,  # ← This is OVER/UNDER confidence
        "under_confidence": 40.0,
        "meets_threshold": False  # ❌ 60% < 75%
    },
    
    # 3. HALFTIME OVER/UNDER
    "halftime": {
        "predicted_halftime_total": 109.6,
        "halftime_over_confidence": 55.0,  # ← This is HALFTIME confidence
        "meets_threshold": False  # ❌ 55% < 75%
    }
}

"""
SO WHEN WE SAY:
===============
"Boston Celtics to Win (78.2% confidence)" 
    → This is ONLY the confidence for WINNER prediction

"OVER 228.4 points (60% confidence)"
    → This is ONLY the confidence for TOTAL POINTS prediction
"""

# ============================================================================
# TODAY'S 9 GAMES BREAKDOWN
# ============================================================================

all_games_analysis = [
    {
        "game": "Pacers @ Cavaliers",
        "winner_prediction": {"team": "Cavaliers", "confidence": 65.3},  # ❌ Below 75%
        "total_prediction": {"play": "OVER", "confidence": 66.0},         # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    },
    
    {
        "game": "Nets @ Celtics",
        "winner_prediction": {"team": "Celtics", "confidence": 78.2},    # ✅ Above 75%
        "total_prediction": {"play": "OVER", "confidence": 60.0},         # ❌ Below 75%
        "high_confidence_bets": ["Celtics to Win (78.2%)"]  # Only winner qualifies
    },
    
    {
        "game": "Wizards @ Raptors",
        "winner_prediction": {"team": "Raptors", "confidence": 70.6},    # ❌ Below 75%
        "total_prediction": {"play": "UNDER", "confidence": 52.0},        # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    },
    
    {
        "game": "Heat @ Bulls",
        "winner_prediction": {"team": "Heat", "confidence": 50.3},       # ❌ Below 75%
        "total_prediction": {"play": "UNDER", "confidence": 58.0},        # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    },
    
    {
        "game": "Pelicans @ Mavericks",
        "winner_prediction": {"team": "Mavericks", "confidence": 51.8},  # ❌ Below 75%
        "total_prediction": {"play": "OVER", "confidence": 60.0},         # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    },
    
    {
        "game": "Timberwolves @ Suns",
        "winner_prediction": {"team": "Suns", "confidence": 77.7},       # ✅ Above 75%
        "total_prediction": {"play": "OVER", "confidence": 60.0},         # ❌ Below 75%
        "high_confidence_bets": ["Suns to Win (77.7%)"]  # Only winner qualifies
    },
    
    {
        "game": "Nuggets @ Rockets",
        "winner_prediction": {"team": "Nuggets", "confidence": 57.8},    # ❌ Below 75%
        "total_prediction": {"play": "UNDER", "confidence": 52.0},        # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    },
    
    {
        "game": "Thunder @ Jazz",
        "winner_prediction": {"team": "Jazz", "confidence": 57.3},       # ❌ Below 75%
        "total_prediction": {"play": "OVER", "confidence": 54.0},         # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    },
    
    {
        "game": "Trail Blazers @ Warriors",
        "winner_prediction": {"team": "Trail Blazers", "confidence": 51.1},  # ❌ Below 75%
        "total_prediction": {"play": "OVER", "confidence": 66.0},             # ❌ Below 75%
        "high_confidence_bets": []  # None meet threshold
    }
]

# ============================================================================
# SUMMARY OF TODAY'S PREDICTIONS
# ============================================================================

summary = {
    "total_games": 9,
    "total_possible_bets": 9 * 2,  # Each game has 2 main bets: Winner + Total
    
    # Winner predictions
    "winner_predictions": {
        "above_75%": 2,  # Celtics (78.2%), Suns (77.7%)
        "below_75%": 7,  # All other games
        "pass_rate": "22%"
    },
    
    # Total points predictions
    "total_predictions": {
        "above_75%": 0,   # NONE met threshold
        "below_75%": 9,   # All games below 75%
        "pass_rate": "0%"
    },
    
    # Overall
    "high_confidence_bets": 2,      # Only 2 winner bets qualified
    "low_confidence_bets": 16,      # 7 winners + 9 totals rejected
    "recommendation": "Only bet on Celtics and Suns to win"
}

"""
KEY INSIGHT:
============
When you see "Games Analyzed: 9, High Confidence: 2"

This means:
- 9 games were analyzed
- Each game has multiple bet types (winner, total, halftime)
- Only 2 BET TYPES across all games met 75% threshold
- Both were WINNER predictions (Celtics 78.2%, Suns 77.7%)
- ZERO total points predictions met threshold

The confidence shown is SPECIFIC to that prediction type:
✅ "Celtics to Win 78.2%" = Winner confidence
✅ "OVER 228.4 (60%)" = Total points confidence (different!)

AI Agent evaluated:
- 9 winner predictions → 2 passed (22%)
- 9 total predictions → 0 passed (0%)
- 9 halftime predictions → 0 passed (0%)
= Total: 2 of 27 possible bets recommended (7.4%)
"""

# ============================================================================
# HOW CONFIDENCE IS CALCULATED FOR EACH TYPE
# ============================================================================

celtics_vs_nets_detailed = {
    "h2h_data": {
        "games": 10,
        "celtics_wins": 8,
        "nets_wins": 2,
        "avg_total": 225.4,
        "over_games": 6,
        "under_games": 4
    },
    
    "calculations": {
        # WINNER CONFIDENCE (separate calculation)
        "winner": {
            "h2h_win_rate": 8 / 10,  # 80%
            "statistical_win_rate": 0.70,  # 70% from season stats
            "combined": (0.80 * 0.6) + (0.70 * 0.4),  # = 0.76
            "adjusted": 0.76 * 0.9 * 1.0,  # Data quality × Pattern clarity
            "final_confidence": 78.2  # ← WINNER confidence
        },
        
        # TOTAL POINTS CONFIDENCE (separate calculation)
        "total_points": {
            "h2h_over_rate": 6 / 10,  # 60%
            "statistical_over_rate": 0.55,  # 55% from season stats
            "combined": (0.60 * 0.6) + (0.55 * 0.4),  # = 0.58
            "adjusted": 0.58 * 0.9 * 0.7,  # Lower pattern clarity
            "final_confidence": 60.0  # ← TOTAL confidence (different!)
        }
    }
}

"""
FINAL ANSWER:
=============

When we say a game was "analyzed" we evaluate MULTIPLE predictions:

1. Winner Prediction → Has its own confidence (e.g., 78.2%)
2. Total Points → Has its own confidence (e.g., 60%)
3. Halftime Total → Has its own confidence (e.g., 55%)

The "High Confidence: 2" means:
→ 2 INDIVIDUAL PREDICTIONS (not games) met 75% threshold
→ Both happened to be winner predictions
→ None of the total points predictions met threshold

So today:
✅ 2 winner bets recommended (Celtics, Suns)
❌ 0 total points bets recommended
❌ 0 halftime bets recommended

Each confidence level is calculated independently based on H2H patterns
for THAT SPECIFIC bet type!
"""
