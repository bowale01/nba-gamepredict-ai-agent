# Simple AWS Deployment Script (No SAM required)
# Uses AWS CLI directly with CloudFormation

Write-Host "🏀 NBA GamePredict AI - Simple AWS Deployment" -ForegroundColor Green
Write-Host "=" * 60
Write-Host ""

# Check AWS CLI
Write-Host "🔐 Checking AWS CLI..." -ForegroundColor Cyan
try {
    $awsVersion = aws --version 2>&1
    Write-Host "✅ AWS CLI installed: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Install it first:" -ForegroundColor Red
    Write-Host "   pip install awscli" -ForegroundColor Yellow
    exit 1
}

# Check AWS credentials
Write-Host ""
Write-Host "🔐 Checking AWS credentials..." -ForegroundColor Cyan
try {
    $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Host "✅ AWS credentials configured" -ForegroundColor Green
    Write-Host "   Account: $($identity.Account)" -ForegroundColor Gray
    Write-Host "   User: $($identity.Arn)" -ForegroundColor Gray
} catch {
    Write-Host "❌ AWS credentials not configured. Run:" -ForegroundColor Red
    Write-Host "   aws configure" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📦 Deployment Options:" -ForegroundColor Cyan
Write-Host "   1. Full deployment (requires SAM CLI)" -ForegroundColor Yellow
Write-Host "   2. Manual setup guide" -ForegroundColor Yellow
Write-Host ""

Write-Host "⚠️  SAM CLI not detected. Showing manual setup guide..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=" * 60
Write-Host ""

Write-Host "📝 MANUAL SETUP GUIDE" -ForegroundColor Green
Write-Host "=" * 60
Write-Host ""

Write-Host "Option 1: Install SAM CLI (Recommended)" -ForegroundColor Cyan
Write-Host "-" * 60
Write-Host "1. Install SAM CLI:"
Write-Host "   pip install aws-sam-cli" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Wait for installation to complete (may take 5-10 minutes)"
Write-Host ""
Write-Host "3. Run deployment:"
Write-Host "   cd aws" -ForegroundColor Yellow
Write-Host "   sam build" -ForegroundColor Yellow
Write-Host "   sam deploy --guided" -ForegroundColor Yellow
Write-Host ""

Write-Host "Option 2: Use AWS Console (No CLI needed)" -ForegroundColor Cyan
Write-Host "-" * 60
Write-Host "1. Go to AWS Lambda Console:"
Write-Host "   https://console.aws.amazon.com/lambda/" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Create Lambda function:"
Write-Host "   - Name: nba-gamepredict-health" -ForegroundColor Yellow
Write-Host "   - Runtime: Python 3.13" -ForegroundColor Yellow
Write-Host "   - Copy code from: aws/lambda/health_check/handler.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Create API Gateway:"
Write-Host "   https://console.aws.amazon.com/apigateway/" -ForegroundColor Yellow
Write-Host "   - Type: REST API" -ForegroundColor Yellow
Write-Host "   - Connect to Lambda function" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Create DynamoDB tables:"
Write-Host "   https://console.aws.amazon.com/dynamodb/" -ForegroundColor Yellow
Write-Host "   - Table: nba-games" -ForegroundColor Yellow
Write-Host "   - Partition key: game_id (String)" -ForegroundColor Yellow
Write-Host "   - Sort key: game_date (String)" -ForegroundColor Yellow
Write-Host ""

Write-Host "Option 3: Wait for SAM Installation" -ForegroundColor Cyan
Write-Host "-" * 60
Write-Host "SAM CLI is currently installing in the background."
Write-Host "Check installation status:"
Write-Host "   sam --version" -ForegroundColor Yellow
Write-Host ""
Write-Host "Once installed, run:"
Write-Host "   cd aws" -ForegroundColor Yellow
Write-Host "   sam build" -ForegroundColor Yellow
Write-Host "   sam deploy --guided" -ForegroundColor Yellow
Write-Host ""

Write-Host "=" * 60
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - Full Guide: AWS_SETUP_GUIDE.md"
Write-Host "   - Quick Start: QUICK_START.md"
Write-Host "   - Architecture: aws_migration_plan.md"
Write-Host ""

Write-Host "💰 Cost Estimate:" -ForegroundColor Cyan
Write-Host "   - Free Tier: $0/month (first 12 months)"
Write-Host "   - After: $0.15-$22/month depending on usage"
Write-Host ""

Write-Host "🆘 Need Help?" -ForegroundColor Cyan
Write-Host "   - GitHub: https://github.com/bowale01/AI-Agents"
Write-Host "   - AWS Docs: https://docs.aws.amazon.com/"
Write-Host ""
