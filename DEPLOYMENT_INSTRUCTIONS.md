# 🚀 AWS Deployment Instructions

## Current Status

✅ AWS CLI is installed and configured
⏳ SAM CLI is installing (may take 5-10 minutes)

## Deployment Options

### Option 1: Wait for SAM CLI Installation (Recommended)

SAM CLI is currently installing in the background. Once complete:

```powershell
# Check if SAM is installed
sam --version

# If installed, deploy:
cd aws
sam build
sam deploy --guided
```

**Guided Deployment Prompts:**
- Stack name: `nba-gamepredict-ai`
- AWS Region: `us-east-1` (or your preferred region)
- Confirm changes: `y`
- Allow SAM CLI IAM role creation: `y`
- Save arguments to config: `y`

**Time:** ~10 minutes

---

### Option 2: Manual AWS Console Setup (No CLI needed)

If you prefer using the AWS web console:

#### Step 1: Create Lambda Function
1. Go to https://console.aws.amazon.com/lambda/
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `nba-gamepredict-health`
5. Runtime: `Python 3.13`
6. Click "Create function"
7. Copy code from `aws/lambda/health_check/handler.py`
8. Click "Deploy"

#### Step 2: Create API Gateway
1. Go to https://console.aws.amazon.com/apigateway/
2. Click "Create API"
3. Choose "REST API" → "Build"
4. API name: `nba-gamepredict-api`
5. Create resource `/health`
6. Create GET method
7. Integration type: Lambda Function
8. Select your Lambda function
9. Deploy API to "prod" stage

#### Step 3: Create DynamoDB Tables
1. Go to https://console.aws.amazon.com/dynamodb/
2. Click "Create table"
3. Table name: `nba-games`
4. Partition key: `game_id` (String)
5. Sort key: `game_date` (String)
6. Table settings: "On-demand"
7. Enable TTL: attribute name `ttl`
8. Click "Create table"

Repeat for:
- `nba-predictions` (partition: `prediction_id`, sort: `created_at`)
- `nba-h2h-history` (partition: `matchup_key`, sort: `game_date`)

**Time:** ~30 minutes

---

### Option 3: Use Terraform (Alternative IaC)

If you prefer Terraform over SAM:

```bash
# Install Terraform
# https://www.terraform.io/downloads

# Create Terraform config (we can generate this if needed)
terraform init
terraform plan
terraform apply
```

---

## Check SAM Installation Status

Run this command to check if SAM CLI finished installing:

```powershell
sam --version
```

**Expected output:**
```
SAM CLI, version 1.154.0
```

If you see this, SAM is ready! Proceed with Option 1.

---

## Cost Monitoring

After deployment, monitor costs:

```powershell
# Run cost monitor
python aws/monitor_costs.py

# Or check AWS Console
# https://console.aws.amazon.com/cost-management/home
```

---

## Testing After Deployment

### Test Health Endpoint
```powershell
# Replace YOUR-API-ID with actual API Gateway ID
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "message": "NBA GamePredict AI Agent - Serverless on AWS",
  "timestamp": "2025-01-XX...",
  "version": "2.0.0-aws"
}
```

### Test Predictions Endpoint
```powershell
curl https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/daily-predictions
```

---

## Troubleshooting

### SAM Installation Taking Too Long
- Installation can take 5-15 minutes depending on internet speed
- Check progress: `pip list | findstr sam`
- If stuck, cancel (Ctrl+C) and retry: `pip install aws-sam-cli --upgrade`

### AWS Credentials Not Working
```powershell
# Reconfigure AWS
aws configure

# Test credentials
aws sts get-caller-identity
```

### Deployment Fails
- Check CloudFormation console for error details
- Ensure you have sufficient IAM permissions
- Try deploying to a different region

---

## Next Steps After Deployment

1. ✅ Test all endpoints
2. ⬜ Set up billing alerts ($1/month threshold)
3. ⬜ Configure API keys for production
4. ⬜ Monitor CloudWatch logs
5. ⬜ Review cost monitoring dashboard

---

## Quick Reference

| Task | Command |
|------|---------|
| Check SAM | `sam --version` |
| Build | `sam build` |
| Deploy | `sam deploy --guided` |
| View logs | `sam logs -n HealthCheckFunction --tail` |
| Delete stack | `sam delete` |
| Monitor costs | `python aws/monitor_costs.py` |

---

## Documentation

- **Full Setup Guide**: `AWS_SETUP_GUIDE.md`
- **Architecture Details**: `aws_migration_plan.md`
- **Quick Start**: `QUICK_START.md`
- **AWS README**: `aws/README.md`

---

## Support

- **GitHub**: https://github.com/bowale01/AI-Agents
- **AWS Docs**: https://docs.aws.amazon.com/
- **SAM Docs**: https://docs.aws.amazon.com/serverless-application-model/

---

**Current Status**: SAM CLI installing... Check back in 5-10 minutes!

**Estimated Total Time**: 20 minutes (after SAM installation)
**Monthly Cost**: $0 (Free Tier) or $0.15-$22 (after)
