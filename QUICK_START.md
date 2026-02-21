# ⚡ Quick Start - NBA GamePredict AI on AWS

## 🚀 Deploy in 3 Commands

```bash
# 1. Install tools
pip install awscli aws-sam-cli && aws configure

# 2. Navigate and deploy
cd aws && chmod +x deploy.sh && ./deploy.sh

# 3. Test
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/health
```

**Done! Your API is live on AWS.** ✅

---

## 📋 What You Get

- ✅ Serverless NBA prediction API
- ✅ 4 Lambda functions (health, predictions, data collection)
- ✅ DynamoDB tables (games, predictions, H2H history)
- ✅ API Gateway with rate limiting
- ✅ CloudWatch monitoring
- ✅ Cost alarms ($1/day threshold)
- ✅ S3 log storage

---

## 💰 Cost

| Users/Day | Free Tier | After Free Tier |
|-----------|-----------|-----------------|
| 100 | $0 | $0.15/month |
| 1,000 | $0 | $1.50/month |
| 10,000 | $0 | $22/month |

**Free Tier lasts 12 months** 🎁

---

## 🔧 Common Commands

### Deploy
```bash
cd aws
sam build && sam deploy
```

### Monitor Costs
```bash
cd aws
python monitor_costs.py
```

### View Logs
```bash
sam logs -n DailyPredictionsFunction --tail
```

### Test Endpoints
```bash
# Health check
curl https://YOUR-API/prod/health

# Daily predictions
curl https://YOUR-API/prod/daily-predictions

# Single prediction
curl -X POST https://YOUR-API/prod/predict \
  -H "Content-Type: application/json" \
  -d '{"home_team":"Lakers","away_team":"Warriors"}'
```

### Delete Everything
```bash
cd aws
sam delete
```

---

## 📚 Documentation

- **Full Setup**: `AWS_SETUP_GUIDE.md`
- **Architecture**: `aws_migration_plan.md`
- **Implementation**: `AWS_IMPLEMENTATION_SUMMARY.md`
- **AWS Details**: `aws/README.md`

---

## 🆘 Troubleshooting

**AWS CLI not configured?**
```bash
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1)
```

**SAM not found?**
```bash
pip install aws-sam-cli
```

**Deployment failed?**
```bash
# Check credentials
aws sts get-caller-identity

# Check region
aws configure get region

# View CloudFormation errors
aws cloudformation describe-stack-events --stack-name nba-gamepredict-ai
```

**High costs?**
```bash
# Disable AI enhancement
# Edit aws/template.yaml:
# AI_ENHANCEMENT_ENABLED: false

# Redeploy
sam build && sam deploy
```

---

## 🎯 Next Steps

1. ✅ Deploy to AWS
2. ⬜ Test endpoints
3. ⬜ Set up billing alerts
4. ⬜ Configure API keys
5. ⬜ Monitor CloudWatch

---

## 📞 Need Help?

- **GitHub**: https://github.com/bowale01/AI-Agents
- **AWS Docs**: https://docs.aws.amazon.com/
- **SAM Docs**: https://docs.aws.amazon.com/serverless-application-model/

---

**Total Time: 20 minutes from zero to production** ⚡

**Cost: $0 (Free Tier) or $0.15-$22/month (after)** 💰

**Scalability: 10 to 10,000+ users** 📈

🎉 **You're ready to build!**
