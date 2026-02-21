#!/bin/bash

# NBA GamePredict AI - AWS Deployment Script
# Cost-optimized deployment to AWS Free Tier

set -e  # Exit on error

echo "🏀 NBA GamePredict AI - AWS Deployment"
echo "========================================"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   pip install awscli"
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ AWS SAM CLI not found. Please install it first:"
    echo "   pip install aws-sam-cli"
    exit 1
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run:"
    echo "   aws configure"
    exit 1
fi

echo "✅ AWS credentials configured"
echo ""

# Build Lambda layer
echo "📦 Building Lambda layer with dependencies..."
cd layers/dependencies

# Create python directory for layer
mkdir -p python/lib/python3.13/site-packages

# Install dependencies
pip install -r requirements.txt -t python/lib/python3.13/site-packages --upgrade

# Go back to root
cd ../..

echo "✅ Lambda layer built"
echo ""

# Build SAM application
echo "🔨 Building SAM application..."
sam build

echo "✅ SAM application built"
echo ""

# Deploy
echo "🚀 Deploying to AWS..."
echo ""
echo "⚠️  IMPORTANT: This will create AWS resources"
echo "   - Lambda functions (FREE TIER: 1M requests/month)"
echo "   - API Gateway (FREE TIER: 1M calls/month)"
echo "   - DynamoDB tables (FREE TIER: 25GB storage)"
echo "   - S3 bucket (FREE TIER: 5GB storage)"
echo ""
read -p "Continue with deployment? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Check if this is first deployment
if [ ! -f samconfig.toml ]; then
    echo "📝 First time deployment - running guided setup..."
    sam deploy --guided
else
    echo "📝 Deploying with existing configuration..."
    sam deploy
fi

echo ""
echo "✅ Deployment complete!"
echo ""

# Get API endpoint
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name nba-gamepredict-ai \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text 2>/dev/null || echo "")

if [ -n "$API_ENDPOINT" ]; then
    echo "🌐 API Endpoints:"
    echo "   Health Check: ${API_ENDPOINT}/health"
    echo "   Daily Predictions: ${API_ENDPOINT}/daily-predictions"
    echo ""
    
    # Test health endpoint
    echo "🧪 Testing health endpoint..."
    curl -s "${API_ENDPOINT}/health" | python -m json.tool
    echo ""
fi

echo "💰 Cost Monitoring:"
echo "   - View costs: https://console.aws.amazon.com/cost-management/home"
echo "   - Set budget alerts in AWS Budgets"
echo "   - Monitor CloudWatch metrics"
echo ""

echo "📊 Next Steps:"
echo "   1. Test the API endpoints"
echo "   2. Monitor CloudWatch logs"
echo "   3. Set up cost alerts"
echo "   4. Configure API keys for production"
echo ""

echo "🎉 Deployment successful!"
