#!/usr/bin/env python3
"""
Smart API using your ModelSelector algorithm for dual database storage
- User conversations stored in SQLite
- Model analytics stored separately
- Graceful error handling for missing dependencies
"""

import sqlite3
import json
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Flask
try:
    from flask import Flask, request, jsonify
    flask_available = True
except ImportError:
    logger.error("Flask not installed. Run: pip install flask")
    flask_available = False

# Try to import your ModelSelector
try:
    from model_selector import ModelSelector
    import joblib
    model_available = True
except ImportError:
    logger.error("ModelSelector not available")
    model_available = False

if not flask_available:
    print("Please install Flask: pip install flask")
    exit(1)

app = Flask(__name__)

# Database paths
CONVERSATIONS_DB = 'user_conversations.db'
ANALYTICS_DB = 'model_analytics.db'
MODEL_PATH = 'model_selector.pkl'

# Global model instance
model_selector = None

def load_model():
    """Load your trained ModelSelector"""
    global model_selector
    try:
        if model_available and os.path.exists(MODEL_PATH):
            model_selector = joblib.load(MODEL_PATH)
            logger.info("✅ ModelSelector loaded successfully!")
            return True
        else:
            logger.error(f"❌ Model file {MODEL_PATH} not found or ModelSelector unavailable")
            return False
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False

def init_databases():
    """Initialize both databases with required tables"""
    try:
        # Database 1: User Conversations
        conn1 = sqlite3.connect(CONVERSATIONS_DB)
        cursor1 = conn1.cursor()
        cursor1.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                user_id TEXT,
                session_id TEXT,
                prompt TEXT NOT NULL,
                response TEXT,
                model_used TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                response_time_ms INTEGER,
                tokens_used INTEGER,
                satisfaction_rating INTEGER
            )
        ''')
        conn1.commit()
        conn1.close()
        
        # Database 2: Model Selection Analytics
        conn2 = sqlite3.connect(ANALYTICS_DB)
        cursor2 = conn2.cursor()
        cursor2.execute('''
            CREATE TABLE IF NOT EXISTS model_predictions (
                prediction_id TEXT PRIMARY KEY,
                prompt TEXT NOT NULL,
                predicted_model TEXT,
                confidence_score REAL,
                all_model_scores TEXT,
                prompt_features TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                actual_model_used TEXT,
                prediction_correct BOOLEAN
            )
        ''')
        conn2.commit()
        conn2.close()
        
        logger.info("✅ Databases initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def store_conversation(user_id, session_id, prompt, response, model_used, response_time_ms=0, tokens_used=0):
    """Store user conversation in conversations database"""
    try:
        conn = sqlite3.connect(CONVERSATIONS_DB)
        cursor = conn.cursor()
        
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id[:8]}"
        
        cursor.execute('''
            INSERT INTO conversations 
            (conversation_id, user_id, session_id, prompt, response, model_used, response_time_ms, tokens_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (conversation_id, user_id, session_id, prompt, response, model_used, response_time_ms, tokens_used))
        
        conn.commit()
        conn.close()
        return conversation_id
    except Exception as e:
        logger.error(f"Error storing conversation: {e}")
        return None

def store_model_prediction(prompt, prediction_result):
    """Store model prediction analytics in analytics database"""
    try:
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        cursor.execute('''
            INSERT INTO model_predictions 
            (prediction_id, prompt, predicted_model, confidence_score, all_model_scores, prompt_features)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            prediction_id,
            prompt,
            prediction_result.get('predicted_model', 'unknown'),
            prediction_result.get('prediction_confidence', 0.0),
            json.dumps(prediction_result.get('confidence_scores', {})),
            json.dumps(prediction_result.get('prompt_features', {}))
        ))
        
        conn.commit()
        conn.close()
        return prediction_id
    except Exception as e:
        logger.error(f"Error storing prediction: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model_selector else "not_loaded"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'databases': {
            'conversations': os.path.exists(CONVERSATIONS_DB),
            'analytics': os.path.exists(ANALYTICS_DB)
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict_best_model():
    """Use your algorithm to predict the best model for a prompt"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        if not model_selector:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Use your ModelSelector algorithm
        prediction_result = model_selector.predict_best_model(prompt)
        
        # Store the prediction in analytics database
        prediction_id = store_model_prediction(prompt, prediction_result)
        
        # Return the algorithm's choice
        return jsonify({
            'success': True,
            'prediction_id': prediction_id,
            'predicted_model': prediction_result['predicted_model'],
            'confidence': prediction_result['prediction_confidence'],
            'all_model_scores': prediction_result['confidence_scores'],
            'prompt_analysis': prediction_result['prompt_features']
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Handle chat request with dual database storage"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', 'default')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Step 1: Use your algorithm to choose the best model
        if model_selector:
            prediction_result = model_selector.predict_best_model(prompt)
            chosen_model = prediction_result['predicted_model']
            confidence = prediction_result['prediction_confidence']
            
            # Store prediction analytics
            store_model_prediction(prompt, prediction_result)
        else:
            chosen_model = 'fallback_model'
            confidence = 0.5
        
        # Step 2: Generate response (placeholder - integrate with your actual models)
        response = f"Response from {chosen_model} (confidence: {confidence:.2f}): This is a simulated response to '{prompt[:50]}...'"
        
        # Step 3: Store conversation
        conversation_id = store_conversation(
            user_id=user_id,
            session_id=session_id,
            prompt=prompt,
            response=response,
            model_used=chosen_model,
            response_time_ms=100,  # Replace with actual timing
            tokens_used=len(response.split())
        )
        
        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'response': response,
            'model_used': chosen_model,
            'confidence': confidence
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Get user conversations from database"""
    try:
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 10))
        
        conn = sqlite3.connect(CONVERSATIONS_DB)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT * FROM conversations 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conversations = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'conversations': conversations,
            'count': len(conversations)
        })
        
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get model prediction analytics"""
    try:
        limit = int(request.args.get('limit', 10))
        
        conn = sqlite3.connect(ANALYTICS_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM model_predictions 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        predictions = [dict(zip(columns, row)) for row in rows]
        
        # Parse JSON fields for better display
        for pred in predictions:
            try:
                pred['all_model_scores'] = json.loads(pred['all_model_scores']) if pred['all_model_scores'] else {}
                pred['prompt_features'] = json.loads(pred['prompt_features']) if pred['prompt_features'] else {}
            except:
                pass
        
        conn.close()
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'count': len(predictions)
        })
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Smart API with your ModelSelector algorithm...")
    
    # Initialize databases
    if not init_databases():
        print("❌ Database initialization failed")
        exit(1)
    
    # Load your model
    model_loaded = load_model()
    if model_loaded:
        print("✅ Your ModelSelector is ready to choose the best responses!")
    else:
        print("⚠️  Running without ModelSelector - using fallback mode")
    
    print("\n📊 Dual Database Architecture:")
    print(f"   👥 User Conversations: {CONVERSATIONS_DB}")
    print(f"   📈 Model Analytics: {ANALYTICS_DB}")
    print("\n🌐 API Endpoints:")
    print("   POST /predict - Get best model prediction")
    print("   POST /chat - Handle chat with dual storage")
    print("   GET /conversations - View user conversations")
    print("   GET /analytics - View model analytics")
    print("   GET /health - Health check")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
