# 🏀 NBA Overtime Betting Guide

## Understanding Overtime in NBA Betting

### What is Overtime?
In NBA basketball, if the score is tied at the end of regulation (48 minutes), the game goes to overtime. Each overtime period is 5 minutes long, and the game continues until there's a winner.

---

## 📊 How Overtime Affects Different Bet Types

### 1. Moneyline Bets (Winner) ✅ INCLUDES OT
**Our System:** All "Team to Win" predictions include overtime

- **What it means:** The bet is settled based on the FINAL score after all overtime periods
- **Example:** If we predict "Cleveland Cavaliers to Win" and they win 120-118 in OT, the bet WINS
- **Important:** Regulation score doesn't matter - only the final winner counts

**Why this matters for our predictions:**
- Our 79%+ confidence predictions account for close games
- H2H analysis includes overtime results from past games
- Form analysis considers teams' performance in clutch situations

---

### 2. Over/Under (Total Points) ✅ INCLUDES OT
**Our System:** All O/U predictions include overtime points

- **What it means:** ALL points scored in overtime are added to the total
- **Example:** If we predict OVER 225.3 and the game ends 115-113 in regulation (228 total), it's OVER even before OT
- **Example 2:** If regulation ends 110-110 (220) and OT adds 12 points (232 total), OVER 225.3 WINS

**Why this matters for our predictions:**
- Close games that go to OT typically push totals OVER
- Our system factors in competitive matchups that may extend
- Yesterday's San Antonio vs Sacramento went OVER 239.8 (actual: 261) - likely included OT

---

### 3. Point Spread ✅ INCLUDES OT
**Our System:** Spread predictions include overtime

- **What it means:** The final margin includes all overtime points
- **Example:** If spread is Cavaliers -3.5 and they win 120-115 in OT, they cover (5-point margin)
- **Important:** A team can lose in regulation but cover the spread in OT, or vice versa

---

## 🎯 How Our System Handles Overtime

### Prediction Methodology
1. **H2H Analysis:** Includes historical games that went to OT
2. **Form Analysis:** Considers teams' clutch performance
3. **Close Game Detection:** Identifies matchups likely to be tight
4. **Confidence Adjustment:** Lower confidence for games likely to go to OT (more variance)

### High-Confidence Bets (75%+)
- We only recommend bets where we're confident even with OT possibility
- Moneyline bets on strong teams are safer (winner is winner, regardless of OT)
- O/U bets in close games have higher variance due to OT potential

---

## 📈 Historical Examples

### Yesterday's Results (Feb 21, 2026)
✅ **New York Knicks to Win** - Won 108-106
- Very close game (2-point margin)
- Could have gone to OT if Sacramento made last shot
- Our prediction was CORRECT regardless

✅ **San Antonio vs Sacramento - OVER 239.8** - Actual: 261 points
- High total suggests possible OT or high-scoring game
- Actual total was 21.2 points over prediction
- Our prediction was CORRECT

---

## ⚠️ Important Notes for Bettors

### What You Need to Know
1. **Moneyline is safest:** Winner is winner, OT doesn't change the bet logic
2. **O/U has variance:** OT adds 10-20 points typically, can swing close totals
3. **Spread can flip:** A losing team in regulation can cover in OT
4. **Live betting changes:** Once OT starts, odds change dramatically

### Our System's Approach
- ✅ We account for OT in all predictions
- ✅ Historical data includes OT games
- ✅ Close matchups are flagged (lower confidence if needed)
- ✅ Moneyline bets are preferred for close games (less OT variance)

---

## 🔍 Validation Process

### How We Check Results
Our validation scripts (`check_yesterday_results.py` and `validate_predictions.py`) now:

1. **Detect overtime games:** Shows "(OT)" or "(2OT)" in results
2. **Include OT in totals:** All points counted
3. **Validate moneyline:** Winner after OT is the winner
4. **Note OT impact:** Flags when OT affected the outcome

### Example Output
```
✅ Cleveland Cavaliers 120 - 118 Oklahoma City Thunder (OT)
   Winner: Cleveland Cavaliers (OT)
   Total Points: 238
   ⚠️  Game went to overtime - Moneyline bets include OT
```

---

## 💡 Betting Strategy Tips

### For Moneyline Bets (Our Focus)
- ✅ **Best for close games:** Winner is winner, OT doesn't matter
- ✅ **High-confidence picks:** Our 75%+ threshold accounts for OT possibility
- ✅ **Less variance:** Compared to O/U or spread in close games

### For Over/Under Bets
- ⚠️ **Higher variance:** OT adds 10-20 points typically
- ⚠️ **Close totals risky:** If predicted total is near actual, OT can swing it
- ✅ **Clear OVER/UNDER:** If prediction is far from line, OT won't matter

### For Spread Bets
- ⚠️ **Most variance:** OT can completely flip the spread
- ⚠️ **Close spreads risky:** -3.5 or less can easily flip in OT
- ✅ **Large spreads safer:** -10 or more unlikely to flip in OT

---

## 📊 Today's Predictions (Feb 22-23, 2026)

### High-Confidence Moneyline Bets
All include overtime - winner by final score:

1. **Cleveland Cavaliers to Win** (79.0%) - Safe even if OT
2. **Boston Celtics to Win** (79.1%) - Safe even if OT
3. **LA Clippers to Win** (82.7%) - Safe even if OT

These predictions are confident enough that even if games go to OT, we expect these teams to win.

---

## 🎯 Summary

### Key Takeaways
1. ✅ All NBA bets include overtime (moneyline, O/U, spread)
2. ✅ Our system accounts for OT in predictions
3. ✅ Moneyline bets have least OT variance
4. ✅ Our 75%+ confidence threshold protects against OT uncertainty
5. ✅ Validation scripts now show OT information

### System Updates
- ✅ `check_yesterday_results.py` - Shows OT in results
- ✅ `validate_predictions.py` - Notes OT impact on validation
- ✅ `get_today_nba_predictions.py` - Includes OT betting notes
- ✅ `show_table.py` - Displays OT information

---

**Remember:** In NBA betting, overtime is part of the game. Our predictions are designed to be accurate regardless of whether games go to OT, which is why we focus on high-confidence moneyline bets where the winner is clear.
