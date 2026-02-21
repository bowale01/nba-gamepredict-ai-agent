#!/usr/bin/env python3
"""
AWS Cost Monitoring Script
Track and alert on NBA GamePredict AI costs
"""

import boto3
from datetime import datetime, timedelta
import json

def get_current_month_costs():
    """Get current month AWS costs"""
    
    ce = boto3.client('ce')  # Cost Explorer
    
    # Get current month date range
    today = datetime.now()
    start_date = today.replace(day=1).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'SERVICE', 'Key': 'SERVICE'}
            ]
        )
        
        return response
    except Exception as e:
        print(f"Error fetching costs: {e}")
        return None

def get_service_costs(response):
    """Parse costs by service"""
    
    if not response or 'ResultsByTime' not in response:
        return {}
    
    costs = {}
    for result in response['ResultsByTime']:
        for group in result.get('Groups', []):
            service = group['Keys'][0]
            amount = float(group['Metrics']['BlendedCost']['Amount'])
            costs[service] = amount
    
    return costs

def check_free_tier_usage():
    """Check Free Tier usage"""
    
    ce = boto3.client('ce')
    
    # Get last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UsageQuantity'],
            Filter={
                'Dimensions': {
                    'Key': 'RECORD_TYPE',
                    'Values': ['Usage']
                }
            },
            GroupBy=[
                {'Type': 'SERVICE', 'Key': 'SERVICE'}
            ]
        )
        
        return response
    except Exception as e:
        print(f"Error checking Free Tier: {e}")
        return None

def estimate_monthly_cost(daily_requests):
    """Estimate monthly cost based on daily requests"""
    
    monthly_requests = daily_requests * 30
    
    # Free Tier limits
    lambda_free = 1_000_000  # 1M requests
    api_gateway_free = 1_000_000  # 1M calls
    
    # Costs after Free Tier
    lambda_cost_per_million = 0.20
    api_gateway_cost_per_million = 3.50
    bedrock_cost_per_million_tokens = 0.25  # Claude Haiku input
    
    # Calculate costs
    costs = {
        'lambda': 0,
        'api_gateway': 0,
        'bedrock': 0,
        'dynamodb': 0,
        's3': 0,
        'total': 0
    }
    
    # Lambda costs
    if monthly_requests > lambda_free:
        excess = monthly_requests - lambda_free
        costs['lambda'] = (excess / 1_000_000) * lambda_cost_per_million
    
    # API Gateway costs
    if monthly_requests > api_gateway_free:
        excess = monthly_requests - api_gateway_free
        costs['api_gateway'] = (excess / 1_000_000) * api_gateway_cost_per_million
    
    # Bedrock costs (assume 10% of requests use AI)
    ai_requests = monthly_requests * 0.1
    tokens_per_request = 500  # Average
    total_tokens = ai_requests * tokens_per_request
    costs['bedrock'] = (total_tokens / 1_000_000) * bedrock_cost_per_million_tokens
    
    # DynamoDB (on-demand, minimal cost)
    costs['dynamodb'] = 0.50  # Estimate
    
    # S3 (minimal storage)
    costs['s3'] = 0.05  # Estimate
    
    # Total
    costs['total'] = sum(costs.values())
    
    return costs

def main():
    """Main monitoring function"""
    
    print("🏀 NBA GamePredict AI - AWS Cost Monitor")
    print("=" * 60)
    print()
    
    # Get current month costs
    print("📊 Current Month Costs:")
    print("-" * 60)
    
    response = get_current_month_costs()
    if response:
        costs = get_service_costs(response)
        
        total = sum(costs.values())
        
        if total == 0:
            print("✅ No costs yet (within Free Tier)")
        else:
            print(f"Total: ${total:.2f}")
            print()
            print("By Service:")
            for service, cost in sorted(costs.items(), key=lambda x: x[1], reverse=True):
                if cost > 0:
                    print(f"  {service}: ${cost:.2f}")
    else:
        print("❌ Could not fetch cost data")
    
    print()
    print("-" * 60)
    print()
    
    # Cost projections
    print("💰 Cost Projections:")
    print("-" * 60)
    
    scenarios = [
        ("100 users/day", 500),
        ("1,000 users/day", 5000),
        ("10,000 users/day", 50000)
    ]
    
    for scenario_name, daily_requests in scenarios:
        costs = estimate_monthly_cost(daily_requests)
        print(f"\n{scenario_name} (~{daily_requests:,} requests/day):")
        print(f"  Lambda: ${costs['lambda']:.2f}")
        print(f"  API Gateway: ${costs['api_gateway']:.2f}")
        print(f"  Bedrock (AI): ${costs['bedrock']:.2f}")
        print(f"  DynamoDB: ${costs['dynamodb']:.2f}")
        print(f"  S3: ${costs['s3']:.2f}")
        print(f"  TOTAL: ${costs['total']:.2f}/month")
    
    print()
    print("-" * 60)
    print()
    
    # Recommendations
    print("💡 Cost Optimization Tips:")
    print("-" * 60)
    print("1. Enable API Gateway caching (reduces Lambda invocations)")
    print("2. Use DynamoDB TTL to auto-delete old data")
    print("3. Limit Bedrock usage to high-value predictions only")
    print("4. Set CloudWatch alarms for cost thresholds")
    print("5. Use S3 lifecycle policies to move old logs to Glacier")
    print()
    
    # Free Tier status
    print("🎁 Free Tier Status:")
    print("-" * 60)
    print("Lambda: 1M requests/month FREE (forever)")
    print("API Gateway: 1M calls/month FREE (12 months)")
    print("DynamoDB: 25GB + 25 RCU/WCU FREE (forever)")
    print("S3: 5GB storage FREE (12 months)")
    print("Bedrock: 3 months trial, then pay-per-use")
    print()

if __name__ == "__main__":
    main()
