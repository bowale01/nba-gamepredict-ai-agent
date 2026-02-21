#!/bin/bash

# Deploy NBA GamePredict AI with Bedrock AI Validation Enabled
# This enables AI-powered validation for real money betting

echo "=========================================="
echo "NBA GamePredict AI - Bedrock Deployment"
echo "=========================================="
echo ""
echo "🤖 AI Validation: ENABLED"
echo "💰 Use Case: Real Money Betting"
echo "📊 Model: Claude 3 Haiku (Fast & Cost-Effective)"
echo ""

# Check if SAM CLI is available
if ! command -v sam &> /dev/null; then
    if ! python -m samcli --version &> /dev/null; then
        echo "❌ SAM CLI not found. Please install it first."
        exit 1
    fi
    SAM_CMD="python -m samcli"
else
    SAM_CMD="sam"
fi

echo "✅ Using SAM CLI: $SAM_CMD"
echo ""

# Build
echo "📦 Building Lambda functions..."
$SAM_CMD build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build successful"
echo ""

# Deploy
echo "🚀 Deploying to AWS..."
echo "⚠️  This will enable Bedrock AI validation"
echo "💵 Estimated cost: $0.01-0.05 per day"
echo ""

$SAM_CMD deploy \
    --stack-name nba-gamepredict-ai \
    --region us-east-1 \
    --capabilities CAPABILITY_IAM \
    --no-confirm-changeset \
    --no-fail-on-empty-changeset

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ DEPLOYMENT SUCCESSFUL"
echo "=========================================="
echo ""
echo "🤖 Bedrock AI Validation: ENABLED"
echo "📊 Features:"
echo "   - H2H data validation"
echo "   - Anomaly detection"
echo "   - Confidence adjustments"
echo "   - Betting advice (TRUST/CAUTION/SKIP)"
echo ""
echo "💡 API Endpoints:"
$SAM_CMD list stack-outputs --stack-name nba-gamepredict-ai --region us-east-1
echo ""
echo "🎯 Ready for real money betting predictions!"
echo "=========================================="
