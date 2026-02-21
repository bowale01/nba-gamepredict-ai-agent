"""
Daily Predictions Lambda Function
Get all high-confidence NBA predictions for today
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
    Main handler for daily predictions
    """
    
    try:
        # Get today's games
        games = get_todays_games()
        
        if not games:
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "total_matches_analyzed": 0,
                    "high_confidence_bets_found": 0,
                    "predictions": [],
                    "message": "No NBA games scheduled for today"
                })
            }
        
        # Generate predictions
        predictions = []
        for game in games[:10]:  # Limit to 10 games for cost control
            try:
                prediction = predict_game(game)
                if prediction and prediction.get('confidence', 0) >= 0.75:
                    predictions.append(prediction)
            except Exception as e:
                print(f"Error predicting game {game.get('id')}: {e}")
                continue
        
        # Build response
        response_body = {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "total_matches_analyzed": len(games),
            "high_confidence_bets_found": len(predictions),
            "predictions": predictions,
            "best_single_bet": predictions[0] if predictions else None,
            "strategy_recommendation": "Only high-confidence bets (75%+) recommended",
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(response_body, default=decimal_default)
        }
        
    except Exception as e:
        print(f"Error in daily predictions: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }

def get_todays_games():
    """Fetch today's NBA games from ESPN API"""
    
    try:
        today = datetime.utcnow().strftime("%Y%m%d")
        url = f"{ESPN_BASE}/scoreboard?dates={today}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        games = []
        
        for event in data.get('events', []):
            if 'competitions' in event and event['competitions']:
                competition = event['competitions'][0]
                competitors = competition.get('competitors', [])
                
                if len(competitors) == 2:
                    home_team = next((c for c in competitors if c.get('homeAway') == 'home'), None)
                    away_team = next((c for c in competitors if c.get('homeAway') == 'away'), None)
                    
                    if home_team and away_team:
                        game = {
                            "id": event.get('id'),
                            "date": today,
                            "home_team": home_team['team']['displayName'],
                            "away_team": away_team['team']['displayName'],
                            "home_team_id": int(home_team['team']['id']),
                            "away_team_id": int(away_team['team']['id']),
                            "status": competition.get('status', {}).get('type', {}).get('description', 'Scheduled')
                        }
                        games.append(game)
        
        # Cache in DynamoDB
        for game in games:
            try:
                games_table.put_item(
                    Item={
                        'game_id': game['id'],
                        'game_date': game['date'],
                        'home_team': game['home_team'],
                        'away_team': game['away_team'],
                        'status': game['status'],
                        'ttl': int((datetime.utcnow() + timedelta(days=1)).timestamp())
                    }
                )
            except Exception as e:
                print(f"Error caching game: {e}")
        
        return games
        
    except Exception as e:
        print(f"Error fetching games: {e}")
        return []

def predict_game(game):
    """Generate prediction for a single game with AI validation"""
    
    # Get H2H data
    h2h_data = get_h2h_data(game['home_team'], game['away_team'])
    
    if not h2h_data or len(h2h_data) < 4:
        return None  # Skip games without sufficient H2H data
    
    # Calculate statistics
    home_wins = sum(1 for g in h2h_data if g.get('winner') == game['home_team'])
    total_games = len(h2h_data)
    home_win_pct = home_wins / total_games if total_games > 0 else 0.5
    
    avg_total = sum(g.get('total_points', 0) for g in h2h_data) / total_games if total_games > 0 else 220
    
    # AI Validation with Bedrock (ENABLED for real money betting)
    ai_validation = None
    confidence_adjustment = 0
    
    if os.environ.get('AI_ENHANCEMENT_ENABLED') == 'true':
        ai_validation = validate_with_bedrock(game, h2h_data)
        
        # Adjust confidence based on AI validation
        if ai_validation and ai_validation.get('validated'):
            if ai_validation['ai_status'] == 'QUESTIONABLE':
                confidence_adjustment = -0.10  # Reduce confidence by 10%
            elif ai_validation['ai_status'] == 'NEEDS_ADJUSTMENT':
                confidence_adjustment = -0.20  # Reduce confidence by 20%
            elif ai_validation['betting_advice'] == 'SKIP_GAME':
                return None  # Skip game if AI recommends it
    
    # Calculate final confidence with AI adjustment
    base_confidence = max(home_win_pct, 1 - home_win_pct)
    final_confidence = max(0.5, min(0.99, base_confidence + confidence_adjustment))
    
    # Build enhanced prediction
    prediction = {
        "match": f"{game['away_team']} @ {game['home_team']}",
        "time": "TBD",
        "prediction": f"{'Home Win' if home_win_pct > 0.6 else 'Away Win' if home_win_pct < 0.4 else 'Close Game'}",
        "confidence": round(final_confidence, 3),
        "quality": "HIGH-CONFIDENCE" if final_confidence >= 0.75 else "MEDIUM",
        "h2h_matches": total_games,
        "predicted_total": round(avg_total, 1),
        "recommendation": f"Over {avg_total:.1f}" if avg_total > 220 else f"Under {avg_total:.1f}",
        "data_source": "ESPN API + H2H Analysis" + (" + AI Validation" if ai_validation else "")
    }
    
    # Add AI validation details if available
    if ai_validation and ai_validation.get('validated'):
        prediction['ai_validation'] = {
            'status': ai_validation['ai_status'],
            'confidence': ai_validation['ai_confidence'],
            'insight': ai_validation['key_insight'],
            'advice': ai_validation['betting_advice']
        }
        prediction['confidence_adjusted'] = confidence_adjustment != 0
    
    # Save prediction to DynamoDB
    try:
        item = {
            'prediction_id': f"{game['id']}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            'created_at': datetime.utcnow().isoformat(),
            'game_id': game['id'],
            'home_team': game['home_team'],
            'away_team': game['away_team'],
            'confidence': Decimal(str(prediction['confidence'])),
            'prediction_type': prediction['prediction'],
            'ttl': int((datetime.utcnow() + timedelta(days=1)).timestamp())
        }
        
        # Add AI validation to DynamoDB if available
        if ai_validation and ai_validation.get('validated'):
            item['ai_validated'] = True
            item['ai_status'] = ai_validation['ai_status']
            item['ai_confidence'] = Decimal(str(ai_validation['ai_confidence']))
        
        predictions_table.put_item(Item=item)
    except Exception as e:
        print(f"Error saving prediction: {e}")
    
    return prediction

def get_h2h_data(home_team, away_team):
    """Get H2H data from cache or ESPN API"""
    
    matchup_key = f"{home_team}_{away_team}"
    
    # Try cache first
    try:
        response = h2h_table.query(
            KeyConditionExpression='matchup_key = :mk',
            ExpressionAttributeValues={':mk': matchup_key},
            Limit=10
        )
        
        if response.get('Items'):
            return response['Items']
    except Exception as e:
        print(f"Error querying H2H cache: {e}")
    
    # Fetch from ESPN API (simplified - real implementation would parse actual games)
    # For now, return empty to skip games without cached data
    return []

def validate_with_bedrock(game, h2h_data):
    """Validate H2H data with Amazon Bedrock (Claude) - Enhanced for real money betting"""
    
    try:
        # Calculate H2H statistics
        home_wins = sum(1 for g in h2h_data if g.get('winner') == game['home_team'])
        away_wins = len(h2h_data) - home_wins
        avg_total = sum(g.get('total_points', 0) for g in h2h_data) / len(h2h_data) if h2h_data else 220
        
        # Enhanced prompt for betting validation
        prompt = f"""You are an expert NBA analyst validating betting predictions. Analyze this matchup:

**Matchup:** {game['home_team']} vs {game['away_team']}
**H2H Data:** {len(h2h_data)} games analyzed
- {game['home_team']} wins: {home_wins}
- {game['away_team']} wins: {away_wins}
- Average total points: {avg_total:.1f}

**Critical Questions:**
1. Does this H2H record align with NBA historical trends for these teams?
2. Are there recent roster changes, injuries, or coaching changes that make old H2H data less relevant?
3. Is the average total points realistic for current NBA pace?
4. Any red flags or anomalies in this data?

**Respond in this exact format:**
VALIDATION: [ACCURATE/QUESTIONABLE/NEEDS_ADJUSTMENT]
CONFIDENCE: [0-100]
KEY_INSIGHT: [One sentence about the most important factor]
BETTING_ADVICE: [TRUST_DATA/USE_CAUTION/SKIP_GAME]

Keep total response under 100 words."""

        # Call Bedrock (Claude Haiku - fast and cost-effective)
        response = bedrock.invoke_model(
            modelId=os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-haiku-20240307-v1:0'),
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "temperature": 0.3,  # Lower temperature for more consistent validation
                "messages": [{
                    "role": "user",
                    "content": prompt
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        ai_response = result.get('content', [{}])[0].get('text', '')
        
        # Parse AI response
        validation_result = {
            'status': 'ACCURATE',
            'confidence': 75,
            'insight': 'AI validation completed',
            'advice': 'TRUST_DATA'
        }
        
        # Extract structured data from response
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
        
        print(f"✅ Bedrock validation: {validation_result['status']} ({validation_result['confidence']}%)")
        
        return {
            'validated': True,
            'ai_status': validation_result['status'],
            'ai_confidence': validation_result['confidence'],
            'key_insight': validation_result['insight'],
            'betting_advice': validation_result['advice'],
            'full_response': ai_response
        }
        
    except Exception as e:
        print(f"⚠️ Bedrock validation error: {e}")
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

