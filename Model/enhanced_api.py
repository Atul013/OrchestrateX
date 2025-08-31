#!/usr/bin/env python3
"""
Enhanced Model Selector API with Dual Database Storage
Separates user conversations from model analytics
"""

from flask import Flask, request, jsonify
from model_selector import ModelSelector
import sqlite3
import json
from datetime import datetime
import uuid

app = Flask(__name__)
selector = ModelSelector()
selector.load_model('model_selector.pkl')

# Initialize databases
def init_databases():
    """Initialize both databases with required tables"""
    
    # Database 1: User Conversations
    conn1 = sqlite3.connect('user_conversations.db')
    cursor1 = conn1.cursor()
    cursor1.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            user_id TEXT,
            session_id TEXT,
            prompt TEXT NOT NULL,
            response TEXT,
            model_used TEXT,
            timestamp DATETIME,
            response_time_ms INTEGER,
            tokens_used INTEGER,
            cost_usd REAL
        )
    ''')
    conn1.commit()
    conn1.close()
    
    # Database 2: Model Selection Analytics
    conn2 = sqlite3.connect('model_analytics.db')
    cursor2 = conn2.cursor()
    cursor2.execute('''
        CREATE TABLE IF NOT EXISTS model_predictions (
            prediction_id TEXT PRIMARY KEY,
            prompt TEXT NOT NULL,
            predicted_model TEXT,
            confidence_score REAL,
            all_confidences TEXT,  -- JSON string
            actual_model_used TEXT,
            response_quality INTEGER,  -- 1-5 rating
            timestamp DATETIME,
            prompt_features TEXT,  -- JSON string
            prediction_accuracy BOOLEAN
        )
    ''')
    conn2.commit()
    conn2.close()

def store_conversation(data):
    """Store user conversation in conversations database"""
    conn = sqlite3.connect('user_conversations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations 
        (conversation_id, user_id, session_id, prompt, response, model_used, 
         timestamp, response_time_ms, tokens_used, cost_usd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['conversation_id'], data.get('user_id'), data.get('session_id'),
        data['prompt'], data['response'], data['model_used'],
        data['timestamp'], data.get('response_time_ms'), 
        data.get('tokens_used'), data.get('cost_usd')
    ))
    conn.commit()
    conn.close()

def store_model_prediction(data):
    """Store model prediction analytics"""
    conn = sqlite3.connect('model_analytics.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO model_predictions 
        (prediction_id, prompt, predicted_model, confidence_score, all_confidences,
         actual_model_used, timestamp, prompt_features)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['prediction_id'], data['prompt'], data['predicted_model'],
        data['confidence_score'], json.dumps(data['all_confidences']),
        data.get('actual_model_used'), data['timestamp'],
        json.dumps(data['prompt_features'])
    ))
    conn.commit()
    conn.close()

@app.route('/predict', methods=['POST'])
def predict_model():
    """Get model prediction only (for testing algorithm)"""
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Missing prompt parameter'}), 400
    
    # Get prediction from your algorithm
    result = selector.select_best_model(prompt)
    
    # Store model prediction analytics
    prediction_data = {
        'prediction_id': str(uuid.uuid4()),
        'prompt': prompt,
        'predicted_model': result['predicted_model'],
        'confidence_score': result['prediction_confidence'],
        'all_confidences': result['confidence_scores'],
        'timestamp': datetime.now(),
        'prompt_features': result['prompt_features']
    }
    store_model_prediction(prediction_data)
    
    return jsonify({
        'best_model': result['predicted_model'],
        'prediction_confidence': result['prediction_confidence'],
        'confidence_scores': result['confidence_scores'],
        'prediction_id': prediction_data['prediction_id']
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Full chat with model selection, AI call, and dual storage"""
    data = request.get_json()
    prompt = data.get('prompt')
    user_id = data.get('user_id', 'anonymous')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    if not prompt:
        return jsonify({'error': 'Missing prompt parameter'}), 400
    
    start_time = datetime.now()
    
    # 1. Get model prediction
    prediction_result = selector.select_best_model(prompt)
    predicted_model = prediction_result['predicted_model']
    
    # 2. TODO: Call actual AI model (placeholder for now)
    ai_response = f"[{predicted_model} Response] Thank you for your prompt: '{prompt}'. This would be the actual AI response."
    
    end_time = datetime.now()
    response_time_ms = int((end_time - start_time).total_seconds() * 1000)
    
    # 3. Generate IDs
    conversation_id = str(uuid.uuid4())
    prediction_id = str(uuid.uuid4())
    
    # 4. Store in conversations database
    conversation_data = {
        'conversation_id': conversation_id,
        'user_id': user_id,
        'session_id': session_id,
        'prompt': prompt,
        'response': ai_response,
        'model_used': predicted_model,
        'timestamp': start_time,
        'response_time_ms': response_time_ms,
        'tokens_used': 150,  # TODO: Get from actual AI call
        'cost_usd': 0.002    # TODO: Calculate actual cost
    }
    store_conversation(conversation_data)
    
    # 5. Store in model analytics database
    analytics_data = {
        'prediction_id': prediction_id,
        'prompt': prompt,
        'predicted_model': predicted_model,
        'confidence_score': prediction_result['prediction_confidence'],
        'all_confidences': prediction_result['confidence_scores'],
        'actual_model_used': predicted_model,
        'timestamp': start_time,
        'prompt_features': prediction_result['prompt_features']
    }
    store_model_prediction(analytics_data)
    
    return jsonify({
        'response': ai_response,
        'model_used': predicted_model,
        'confidence': prediction_result['prediction_confidence'],
        'conversation_id': conversation_id,
        'prediction_id': prediction_id,
        'response_time_ms': response_time_ms
    })

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Get user conversation history"""
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    
    conn = sqlite3.connect('user_conversations.db')
    cursor = conn.cursor()
    
    if user_id:
        cursor.execute('SELECT * FROM conversations WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    elif session_id:
        cursor.execute('SELECT * FROM conversations WHERE session_id = ? ORDER BY timestamp DESC', (session_id,))
    else:
        cursor.execute('SELECT * FROM conversations ORDER BY timestamp DESC LIMIT 50')
    
    conversations = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'conversations': [dict(zip([col[0] for col in cursor.description], row)) for row in conversations]
    })

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get model selection analytics"""
    conn = sqlite3.connect('model_analytics.db')
    cursor = conn.cursor()
    
    # Model usage statistics
    cursor.execute('''
        SELECT predicted_model, COUNT(*) as usage_count, AVG(confidence_score) as avg_confidence
        FROM model_predictions 
        GROUP BY predicted_model 
        ORDER BY usage_count DESC
    ''')
    model_stats = cursor.fetchall()
    
    # Recent predictions
    cursor.execute('SELECT * FROM model_predictions ORDER BY timestamp DESC LIMIT 20')
    recent_predictions = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'model_statistics': [dict(zip(['model', 'usage_count', 'avg_confidence'], row)) for row in model_stats],
        'recent_predictions': [dict(zip([col[0] for col in cursor.description], row)) for row in recent_predictions]
    })

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback on model prediction quality"""
    data = request.get_json()
    prediction_id = data.get('prediction_id')
    quality_rating = data.get('rating')  # 1-5
    
    if not prediction_id or not quality_rating:
        return jsonify({'error': 'Missing prediction_id or rating'}), 400
    
    conn = sqlite3.connect('model_analytics.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE model_predictions 
        SET response_quality = ? 
        WHERE prediction_id = ?
    ''', (quality_rating, prediction_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Feedback recorded successfully'})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'orchestratex-dual-db-api',
        'algorithm_loaded': selector.classifier is not None
    })

if __name__ == "__main__":
    print("Initializing dual databases...")
    init_databases()
    print("✅ Databases initialized")
    print("🚀 Starting Enhanced Model Selector API...")
    app.run(host='0.0.0.0', port=5000, debug=True)
