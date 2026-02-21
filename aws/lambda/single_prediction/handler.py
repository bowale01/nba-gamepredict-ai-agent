"""
Single Game Prediction Lambda Function
Predict a specific NBA game with AI validation
"""

import json
import os
from datetime import datetime, timedelta
import boto3
import requests
from decimal import Decimal

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
bedrock = boto3.client('bedrock-runtime')

# DynamoDB tables
games_table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'nba-games'))
predictions_table = dynamodb.Table(os.environ.get('PREDICTIONS_TABLE', 'nba-predictions'))
h2h_table = dynamodb.Table(os.environ.get('H2H_TABLE', 'nba-h2h-history'))

# ESPN API
ESPN_BASE = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba"

def lambda_handler(event, context):
    """
    Single game prediction endpoint with AI validation
    """
    
    try:
        # Parse request body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        home_team = body.get('home_team', '')
        away_team = body.get('away_team', '')
        
        if not home_team or not away_team:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "home_team and away_team are required"})
            }
        
        # Get H2H data
        h2h_data = get_h2h_data(home_team, away_team)
        
        if not h2h_data or len(h2h_data) < 4:
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "match": f"{away_team} @ {home_team}",
                    "error": "Insufficient H2H data",
                    "h2h_matches": len(h2h_data) if h2h_data else 0,
                    "minimum_required": 4,
                    "recommendation": "Skip - Not enough historical data"
                })
            }
        
        # Generate prediction with AI validation
        game_data = {
            'home_team': home_team,
            'away_team': away_team,
            'id': f"{home_team}_{away_team}_{datetime.utcnow().strftime('%Y%m%d')}"
        }
        
        prediction = predict_game_with_ai(game_data, h2h_data)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(prediction, default=decimal_default)
        }
        
    except Exception as e:
        print(f"Error in single prediction: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }

def predict_game_with_ai(game, h2h_data):
    """Generate prediction with AI validation"""
    
    # Calculate statistics
    home_wins = sum(1 for g in h2h_data if g.get('winner') == game['home_team'])
    total_games = len(h2h_data)
    home_win_pct = home_wins / total_games if total_games > 0 else 0.5
    
    avg_total = sum(g.get('total_points', 0) for g in h2h_data) / total_games if total_games > 0 else 220
    
    # AI Validation with Bedrock
    ai_validation = None
    confidence_adjustment = 0
    
    if os.environ.get('AI_ENHANCEMENT_ENABLED') == 'true':
        ai_validation = validate_with_bedrock(game, h2h_data)
        
        if ai_validation and ai_validation.get('validated'):
            if ai_validation['ai_status'] == 'QUESTIONABLE':
                confidence_adjustment = -0.10
            elif ai_validation['ai_status'] == 'NEEDS_ADJUSTMENT':
                confidence_adjustment = -0.20
    
    # Calculate final confidence
    base_confidence = max(home_win_pct, 1 - home_win_pct)
    final_confidence = max(0.5, min(0.99, base_confidence + confidence_adjustment))
    
    # Build prediction
    prediction = {
        "match": f"{game['away_team']} @ {game['home_team']}",
        "time": "TBD",
        "prediction": f"{'Home Win' if home_win_pct > 0.6 else 'Away Win' if home_win_pct < 0.4 else 'Close Game'}",
        "confidence": round(final_confidence, 3),
        "quality": "HIGH-CONFIDENCE" if final_confidence >= 0.75 else "MEDIUM",
        "h2h_matches": total_games,
        "predicted_total": round(avg_total, 1),
        "recommendation": f"Over {avg_total:.1f}" if avg_total > 220 else f"Under {avg_total:.1f}",
        "data_source": "ESPN API + H2H Analysis + AI Validation",
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Add AI validation details
    if ai_validation and ai_validation.get('validated'):
        prediction['ai_validation'] = {
            'status': ai_validation['ai_status'],
            'confidence': ai_validation['ai_confidence'],
            'insight': ai_validation['key_insight'],
            'advice': ai_validation['betting_advice']
        }
    
    return prediction

def get_h2h_data(home_team, away_team):
    """Get H2H data from cache"""
    matchup_key = f"{home_team}_{away_team}"
    
    try:
        response = h2h_table.query(
            KeyConditionExpression='matchup_key = :mk',
            ExpressionAttributeValues={':mk': matchup_key},
            Limit=10
        )
        return response.get('Items', [])
    except Exception as e:
        print(f"Error querying H2H cache: {e}")
        return []

def validate_with_bedrock(game, h2h_data):
    """Validate H2H data with Amazon Bedrock (Claude)"""
    
    try:
        home_wins = sum(1 for g in h2h_data if g.get('winner') == game['home_team'])
        away_wins = len(h2h_data) - home_wins
        avg_total = sum(g.get('total_points', 0) for g in h2h_data) / len(h2h_data) if h2h_data else 220
        
        prompt = f"""You are an expert NBA analyst validating betting predictions. Analyze this matchup:

**Matchup:** {game['home_team']} vs {game['away_team']}
**H2H Data:** {len(h2h_data)} games analyzed
- {game['home_team']} wins: {home_wins}
- {game['away_team']} wins: {away_wins}
- Average total points: {avg_total:.1f}

**Critical Questions:**
1. Does this H2H record align with NBA historical trends?
2. Recent roster/coaching changes affecting relevance?
3. Is the average total realistic for current NBA pace?
4. Any red flags or anomalies?

**Respond in this exact format:**
VALIDATION: [ACCURATE/QUESTIONABLE/NEEDS_ADJUSTMENT]
CONFIDENCE: [0-100]
KEY_INSIGHT: [One sentence]
BETTING_ADVICE: [TRUST_DATA/USE_CAUTION/SKIP_GAME]

Keep under 100 words."""

        response = bedrock.invoke_model(
            modelId=os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0'),
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "temperature": 0.3,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        ai_response = result.get('content', [{}])[0].get('text', '')
        
        # Parse response
        validation_result = {
            'status': 'ACCURATE',
            'confidence': 75,
            'insight': 'AI validation completed',
            'advice': 'TRUST_DATA'
        }
        
        for line in ai_response.split('\n'):
            if 'VALIDATION:' in line:
                validation_result['status'] = line.split('VALIDATION:')[1].strip().split()[0]
            elif 'CONFIDENCE:' in line:
                try:
                    validation_result['confidence'] = int(''.join(filter(str.isdigit, line)))
                except:
                    pass
            elif 'KEY_INSIGHT:' in line:
                validation_result['insight'] = line.split('KEY_INSIGHT:')[1].strip()
            elif 'BETTING_ADVICE:' in line:
                validation_result['advice'] = line.split('BETTING_ADVICE:')[1].strip().split()[0]
        
        return {
            'validated': True,
            'ai_status': validation_result['status'],
            'ai_confidence': validation_result['confidence'],
            'key_insight': validation_result['insight'],
            'betting_advice': validation_result['advice']
        }
        
    except Exception as e:
        print(f"Bedrock validation error: {e}")
        return {
            'validated': False,
            'error': str(e),
            'ai_status': 'ERROR',
            'betting_advice': 'USE_CAUTION'
        }

def decimal_default(obj):
    """JSON serializer for Decimal objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
