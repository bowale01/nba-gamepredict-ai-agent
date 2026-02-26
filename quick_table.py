#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick table view of predictions"""
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

try:
    with open('predictions_cache.json', 'r') as f:
        cache = json.load(f)
    predictions = cache['predictions']
    
    print("=" * 150)
    print(f"🏀 NBA PREDICTIONS - {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print("=" * 150)
    print()
    
    # Main table
    table_data = []
    for i, p in enumerate(predictions, 1):
        time_str = p.get('game_time', 'TBD')
        if time_str != 'TBD':
            try:
                dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                time_display = dt.strftime('%I:%M %p')
            except:
                time_display = time_str
        else:
            time_display = 'TBD'
        
        high_conf = '✅ YES' if p.get('high_confidence_bets') else '—'
        
        table_data.append([
            i,
            f"{p['home_team']} - {p['away_team']}",
            time_display,
            p.get('predicted_winner', 'N/A'),
            f"{p.get('winner_confidence', 0)*100:.1f}%",
            f"{p.get('over_under_recommendation', 'N/A')} {p.get('predicted_total', 0):.1f}",
            f"{p.get('ou_confidence', 0)*100:.1f}%",
            high_conf
        ])
    
    headers = ['#', 'Game (Home - Away)', 'Time', 'Predicted Winner', 'Conf%', 'Over/Under', 'Conf%', '75%+ Bet']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    print()
    
    # High-confidence bets
    print("=" * 150)
    print("🎯 HIGH-CONFIDENCE BETS (75%+)")
    print("=" * 150)
    print()
    
    hc_bets = []
    for p in predictions:
        if p.get('high_confidence_bets'):
            for bet in p['high_confidence_bets']:
                time_str = p.get('game_time', 'TBD')
                if time_str != 'TBD':
                    try:
                        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                        time_display = dt.strftime('%I:%M %p EST')
                    except:
                        time_display = time_str
                else:
                    time_display = 'TBD'
                
                conf = p.get('winner_confidence', 0) * 100 if 'Win' in bet else p.get('ou_confidence', 0) * 100
                hc_bets.append([
                    f"{p['home_team']} - {p['away_team']}",
                    time_display,
                    bet,
                    f"{conf:.1f}%"
                ])
    
    if hc_bets:
        print(tabulate(hc_bets, headers=['Game', 'Time', 'Recommended Bet', 'Confidence'], tablefmt='grid'))
        print()
        print(f"✅ Total: {len(hc_bets)} high-confidence bets")
    else:
        print("⚠️  No bets meet 75% confidence threshold")
    
    print()
    print("=" * 150)
    print("⚠️ IMPORTANT: Moneyline bets INCLUDE overtime - winner by final score")
    print("=" * 150)
    
except FileNotFoundError:
    print("❌ No predictions cache found. Run: python get_today_nba_predictions.py")
except Exception as e:
    print(f"❌ Error: {e}")
