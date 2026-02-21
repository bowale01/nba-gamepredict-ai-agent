# 🚀 AWS Migration Plan - Cost-Optimized NBA GamePredict AI

## 📋 Phase 1: AWS Free Tier Foundation (Week 1-2)

### Architecture Overview
```
User Request
    ↓
CloudFront (CDN) → API Gateway → Lambda Functions
                                      ↓
                            ┌─────────┴─────────┐
                            ↓                   ↓
                      DynamoDB            Amazon Bedrock
                    (Game Data)         (AI Enhancement)
                            ↓
                        S3 Bucket
                    (Logs & Archives)
```

### Cost Breakdown (Monthly - Free Tier)

| Service | Free Tier | Expected Usage | Cost |
|---------|-----------|----------------|------|
| Lambda | 1M requests | ~300K requests | $0 |
| API Gateway | 1M calls | ~300K calls | $0 |
| DynamoDB | 25GB + 25 RCU/WCU | ~3GB + 10 RCU/WCU | $0 |
| S3 | 5GB + 20K GET | ~1GB + 5K GET | $0 |
| CloudWatch | 10 metrics | 5 metrics | $0 |
| Bedrock | 3 months trial | Dev usage | $0 |
| **TOTAL** | | | **$0/month** |

### After Free Tier (Estimated)

| Service | Cost per Unit | Expected Usage | Monthly Cost |
|---------|---------------|----------------|--------------|
| Lambda | $0.20 per 1M requests | 500K requests | $0.10 |
| API Gateway | $3.50 per 1M calls | 500K calls | $1.75 |
| DynamoDB | $0.25 per GB | 5GB | $1.25 |
| Bedrock (Claude Haiku) | $0.25 per 1M tokens | 2M tokens | $0.50 |
| S3 | $0.023 per GB | 2GB | $0.05 |
| CloudWatch | $0.30 per metric | 5 metrics | $1.50 |
| **TOTAL** | | | **~$5.15/month** |

## 🎯 Implementation Steps

### Step 1: Lambda Functions (Serverless Compute)
Replace FastAPI with Lambda functions:
- `get_daily_predictions` - Main prediction endpoint
- `predict_single_game` - Single game prediction
- `health_check` - System health
- `collect_h2h_data` - ESPN API data collection

### Step 2: DynamoDB Tables
- `nba_games` - Today's games cache (TTL: 24 hours)
- `h2h_history` - Historical matchup data (TTL: 7 days)
- `predictions` - Generated predictions (TTL: 24 hours)
- `prediction_accuracy` - Track accuracy over time

### Step 3: Amazon Bedrock Integration
Replace OpenAI GPT-4o with Amazon Bedrock:
- **Model**: Claude 3 Haiku (fastest, cheapest)
- **Cost**: $0.25 per 1M input tokens, $1.25 per 1M output tokens
- **Use Case**: H2H validation, contextual analysis
- **Estimated**: ~$0.50/month for 100 predictions/day

### Step 4: API Gateway
- REST API endpoints
- Rate limiting (100 requests/minute per IP)
- API key authentication
- CORS configuration

### Step 5: S3 Storage
- Prediction logs archive
- Historical data backup
- Static assets (if needed)

## 💰 Cost Optimization Strategies

### 1. Aggressive Caching
```python
# Cache ESPN API responses for 1 hour
# Cache predictions for 30 minutes
# Reduces API calls by 80%
```

### 2. Efficient DynamoDB Queries
```python
# Use partition keys: game_date + team_names
# Use TTL to auto-delete old data
# On-demand pricing (pay per request)
```

### 3. Lambda Optimization
```python
# Memory: 256MB (sufficient for predictions)
# Timeout: 30 seconds
# Cold start mitigation: Keep functions warm
```

### 4. Bedrock Cost Control
```python
# Use Claude Haiku (cheapest)
# Limit context window to 2K tokens
# Cache AI responses for similar games
# Only use AI for validation, not generation
```

## 📊 Scaling Projections

### 100 Users/Day
- Requests: ~500/day = 15K/month
- Lambda: FREE (within 1M limit)
- DynamoDB: FREE (within 25GB limit)
- Bedrock: ~$0.15/month
- **Total: $0.15/month**

### 1,000 Users/Day
- Requests: ~5K/day = 150K/month
- Lambda: FREE
- DynamoDB: FREE
- Bedrock: ~$1.50/month
- **Total: $1.50/month**

### 10,000 Users/Day
- Requests: ~50K/day = 1.5M/month
- Lambda: $0.30
- API Gateway: $5.25
- DynamoDB: $2.00
- Bedrock: $15.00
- **Total: ~$22.55/month**

## 🔧 Technology Stack

### Current → AWS Migration

| Current | AWS Replacement | Benefit |
|---------|----------------|---------|
| FastAPI + Uvicorn | Lambda + API Gateway | Serverless, auto-scale |
| OpenAI GPT-4o | Amazon Bedrock (Claude) | 60% cheaper, AWS native |
| Local Python | Lambda Layers | No server management |
| Manual scaling | Auto-scaling | Pay per use |
| Requests library | boto3 | AWS optimized |

## 🚀 Quick Start Commands

### 1. Install AWS CLI & SAM
```bash
# Install AWS CLI
pip install awscli

# Install AWS SAM (Serverless Application Model)
pip install aws-sam-cli

# Configure AWS credentials
aws configure
```

### 2. Create Project Structure
```
nba-gamepredict-aws/
├── lambda/
│   ├── daily_predictions/
│   │   └── handler.py
│   ├── single_prediction/
│   │   └── handler.py
│   └── health_check/
│       └── handler.py
├── layers/
│   └── dependencies/
│       └── requirements.txt
├── template.yaml (SAM template)
└── README.md
```

### 3. Deploy to AWS
```bash
# Build
sam build

# Deploy (first time)
sam deploy --guided

# Deploy (subsequent)
sam deploy
```

## 📝 Next Steps

1. **Create Lambda functions** - Convert FastAPI endpoints
2. **Set up DynamoDB** - Define tables and indexes
3. **Configure Bedrock** - Replace OpenAI with Claude
4. **Deploy API Gateway** - REST API with authentication
5. **Test thoroughly** - Ensure predictions work
6. **Monitor costs** - CloudWatch + Cost Explorer

## ⚠️ Important Notes

- **Free Tier Duration**: 12 months for most services
- **Bedrock Trial**: 3 months free (then pay-per-use)
- **DynamoDB**: On-demand pricing recommended (no upfront cost)
- **Lambda**: 1M requests/month free FOREVER
- **S3**: First 5GB free for 12 months

## 🎯 Success Metrics

- [ ] Deploy within AWS Free Tier limits
- [ ] Maintain <500ms API response time
- [ ] Keep monthly cost under $5 (after free tier)
- [ ] 99.9% uptime
- [ ] Support 1000+ predictions/day

---

**Ready to start? Let's build Phase 1!**
