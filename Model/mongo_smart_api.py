#!/usr/bin/env python3
"""
Smart API with MongoDB Integration
Uses your ModelSelector algorithm with existing Docker database
"""

import os
from datetime import datetime
import logging
import json

# Try to import dependencies
try:
    from flask import Flask, request, jsonify
    flask_available = True
except ImportError:
    print("Flask not installed. Run: pip install flask")
    flask_available = False

try:
    from pymongo import MongoClient
    from bson import ObjectId
    mongo_available = True
except ImportError:
    print("PyMongo not installed. Run: pip install pymongo")
    mongo_available = False

try:
    from model_selector import ModelSelector
    import joblib
    model_available = True
except ImportError:
    print("ModelSelector not available")
    model_available = False

if not flask_available:
    exit(1)

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Configuration (your original setup with authentication)
MONGO_HOST = "localhost"
MONGO_PORT = 27018
MONGO_DB = "orchestratex"
# Your correct authentication from CONNECTION_GUIDE.md
MONGO_USERNAME = "project_admin"
MONGO_PASSWORD = "project_password"

# Global variables
mongo_client = None
db = None
model_selector = None

def connect_to_mongodb():
    """Connect to your existing MongoDB in Docker"""
    global mongo_client, db
    try:
        if mongo_available:
            # Connect to your original MongoDB with proper authentication
            mongo_client = MongoClient(
                host=MONGO_HOST,
                port=MONGO_PORT,
                username=MONGO_USERNAME,
                password=MONGO_PASSWORD,
                authSource='admin',
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            mongo_client.admin.command('ping')
            db = mongo_client[MONGO_DB]
            logger.info("✅ Connected to your ORIGINAL MongoDB with your friend's database schema!")
            return True
        else:
            logger.error("❌ PyMongo not available")
            return False
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return False

def load_model():
    """Load your trained ModelSelector"""
    global model_selector
    try:
        model_path = 'model_selector.pkl'
        if model_available and os.path.exists(model_path):
            model_selector = joblib.load(model_path)
            logger.info("✅ ModelSelector loaded successfully!")
            return True
        else:
            logger.error(f"❌ Model file not found or ModelSelector unavailable")
            return False
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        return False

def create_session(user_id, max_iterations=5):
    """Create new user session in your existing schema"""
    try:
        session_doc = {
            "user_id": user_id,
            "session_start": datetime.utcnow(),
            "max_iterations": max_iterations,
            "status": "active",
            "total_cost": 0.0,
            "settings": {
                "preferred_models": [],
                "excluded_models": [],
                "cost_limit": 10.0,
                "quality_threshold": 7.0
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.user_sessions.insert_one(session_doc)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        return None

def store_conversation_thread(session_id, prompt, model_prediction):
    """Store conversation in your existing conversation_threads collection"""
    try:
        thread_doc = {
            "session_id": ObjectId(session_id),
            "original_prompt": prompt,
            "processed_prompt": prompt,
            "domain": model_prediction.get('prompt_features', {}).get('topic_domain', 'general'),
            "complexity_level": "moderate",  # Could be enhanced with your algorithm
            "estimated_difficulty": 5.0,
            "language": "en",
            "thread_status": "active",
            "total_iterations": 1,
            "current_iteration": 1,
            "algorithm_selection": {
                "selected_model": model_prediction.get('predicted_model', 'unknown'),
                "confidence_score": model_prediction.get('prediction_confidence', 0.0),
                "selection_reasoning": f"Algorithm selected based on prompt analysis: {model_prediction.get('prompt_features', {})}"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.conversation_threads.insert_one(thread_doc)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error storing conversation thread: {e}")
        return None

def store_model_response(thread_id, model_name, response_text, prediction_data):
    """Store model response in your existing model_responses collection"""
    try:
        response_doc = {
            "thread_id": ObjectId(thread_id),
            "model_name": model_name,
            "model_version": "latest",
            "provider": "algorithm_selected",
            "iteration_number": 1,
            "prompt_tokens": len(prediction_data.get('prompt_features', {}).get('categories', [])),
            "completion_tokens": len(response_text.split()),
            "total_tokens": len(response_text.split()) + 10,
            "response_text": response_text,
            "response_time": 0.5,
            "api_cost": 0.01,
            "confidence_score": prediction_data.get('prediction_confidence', 0.0),
            "quality_metrics": {
                "coherence": 8.5,
                "relevance": 9.0,
                "accuracy": 8.0,
                "completeness": 8.5
            },
            "model_metadata": {
                "algorithm_choice": True,
                "confidence_scores": prediction_data.get('confidence_scores', {}),
                "prompt_features": prediction_data.get('prompt_features', {})
            },
            "created_at": datetime.utcnow()
        }
        
        result = db.model_responses.insert_one(response_doc)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error storing model response: {e}")
        return None

def store_algorithm_metrics(prediction_data, actual_model_used):
    """Store algorithm performance metrics in algorithm_metrics collection"""
    try:
        metrics_doc = {
            "prediction_timestamp": datetime.utcnow(),
            "predicted_model": prediction_data.get('predicted_model', 'unknown'),
            "actual_model_used": actual_model_used,
            "prediction_confidence": prediction_data.get('prediction_confidence', 0.0),
            "confidence_scores": prediction_data.get('confidence_scores', {}),
            "prompt_features": prediction_data.get('prompt_features', {}),
            "prediction_correct": prediction_data.get('predicted_model') == actual_model_used,
            "algorithm_version": "1.0",
            "created_at": datetime.utcnow()
        }
        
        result = db.algorithm_metrics.insert_one(metrics_doc)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error storing algorithm metrics: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    mongo_status = "connected" if mongo_client else "disconnected"
    model_status = "loaded" if model_selector else "not_loaded"
    
    return jsonify({
        'status': 'healthy',
        'mongodb_status': mongo_status,
        'model_status': model_status,
        'database': MONGO_DB,
        'collections': ['user_sessions', 'conversation_threads', 'model_responses', 'algorithm_metrics'],
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict_best_model():
    """Use your algorithm to predict the best model"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        if not model_selector:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Use your ModelSelector algorithm
        prediction_result = model_selector.predict_best_model(prompt)
        
        # Store algorithm metrics
        if db:
            metrics_id = store_algorithm_metrics(prediction_result, prediction_result['predicted_model'])
        
        return jsonify({
            'success': True,
            'predicted_model': prediction_result['predicted_model'],
            'confidence': prediction_result['prediction_confidence'],
            'all_model_scores': prediction_result['confidence_scores'],
            'prompt_analysis': prediction_result['prompt_features'],
            'metrics_id': metrics_id if db else None
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Handle chat with your existing MongoDB schema"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Step 1: Create session
        session_id = None
        if db:
            session_id = create_session(user_id)
        
        # Step 2: Use your algorithm to choose the best model
        if model_selector:
            prediction_result = model_selector.predict_best_model(prompt)
            chosen_model = prediction_result['predicted_model']
            confidence = prediction_result['prediction_confidence']
        else:
            prediction_result = {}
            chosen_model = 'fallback_model'
            confidence = 0.5
        
        # Step 3: Generate response (placeholder - integrate with your actual models)
        response = f"Response from {chosen_model} (confidence: {confidence:.2f}): This is a simulated response to '{prompt[:50]}...'"
        
        # Step 4: Store in your existing MongoDB collections
        thread_id = None
        response_id = None
        
        if db and session_id:
            # Store conversation thread
            thread_id = store_conversation_thread(session_id, prompt, prediction_result)
            
            # Store model response
            if thread_id:
                response_id = store_model_response(thread_id, chosen_model, response, prediction_result)
            
            # Store algorithm metrics
            store_algorithm_metrics(prediction_result, chosen_model)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'thread_id': thread_id,
            'response_id': response_id,
            'response': response,
            'model_used': chosen_model,
            'confidence': confidence,
            'stored_in_mongodb': db is not None
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Get conversations from your MongoDB"""
    try:
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 10))
        
        if not db:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Query your existing conversation_threads collection
        query = {}
        if user_id:
            # First find sessions for this user
            sessions = db.user_sessions.find({"user_id": user_id}, {"_id": 1})
            session_ids = [session["_id"] for session in sessions]
            query["session_id"] = {"$in": session_ids}
        
        conversations = list(db.conversation_threads.find(query).sort("created_at", -1).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for conv in conversations:
            conv['_id'] = str(conv['_id'])
            conv['session_id'] = str(conv['session_id'])
            if 'created_at' in conv:
                conv['created_at'] = conv['created_at'].isoformat()
            if 'updated_at' in conv:
                conv['updated_at'] = conv['updated_at'].isoformat()
        
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
    """Get algorithm analytics from MongoDB"""
    try:
        limit = int(request.args.get('limit', 10))
        
        if not db:
            return jsonify({'error': 'Database not connected'}), 500
        
        # Query your algorithm_metrics collection
        analytics = list(db.algorithm_metrics.find().sort("created_at", -1).limit(limit))
        
        # Convert ObjectId to string and format dates
        for analytic in analytics:
            analytic['_id'] = str(analytic['_id'])
            if 'created_at' in analytic:
                analytic['created_at'] = analytic['created_at'].isoformat()
            if 'prediction_timestamp' in analytic:
                analytic['prediction_timestamp'] = analytic['prediction_timestamp'].isoformat()
        
        return jsonify({
            'success': True,
            'analytics': analytics,
            'count': len(analytics)
        })
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/models', methods=['GET'])
def get_available_models():
    """Get available AI models from your MongoDB"""
    try:
        if not db:
            return jsonify({'error': 'Database not connected'}), 500
        
        models = list(db.ai_model_profiles.find({"is_active": True}))
        
        # Convert ObjectId to string and format dates
        for model in models:
            model['_id'] = str(model['_id'])
            if 'created_at' in model:
                model['created_at'] = model['created_at'].isoformat()
            if 'updated_at' in model:
                model['updated_at'] = model['updated_at'].isoformat()
        
        return jsonify({
            'success': True,
            'models': models,
            'count': len(models)
        })
        
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Smart API with MongoDB Integration...")
    
    # Connect to your existing MongoDB in Docker
    mongo_connected = connect_to_mongodb()
    if mongo_connected:
        print("✅ Connected to your Docker MongoDB!")
    else:
        print("⚠️  Running without MongoDB - check Docker setup")
    
    # Load your model
    model_loaded = load_model()
    if model_loaded:
        print("✅ Your ModelSelector is ready!")
    else:
        print("⚠️  Running without ModelSelector - using fallback mode")
    
    print(f"\n📊 MongoDB Database: {MONGO_DB}")
    print("📋 Collections: user_sessions, conversation_threads, model_responses, algorithm_metrics")
    print("\n🌐 API Endpoints:")
    print("   POST /predict - Get best model prediction")
    print("   POST /chat - Handle chat with MongoDB storage")
    print("   GET /conversations - View conversations from MongoDB")
    print("   GET /analytics - View algorithm analytics")
    print("   GET /models - View available AI models")
    print("   GET /health - Health check")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
