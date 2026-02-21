# 🧪 Testing Guide - NBA GamePredict AI

## 🏀 Testing with Tomorrow's NBA Games

### Current Status

**AWS Deployment:** ✅ Live and working
**Prediction Engine:** ⚠️ Placeholder logic in Lambda (needs enhancement)
**Local System:** ✅ Full prediction engine ready

---

## 🎯 Quick Test Options

### Option 1: Test AWS Health (30 seconds)

Your API is live! Test it:

```powershell
# Health check
curl https://yolx2fbppe.execute-api.us-east-1.amazonaws.com/prod/health
```

**Expected:** Status 200, "healthy" response

---

### Option 2: Test Local Predictions (5 minutes)

The local system has the full prediction engine:

#### Step 1: Check Tomorrow's Games
```powershell
python check_tomorrow_games.py
```

**What it does:**
- Fetches tomorrow's NBA schedule from ESPN API
- Shows all matchups
- Displays game times

#### Step 2: Get Predictions
```powershell
cd nba
python predictor.py
```

**What it does:**
- Analyzes each game with H2H data
- Validates with AI (if configured)
- Generates predictions for:
  - Moneyline (winner)
  - Over/Under (total points)
  - Point Spreads
  - Halftime predictions
  - Player Props
- Filters to 75%+ confidence only

**Example Output:**
```
🏀 NBA DAILY PREDICTIONS
========================================
📅 Date: Saturday, February 22, 2026

🎯 GAME 1: Warriors @ Lakers
   📍 Venue: Crypto.com Arena
   
   🏆 POINT SPREAD (MOST POPULAR):
   Lakers -5.5 (78% confidence)
   
   📊 OVER/UNDER TOTAL:
   Over 225.5 points (82% confidence)
   
   🏆 MONEYLINE (WINNER):
   Lakers to Win (76% confidence)
   
   💰 HIGH-CONFIDENCE BETS (75%+ ONLY):
   • Lakers -5.5 (78% confidence)
   • Over 225.5 (82% confidence)
   • Lakers to Win (76% confidence)
```

#### Step 3: Run Local API
```powershell
python api_service.py
```

Then test in another terminal:
```powershell
curl http://localhost:8000/daily-predictions
```

---

### Option 3: Test Specific Game (2 minutes)

Test a single matchup:

```powershell
# Example: Lakers vs Warriors
curl -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{"home_team":"Lakers","away_team":"Warriors"}'
```

---

## 🔧 Enhancing AWS Lambda (Optional)

To get full predictions from AWS, you need to:

### Step 1: Update Lambda Function

The current Lambda has placeholder logic. To add real predictions:

1. **Copy prediction logic** from `nba/predictor.py`
2. **Update** `aws/lambda/daily_predictions/handler.py`
3. **Add dependencies** to Lambda layer
4. **Redeploy**

### Step 2: Add Dependencies

Create `aws/lambda/daily_predictions/requirements.txt`:
```
requests==2.32.5
boto3==1.35.0
```

### Step 3: Rebuild and Deploy
```powershell
cd aws
python -m samcli build
python -m samcli deploy
```

**Time:** ~10 minutes
**Benefit:** Full predictions from AWS API

---

## 📊 What Each Test Shows

### Health Check Test
- ✅ API Gateway working
- ✅ Lambda function responding
- ✅ DynamoDB accessible
- ✅ Basic infrastructure operational

### Local Predictions Test
- ✅ ESPN API integration
- ✅ H2H data collection
- ✅ AI validation (if configured)
- ✅ Prediction algorithms
- ✅ Confidence filtering
- ✅ Multiple betting markets

### AWS Predictions Test (after enhancement)
- ✅ Serverless predictions
- ✅ Auto-scaling
- ✅ Production-ready
- ✅ Cost-optimized
- ✅ Global availability

---

## 🎯 Recommended Testing Flow

### For Tomorrow's Games:

**1. Quick Check (1 minute)**
```powershell
# See what games are tomorrow
python check_tomorrow_games.py
```

**2. Get Predictions (5 minutes)**
```powershell
# Run full prediction engine
cd nba
python predictor.py
```

**3. Review Results**
- Look for 75%+ confidence bets
- Check H2H analysis
- Review AI validation (if enabled)
- Note recommended stakes

**4. Test AWS Health (30 seconds)**
```powershell
# Verify AWS deployment is healthy
curl https://yolx2fbppe.execute-api.us-east-1.amazonaws.com/prod/health
```

---

## 📝 Example Test Session

```powershell
# 1. Check tomorrow's schedule
PS> python check_tomorrow_games.py
✅ Found 8 NBA games for tomorrow

# 2. Get predictions
PS> cd nba
PS> python predictor.py

🏀 NBA DAILY PREDICTIONS
========================
Games Analyzed: 8
High Confidence: 3

Game 1: Warriors @ Lakers
  Prediction: Lakers -5.5 (78% confidence)
  Recommendation: Bet 3% of bankroll

Game 2: Celtics @ Heat
  Prediction: Over 218.5 (81% confidence)
  Recommendation: Bet 4% of bankroll

# 3. Test AWS
PS> curl https://yolx2fbppe.execute-api.us-east-1.amazonaws.com/prod/health
✅ Status: healthy
```

---

## 🔍 Understanding the Output

### Confidence Levels
- **90%+**: Excellent - Strong recommendation
- **80-89%**: Good - Solid bet
- **75-79%**: Solid - Acceptable bet
- **<75%**: Rejected - Not shown to users

### Betting Markets
1. **Point Spread**: Most popular NBA bet
2. **Over/Under**: Total points prediction
3. **Moneyline**: Winner prediction
4. **Halftime**: First half predictions
5. **Player Props**: Individual player performance

### H2H Analysis
- **Games Analyzed**: Number of historical matchups
- **Win Pattern**: Historical dominance
- **Scoring Pattern**: Over/Under trends
- **AI Validation**: GPT-4o verification

---

## 💡 Tips for Testing

### 1. Best Time to Test
- **Morning**: Check tomorrow's schedule
- **Afternoon**: Run predictions (after lineups confirmed)
- **Evening**: Review and compare with sportsbooks

### 2. What to Look For
- ✅ High confidence (75%+)
- ✅ Multiple H2H games (4+)
- ✅ AI validation passed
- ✅ Clear betting edge

### 3. Red Flags
- ❌ Low H2H data (<4 games)
- ❌ Confidence below 75%
- ❌ AI validation questionable
- ❌ No clear edge

---

## 🚀 Next Steps

### After Testing Tomorrow's Games:

1. **Compare Predictions** with actual results
2. **Track Accuracy** over time
3. **Adjust Confidence** thresholds if needed
4. **Enhance AWS Lambda** for production use
5. **Add More Features** (live updates, alerts, etc.)

---

## 📞 Support

**Testing Issues?**
- Check: ESPN API is accessible
- Verify: Python dependencies installed
- Ensure: AWS credentials configured (for AWS tests)

**Prediction Questions?**
- See: `PREDICTION_METHODOLOGY.md`
- Review: `CONFIDENCE_BREAKDOWN.md`
- Check: `README.md`

---

**Ready to test tomorrow's NBA games!** 🏀

**Quick Start:**
```powershell
python check_tomorrow_games.py
cd nba && python predictor.py
```
