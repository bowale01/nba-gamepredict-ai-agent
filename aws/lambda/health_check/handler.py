"""
Health Check Lambda Function
Simple health check endpoint for NBA GamePredict AI
"""

import json
import os
from datetime import datetime
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    """
    Health check endpoint
    Returns system status and basic metrics
    """
    
    try:
        # Check DynamoDB connectivity
        table_name = os.environ.get('DYNAMODB_TABLE', 'nba-games')
        table = dynamodb.Table(table_name)
        
        # Simple table check (doesn't count against read capacity)
        table.table_status
        
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Build response
    response_body = {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "message": "NBA GamePredict AI Agent - Serverless on AWS",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "2.0.0-aws",
        "components": {
            "api": "healthy",
            "database": db_status,
            "ai_engine": "healthy"
        },
        "environment": os.environ.get('ENVIRONMENT', 'production'),
        "region": os.environ.get('AWS_REGION', 'unknown')
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_body)
    }
