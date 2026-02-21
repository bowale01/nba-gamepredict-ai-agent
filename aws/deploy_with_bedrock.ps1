# Deploy NBA GamePredict AI with Bedrock AI Validation Enabled
# This enables AI-powered validation for real money betting

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "NBA GamePredict AI - Bedrock Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "AI Validation: ENABLED" -ForegroundColor Green
Write-Host "Use Case: Real Money Betting" -ForegroundColor Yellow
Write-Host "Model: Claude 3 Haiku (Fast and Cost-Effective)" -ForegroundColor Blue
Write-Host ""

# Check if SAM CLI is available
$samCmd = "sam"
try {
    sam --version | Out-Null
} catch {
    try {
        python -m samcli --version | Out-Null
        $samCmd = "python -m samcli"
    } catch {
        Write-Host "ERROR: SAM CLI not found. Please install it first." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Using SAM CLI: $samCmd" -ForegroundColor Green
Write-Host ""

# Build
Write-Host "Building Lambda functions..." -ForegroundColor Yellow
if ($samCmd -eq "sam") {
    sam build
} else {
    python -m samcli build
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    exit 1
}

Write-Host "Build successful" -ForegroundColor Green
Write-Host ""

# Deploy
Write-Host "Deploying to AWS..." -ForegroundColor Yellow
Write-Host "WARNING: This will enable Bedrock AI validation" -ForegroundColor Yellow
Write-Host "Estimated cost: 0.01-0.05 USD per day" -ForegroundColor Yellow
Write-Host ""

if ($samCmd -eq "sam") {
    sam deploy `
        --stack-name nba-gamepredict-ai `
        --region us-east-1 `
        --capabilities CAPABILITY_IAM `
        --no-confirm-changeset `
        --no-fail-on-empty-changeset
} else {
    python -m samcli deploy `
        --stack-name nba-gamepredict-ai `
        --region us-east-1 `
        --capabilities CAPABILITY_IAM `
        --no-confirm-changeset `
        --no-fail-on-empty-changeset
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT SUCCESSFUL" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bedrock AI Validation: ENABLED" -ForegroundColor Green
Write-Host "Features:" -ForegroundColor Blue
Write-Host "   - H2H data validation"
Write-Host "   - Anomaly detection"
Write-Host "   - Confidence adjustments"
Write-Host "   - Betting advice (TRUST/CAUTION/SKIP)"
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Yellow
if ($samCmd -eq "sam") {
    sam list stack-outputs --stack-name nba-gamepredict-ai --region us-east-1
} else {
    python -m samcli list stack-outputs --stack-name nba-gamepredict-ai --region us-east-1
}
Write-Host ""
Write-Host "Ready for real money betting predictions!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
