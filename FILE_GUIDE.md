# 📁 Complete File Guide - What Each File Does

## 🎯 Core Application Files

### Main Entry Points

**`api_service.py`**
- FastAPI web service for NBA predictions
- Provides REST API endpoints (/health, /daily-predictions, /predict)
- Swagger UI documentation at /docs
- Used for local development or production deployment

**`check_today_nba.py`**
- Quick script to check today's NBA games
- Shows game schedule with times
- Useful for verifying ESPN API is working

**`check_tomorrow_games.py`**
- Checks tomorrow's NBA games
- Helps plan ahead for predictions

**`get_today_nba_predictions.py`**
- Main script to get predictions for today's games
- Runs the predictor and displays results
- Shows predictions in table format

**`get_nba_predictions_table.py`**
- Gets predictions with table output
- Clean formatted display for betting decisions

**`get_nba_table_only.py`**
- Simplified version showing only the prediction table
- No extra output, just the betting recommendations

---

## 🏀 NBA Module (`nba/` folder)

**`nba/predictor.py`** ⭐ MAIN PREDICTION ENGINE
- Core prediction logic
- Fetches games from ESPN API (48-hour window)
- Calculates win probabilities from H2H data
- Integrates Bedrock + GPT-4o validation
- Generates predictions for all markets
- Filters by 75% confidence threshold
- Outputs predictions in table format

**`nba/nba_h2h_collector.py`**
- Collects head-to-head historical data
- Fetches 8-10 past games between two teams
- Gets real scores from ESPN API
- NO mock data - real data only

**`nba/agentic_ai_enhancer.py`**
- GPT-4o integration for AI validation
- Validates H2H data against historical knowledge
- Provides contextual insights (injuries, roster changes)
- Adjusts predictions based on AI analysis
- Optional: works without it but adds accuracy

**`nba/player_props_analyzer.py`**
- Analyzes individual player performance
- Predicts Points, Rebounds, Assists, 3PT, PRA
- Uses real roster data from ESPN
- Identifies top players by stats (PPG > 15)
- NO hardcoded players - dynamic roster fetching

**`nba/nba_betting_odds_api.py`**
- Integrates with The Odds API (optional)
- Fetches real betting lines if API key provided
- Falls back gracefully if unavailable
- Used for comparing predictions to market odds

**`nba/__init__.py`**
- Makes nba folder a Python package
- Allows imports like `from nba import predictor`

---

## ☁️ AWS Deployment (`aws/` folder)

### Infrastructure as Code

**`aws/template.yaml`** ⭐ MAIN AWS INFRASTRUCTURE
- SAM (Serverless Application Model) template
- Defines all AWS resources:
  - Lambda functions (daily predictions, single prediction, health check)
  - API Gateway (REST API endpoints)
  - DynamoDB table (stores predictions)
  - S3 bucket (logs)
  - IAM roles (permissions)
  - Bedrock integration (AI validation)
- Infrastructure as Code - reproducible deployment

**`aws/samconfig.toml`**
- SAM CLI configuration
- Stores deployment settings (region, stack name)
- Auto-generated during first deployment

### Lambda Functions

**`aws/lambda/daily_predictions/handler.py`**
- Lambda function for daily predictions endpoint
- Fetches all today's games
- Runs predictions with Bedrock validation
- Returns JSON response with all predictions
- Stores results in DynamoDB

**`aws/lambda/daily_predictions/requirements.txt`**
- Python dependencies for daily predictions Lambda
- Minimal: requests, boto3

**`aws/lambda/single_prediction/handler.py`**
- Lambda function for single game prediction
- Takes home_team and away_team as input
- Runs prediction with Bedrock validation
- Returns JSON response for one game

**`aws/lambda/single_prediction/requirements.txt`**
- Python dependencies for single prediction Lambda

**`aws/lambda/health_check/handler.py`**
- Simple health check endpoint
- Returns system status
- No dependencies needed

**`aws/lambda/data_collection/handler.py`**
- Scheduled Lambda for collecting game data
- Runs daily to fetch and store game results
- Updates historical database

**`aws/lambda/data_collection/requirements.txt`**
- Dependencies for data collection Lambda

### Lambda Layer

**`aws/layers/dependencies/requirements.txt`**
- Shared dependencies for all Lambda functions
- Includes: pandas, numpy, requests, boto3
- Deployed as Lambda Layer to reduce package size

### Deployment Scripts

**`aws/deploy_with_bedrock.ps1`** ⭐ RECOMMENDED DEPLOYMENT
- PowerShell script for Windows
- Deploys with Bedrock AI validation enabled
- Sets environment variables for AI features
- Shows deployment progress and API URLs
- **Use this for production deployment**

**`aws/deploy_with_bedrock.sh`**
- Bash script for Linux/Mac
- Same as PowerShell version but for Unix systems
- Deploys with Bedrock enabled

**`aws/simple_deploy.ps1`**
- Simplified PowerShell deployment
- Basic deployment without Bedrock
- Good for testing infrastructure only

**`aws/deploy.sh`**
- Basic bash deployment script
- Deploys without AI enhancements
- Minimal configuration

### Monitoring & Utilities

**`aws/monitor_costs.py`**
- Python script to monitor AWS costs
- Checks current month spending
- Shows cost breakdown by service
- Helps stay within budget

**`aws/README.md`**
- AWS-specific documentation
- Deployment instructions
- Testing endpoints
- Security configuration
- Cost optimization tips

---

## 📚 Documentation Files

### Main Documentation

**`README.md`** ⭐ MAIN PROJECT DOCUMENTATION
- Project overview and features
- Quick start guide
- System flow diagram with Bedrock
- Installation instructions
- API endpoints
- Technology stack
- What makes it different

**`QUICK_START.md`**
- Fast deployment guide (20 minutes)
- Step-by-step AWS deployment
- Minimal explanation, maximum action
- Perfect for getting started quickly

**`AWS_SETUP_GUIDE.md`**
- Detailed AWS setup instructions
- Prerequisites and requirements
- Account configuration
- IAM permissions
- Troubleshooting

**`DEPLOYMENT_INSTRUCTIONS.md`**
- Comprehensive deployment guide
- Multiple deployment options
- Testing procedures
- Post-deployment checklist

**`README_DEPLOYMENT.md`**
- Alternative deployment documentation
- Different deployment scenarios
- Advanced configurations

### Technical Documentation

**`BEDROCK_AI_VALIDATION.md`** ⭐ BEDROCK DOCUMENTATION
- What Bedrock does
- How it validates data
- Cost analysis (~$0.07/month)
- Benefits for real money betting
- Example scenarios
- Comparison with/without Bedrock

**`PREDICTION_METHODOLOGY.md`**
- How predictions are calculated
- Statistical models used
- Confidence scoring system
- Market predictions explained

**`CONFIDENCE_BREAKDOWN.md`**
- Detailed confidence scoring
- What each confidence level means
- Why 75% threshold
- How to interpret predictions

**`NO_MOCK_DATA_VERIFICATION.md`**
- Proof that no mock data is used
- What was removed from code
- Real data sources only
- Production safety verification

**`TESTING_GUIDE.md`**
- How to test the system
- Local testing procedures
- AWS endpoint testing
- Validation steps

**`PROJECT_STRUCTURE.md`**
- Project organization
- Folder structure
- File relationships
- Architecture overview

**`WHAT_WE_BUILT.md`**
- Feature summary
- What's completed
- What's planned
- Technical achievements

### Planning & Migration

**`aws_migration_plan.md`**
- Plan for migrating to AWS
- Architecture decisions
- Migration steps
- Timeline

**`AWS_IMPLEMENTATION_SUMMARY.md`**
- Summary of AWS implementation
- What was deployed
- How it works
- Cost breakdown

**`AWS_COMPETITION_SUBMISSION.md`**
- AWS competition submission details
- Project highlights
- Innovation points
- Business case

### Internal Documentation (Not in GitHub)

**`COMPETITION_CHECKLIST.md`** (excluded)
- Internal checklist for competition
- Not needed in public repo

**`CURRENT_STATUS.md`** (excluded)
- Internal status tracking
- Temporary file

**`DEMO_SCRIPT.md`** (excluded)
- Internal demo preparation
- Not for public

**`FORM_RESPONSES.md`** (excluded)
- Competition form responses
- Internal only

**`GITHUB_PUSH_READY.md`** (excluded)
- Pre-push checklist
- Internal verification

**`SECURITY_CHECK.md`** (excluded)
- Internal security audit
- Not for public repo

**`SUBMISSION_FORM_GUIDE.md`** (excluded)
- Competition submission guide
- Internal only

**`WHAT_WE_BUILT_SUMMARY.md`** (excluded)
- Internal summary
- Replaced by WHAT_WE_BUILT.md

---

## ⚙️ Configuration Files

**`.env.example`**
- Template for environment variables
- Shows what API keys are needed
- Safe to commit (no real keys)
- Copy to `.env` and add real keys

**`.gitignore`**
- Tells Git what files to ignore
- Excludes .env files (API keys)
- Excludes build artifacts
- Excludes deployment info with URLs
- Excludes internal documentation

**`requirements.txt`**
- Python dependencies for local development
- Lists all packages needed
- Install with: `pip install -r requirements.txt`
- Includes: fastapi, pandas, numpy, requests, tabulate, openai, boto3

---

## 🗑️ Generated/Temporary Files (Not in GitHub)

**`nba_predictions_today_tomorrow.txt`** (excluded)
- Generated prediction output
- Created when running predictions
- Not committed to Git

**`nba_real_predictions.txt`** (excluded)
- Another prediction output file
- Temporary results

**`predictions_output.txt`** (excluded)
- Prediction results
- Generated at runtime

**`DEPLOYMENT_SUMMARY.txt`** (excluded)
- Contains API URLs and account IDs
- Security risk - excluded from Git

**`.aws-sam/` folder** (excluded)
- AWS SAM build artifacts
- Generated during deployment
- Not needed in Git

---

## 📊 File Categories Summary

### Must Have (Core)
1. `nba/predictor.py` - Main prediction engine
2. `nba/nba_h2h_collector.py` - Data collection
3. `aws/template.yaml` - Infrastructure definition
4. `aws/deploy_with_bedrock.ps1` - Deployment script
5. `README.md` - Main documentation

### Important (Features)
1. `nba/agentic_ai_enhancer.py` - GPT-4o validation
2. `nba/player_props_analyzer.py` - Player predictions
3. `aws/lambda/*/handler.py` - Lambda functions
4. `BEDROCK_AI_VALIDATION.md` - Bedrock docs

### Nice to Have (Utilities)
1. `api_service.py` - Local API server
2. `check_today_nba.py` - Quick game checker
3. `aws/monitor_costs.py` - Cost monitoring
4. Various documentation files

### Configuration
1. `.env.example` - Environment template
2. `.gitignore` - Git exclusions
3. `requirements.txt` - Dependencies

---

## 🎯 Quick Reference: What to Use When

**Want to run predictions locally?**
→ `python get_today_nba_predictions.py`

**Want to deploy to AWS?**
→ `cd aws && ./deploy_with_bedrock.ps1`

**Want to test API locally?**
→ `python api_service.py`

**Want to check today's games?**
→ `python check_today_nba.py`

**Want to understand Bedrock?**
→ Read `BEDROCK_AI_VALIDATION.md`

**Want to understand predictions?**
→ Read `PREDICTION_METHODOLOGY.md`

**Want to monitor AWS costs?**
→ `python aws/monitor_costs.py`

**Need quick deployment?**
→ Read `QUICK_START.md`

---

## 🔄 File Relationships

```
User Request
    ↓
api_service.py OR get_today_nba_predictions.py
    ↓
nba/predictor.py (main engine)
    ↓
├── nba/nba_h2h_collector.py (get H2H data)
├── nba/agentic_ai_enhancer.py (GPT-4o validation)
├── nba/player_props_analyzer.py (player predictions)
└── nba/nba_betting_odds_api.py (odds integration)
    ↓
Output: Predictions in table format
```

**AWS Deployment:**
```
deploy_with_bedrock.ps1
    ↓
aws/template.yaml (infrastructure)
    ↓
Creates:
├── Lambda functions (from aws/lambda/*/handler.py)
├── API Gateway (REST endpoints)
├── DynamoDB (storage)
└── Bedrock integration (AI validation)
```

---

**Total Files:** ~50+ files
**Core Files:** ~15 files
**Documentation:** ~20 files
**AWS Infrastructure:** ~15 files

