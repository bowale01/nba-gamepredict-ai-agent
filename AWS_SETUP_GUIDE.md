# 🚀 AWS Setup Guide - NBA GamePredict AI

## Step-by-Step AWS Deployment (Cost-Optimized)

### Prerequisites (5 minutes)

1. **AWS Account**
   - Sign up at https://aws.amazon.com/free/
   - Free Tier includes 12 months of free services
   - Credit card required (won't be charged within Free Tier limits)

2. **Install AWS CLI**
   ```bash
   pip install awscli
   ```

3. **Install AWS SAM CLI**
   ```bash
   pip install aws-sam-cli
   ```

4. **Configure AWS Credentials**
   ```bash
   aws configure
   ```
   You'll need:
   - AWS Access Key ID (from IAM console)
   - AWS Secret Access Key
   - Default region (recommend: us-east-1)

### Deployment (10 minutes)

1. **Navigate to AWS directory**
   ```bash
   cd aws
   ```

2. **Make deploy script executable**
   ```bash
   chmod +x deploy.sh
   ```

3. **Run deployment**
   ```bash
   ./deploy.sh
   ```

4. **Follow prompts**
   - Stack name: `nba-gamepredict-ai`
   - AWS Region: `us-east-1` (or your preferred region)
   - Confirm changes: `y`

5. **Wait for deployment** (~5-10 minutes)
   - SAM will create all resources
   - You'll see progress in terminal

### Verify Deployment (2 minutes)

1. **Test health endpoint**
   ```bash
   # Get your API endpoint from deployment output
   curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/health
   ```

2. **Test predictions endpoint**
   ```bash
   curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/daily-predictions
   ```

3. **Check AWS Console**
   - Lambda: https://console.aws.amazon.com/lambda/
   - API Gateway: https://console.aws.amazon.com/apigateway/
   - DynamoDB: https://console.aws.amazon.com/dynamodb/

### Monitor Costs (Ongoing)

1. **Run cost monitor**
   ```bash
   cd aws
   python monitor_costs.py
   ```

2. **Set up billing alerts**
   - Go to AWS Billing Dashboard
   - Create budget alert for $1/month
   - Get email notifications

3. **Check CloudWatch**
   - View Lambda logs
   - Monitor API Gateway metrics
   - Check error rates

### Cost Expectations

**Within Free Tier (First 12 months):**
- 0-1,000 users/day: **$0/month**
- Lambda: FREE (1M requests/month)
- API Gateway: FREE (1M calls/month)
- DynamoDB: FREE (25GB storage)

**After Free Tier:**
- 100 users/day: **~$0.15/month**
- 1,000 users/day: **~$1.50/month**
- 10,000 users/day: **~$22/month**

### Troubleshooting

**Issue: AWS CLI not configured**
```bash
aws configure
# Enter your credentials
```

**Issue: SAM CLI not found**
```bash
pip install aws-sam-cli
```

**Issue: Deployment fails**
- Check AWS credentials: `aws sts get-caller-identity`
- Check region: `aws configure get region`
- Check CloudFormation console for error details

**Issue: Lambda timeout**
- Increase timeout in `template.yaml`
- Redeploy: `sam build && sam deploy`

**Issue: High costs**
- Run `python monitor_costs.py`
- Check CloudWatch metrics
- Reduce Bedrock usage (set `AI_ENHANCEMENT_ENABLED=false`)

### Next Steps

1. ✅ Deploy to AWS
2. ⬜ Test all endpoints
3. ⬜ Set up cost alerts ($1/month threshold)
4. ⬜ Configure API keys for production
5. ⬜ Add CloudFront CDN (optional)
6. ⬜ Implement caching (optional)
7. ⬜ Set up CI/CD pipeline (optional)

### Cleanup (When Done)

To delete all AWS resources:
```bash
cd aws
sam delete
```

This removes:
- All Lambda functions
- API Gateway
- DynamoDB tables
- S3 bucket
- CloudWatch alarms

**No charges after deletion!**

### Support

- AWS Free Tier: https://aws.amazon.com/free/
- AWS Documentation: https://docs.aws.amazon.com/
- SAM Documentation: https://docs.aws.amazon.com/serverless-application-model/
- GitHub Issues: [Your repo]/issues

---

**Total Setup Time: ~20 minutes**
**Monthly Cost (Free Tier): $0**
**Monthly Cost (After Free Tier): $0.15 - $22 depending on usage**

🎉 **You're ready to build on AWS!**
