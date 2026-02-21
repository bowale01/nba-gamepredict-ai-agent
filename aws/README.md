# 🏀 NBA GamePredict AI - AWS Deployment

## 🚀 Quick Start

### Prerequisites
```bash
# Install AWS CLI
pip install awscli

# Install AWS SAM CLI
pip install aws-sam-cli

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
```

### Deploy to AWS
```bash
cd aws

# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

## 📁 Project Structure

```
aws/
├── template.yaml                 # SAM template (infrastructure as code)
├── deploy.sh                     # Deployment script
├── lambda/
│   ├── health_check/
│   │   └── handler.py           # Health check endpoint
│   ├── daily_predictions/
│   │   └── handler.py           # Daily predictions endpoint
│   ├── single_prediction/
│   │   └── handler.py           # Single game prediction
│   └── data_collection/
│       └── handler.py           # Scheduled data collection
└── layers/
    └── dependencies/
        └── requirements.txt     # Python dependencies
```

## 💰 Cost Breakdown

### AWS Free Tier (12 months)
- Lambda: 1M requests/month FREE
- API Gateway: 1M calls/month FREE
- DynamoDB: 25GB storage + 25 RCU/WCU FREE
- S3: 5GB storage FREE
- CloudWatch: 10 metrics FREE

### After Free Tier
- **100 users/day**: ~$0.15/month
- **1,000 users/day**: ~$1.50/month
- **10,000 users/day**: ~$22/month

## 🔧 Configuration

### Environment Variables
Set in `template.yaml`:
- `ENVIRONMENT`: production/development
- `LOG_LEVEL`: INFO/DEBUG
- `AI_ENHANCEMENT_ENABLED`: true/false (controls Bedrock usage)

### DynamoDB Tables
- `nba-games`: Today's games (TTL: 24 hours)
- `nba-predictions`: Generated predictions (TTL: 24 hours)
- `nba-h2h-history`: Historical matchup data (TTL: 7 days)

### API Endpoints
After deployment:
- `GET /health` - System health check
- `GET /daily-predictions` - All high-confidence predictions
- `POST /predict` - Single game prediction

## 📊 Monitoring

### CloudWatch Logs
```bash
# View Lambda logs
sam logs -n HealthCheckFunction --tail

# View API Gateway logs
aws logs tail /aws/apigateway/nba-gamepredict --follow
```

### Cost Monitoring
```bash
# View current month costs
aws ce get-cost-and-usage \
    --time-period Start=2025-01-01,End=2025-01-31 \
    --granularity MONTHLY \
    --metrics BlendedCost
```

### CloudWatch Alarms
- High Cost Alarm: Triggers when daily cost > $1
- Lambda Error Alarm: Triggers on 5+ errors in 5 minutes

## 🧪 Testing

### Test Health Endpoint
```bash
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/health
```

### Test Daily Predictions
```bash
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/daily-predictions
```

### Test Single Prediction
```bash
curl -X POST https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Lakers", "away_team": "Warriors"}'
```

## 🔐 Security

### API Keys (Production)
1. Enable API key requirement in `template.yaml`:
   ```yaml
   Auth:
     ApiKeyRequired: true
   ```

2. Create API key:
   ```bash
   aws apigateway create-api-key --name nba-gamepredict-key --enabled
   ```

3. Create usage plan and associate key

### IAM Permissions
Lambda functions have minimal permissions:
- DynamoDB: Read/Write to specific tables only
- Bedrock: InvokeModel only
- CloudWatch: Logs only

## 🚀 Scaling

### Increase Lambda Memory
Edit `template.yaml`:
```yaml
Globals:
  Function:
    MemorySize: 512  # Increase from 256MB
```

### Add Caching
Enable API Gateway caching:
```yaml
NBAGamePredictAPI:
  Type: AWS::Serverless::Api
  Properties:
    CacheClusterEnabled: true
    CacheClusterSize: '0.5'  # 0.5GB cache
```

### Enable DynamoDB Auto-Scaling
Switch from on-demand to provisioned with auto-scaling for predictable traffic.

## 🐛 Troubleshooting

### Lambda Timeout
Increase timeout in `template.yaml`:
```yaml
Timeout: 60  # seconds
```

### Out of Memory
Increase memory:
```yaml
MemorySize: 512  # MB
```

### DynamoDB Throttling
Switch to on-demand pricing or increase provisioned capacity.

### Bedrock Errors
Check:
1. Bedrock is enabled in your region
2. Model access is granted
3. IAM permissions are correct

## 📝 Update Deployment

```bash
# Make changes to code
# Then redeploy
cd aws
sam build
sam deploy
```

## 🗑️ Cleanup

To delete all AWS resources:
```bash
sam delete
```

This will remove:
- Lambda functions
- API Gateway
- DynamoDB tables
- S3 bucket
- CloudWatch alarms

## 🎯 Next Steps

1. ✅ Deploy to AWS
2. ⬜ Test all endpoints
3. ⬜ Set up cost alerts
4. ⬜ Configure API keys
5. ⬜ Add CloudFront CDN
6. ⬜ Implement caching
7. ⬜ Add monitoring dashboard
8. ⬜ Set up CI/CD pipeline

## 📞 Support

- AWS Documentation: https://docs.aws.amazon.com/
- SAM Documentation: https://docs.aws.amazon.com/serverless-application-model/
- GitHub Issues: [Your repo]/issues

---

**Built with AWS Free Tier - Cost-optimized for scale** 🚀
