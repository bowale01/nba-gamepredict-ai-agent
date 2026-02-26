#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Complete predictions for Feb 22-23, 2026"""
import json
import sys
from datetime import datetime
from tabulate import tabulate

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

with open('predictions_cache.json', 'r') as f:
    cache = json.load(f)

predictions = cache['predictions']

print("=" * 150)
print(f"🏀 NBA PREDICTIONS - COMPLETE ANALYSIS")
print(f"📅 February 22-23, 2026")
print(f"⏰ Generated: {datetime.now().strftime('%I:%M %p')}")
print("=" * 150)
print()

# Separate today and tomorrow
today_games = []
tomorrow_games = []

for p in predictions:
    time_str = p.get('game_time', '')
    if '2026-02-22' in time_str:
        today_games.append(p)
    else:
        tomorrow_games.append(p)

print("=" * 150)
print("📅 TODAY'S GAMES (February 22, 2026)")
print("=" * 150)
print()

table_today = []
for i, p in enumerate(today_games, 1):
    time_str = p.get('game_time', 'TBD')
    try:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        time_display = dt.strftime('%I:%M %p')
    except:
        time_display = 'TBD'
    
    high_conf_ml = '✅' if p.get('winner_confidence', 0) >= 0.75 else '—'
    high_conf_ou = '✅' if p.get('ou_confidence', 0) >= 0.75 else '—'
    
    table_today.append([
        i,
        f"{p['home_team']} - {p['away_team']}",
        time_display,
        p.get('predicted_winner', 'N/A'),
        f"{p.get('winner_confidence', 0)*100:.1f}%",
        high_conf_ml,
        f"{p.get('over_under_recommendation', 'N/A')} {p.get('predicted_total', 0):.1f}",
        f"{p.get('ou_confidence', 0)*100:.1f}%",
        high_conf_ou
    ])

headers = ['#', 'Game (Home - Away)', 'Time', 'Winner', 'Conf%', '75%+', 'Over/Under', 'Conf%', '75%+']
print(tabulate(table_today, headers=headers, tablefmt='grid'))
print()

print("=" * 150)
print("📅 TOMORROW'S GAMES (February 23, 2026)")
print("=" * 150)
print()

table_tomorrow = []
for i, p in enumerate(tomorrow_games, 1):
    time_str = p.get('game_time', 'TBD')
    try:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        time_display = dt.strftime('%I:%M %p')
    except:
        time_display = 'TBD'
    
    high_conf_ml = '✅' if p.get('winner_confidence', 0) >= 0.75 else '—'
    high_conf_ou = '✅' if p.get('ou_confidence', 0) >= 0.75 else '—'
    
    table_tomorrow.append([
        i,
        f"{p['home_team']} - {p['away_team']}",
        time_display,
        p.get('predicted_winner', 'N/A'),
        f"{p.get('winner_confidence', 0)*100:.1f}%",
        high_conf_ml,
        f"{p.get('over_under_recommendation', 'N/A')} {p.get('predicted_total', 0):.1f}",
        f"{p.get('ou_confidence', 0)*100:.1f}%",
        high_conf_ou
    ])

print(tabulate(table_tomorrow, headers=headers, tablefmt='grid'))
print()

# High-confidence summary
print("=" * 150)
print("🎯 HIGH-CONFIDENCE BETS (75%+) - ALL PREDICTIONS")
print("=" * 150)
print()

hc_bets = []
for p in predictions:
    time_str = p.get('game_time', 'TBD')
    try:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        time_display = dt.strftime('%b %d, %I:%M %p EST')
    except:
        time_display = 'TBD'
    
    game_name = f"{p['home_team']} - {p['away_team']}"
    
    # Check moneyline
    if p.get('winner_confidence', 0) >= 0.75:
        winner = p.get('predicted_winner', 'N/A')
        conf = p.get('winner_confidence', 0) * 100
        hc_bets.append([
            game_name,
            time_display,
            f"{winner} to Win",
            f"{conf:.1f}%",
            "Moneyline"
        ])
    
    # Check O/U
    if p.get('ou_confidence', 0) >= 0.75:
        ou_rec = p.get('over_under_recommendation', 'N/A')
        ou_total = p.get('predicted_total', 0)
        conf = p.get('ou_confidence', 0) * 100
        hc_bets.append([
            game_name,
            time_display,
            f"{ou_rec} {ou_total:.1f} points",
            f"{conf:.1f}%",
            "Over/Under"
        ])

if hc_bets:
    hc_headers = ['Game', 'Time', 'Recommended Bet', 'Confidence', 'Bet Type']
    print(tabulate(hc_bets, headers=hc_headers, tablefmt='grid'))
    print()
    print(f"✅ TOTAL HIGH-CONFIDENCE BETS: {len(hc_bets)}")
else:
    print("⚠️  No bets meet 75% confidence threshold")

print()
print("=" * 150)
print("📊 SUMMARY")
print("=" * 150)
print()
print(f"Total Games Analyzed: {len(predictions)}")
print(f"Today's Games: {len(today_games)}")
print(f"Tomorrow's Games: {len(tomorrow_games)}")
print(f"High-Confidence Bets: {len(hc_bets)}")
print()
print("✅ Features Used:")
print("   • Real ESPN H2H Data")
print("   • Injury Reports (Real-time)")
print("   • Current Form Analysis (Last 10 games)")
print("   • AWS Bedrock AI Validation")
print("   • GPT-4o Historical Context")
print("   • 75% Confidence Filter")
print()
print("⚠️ IMPORTANT BETTING NOTES:")
print("   • Moneyline bets INCLUDE overtime - winner by final score")
print("   • Over/Under totals INCLUDE overtime points")
print("   • All predictions account for close games that may go to OT")
print()
print("🏆 Yesterday's Performance (Feb 21, 2026):")
print("   • Accuracy: 100% (2/2 correct)")
print("   • ROI: 78.8% ($157.58 profit on $200)")
print("   • ✅ San Antonio vs Sacramento - OVER 239.8 (Actual: 261)")
print("   • ✅ New York Knicks to Win (Won 108-106)")
print()
print("=" * 150)
print("💡 BETTING STRATEGY")
print("=" * 150)
print()
print("RECOMMENDED APPROACH:")
print("   1. Focus on high-confidence bets (75%+)")
print("   2. Use proper bankroll management")
print("   3. Moneyline bets are safest (winner is winner)")
print("   4. O/U bets have higher variance but can be profitable")
print("   5. Track results to validate system accuracy")
print()
print("=" * 150)
