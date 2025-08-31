#!/usr/bin/env python3
"""
OrchestrateX Algorithm Response Storage API
Simple Flask API for storing AI model responses and algorithm decisions
"""

from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB connection
CONNECTION_STRING = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
client = MongoClient(CONNECTION_STRING)
db = client.orchestratex

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        client.admin.command('ping')
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/store-user-input', methods=['POST'])
def store_user_input():
    """Store user input and session data"""
    try:
        data = request.json
        
        # Create user session document
        session_doc = {
            "user_id": data.get("user_id", "anonymous"),
            "session_id": data.get("session_id"),
            "user_prompt": data.get("prompt"),
            "prompt_category": data.get("category", "general"),
            "timestamp": datetime.now(),
            "status": "received"
        }
        
        # Store in user_sessions collection
        result = db.user_sessions.insert_one(session_doc)
        
        logger.info(f"User input stored with ID: {result.inserted_id}")
        
        return jsonify({
            "status": "success",
            "session_id": str(result.inserted_id),
            "message": "User input stored successfully"
        })
        
    except Exception as e:
        logger.error(f"Error storing user input: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/store-algorithm-decision', methods=['POST'])
def store_algorithm_decision():
    """Store algorithm model selection decision"""
    try:
        data = request.json
        
        # Create algorithm decision document
        decision_doc = {
            "session_id": data.get("session_id"),
            "user_prompt": data.get("user_prompt"),
            "selected_model": data.get("selected_model"),
            "confidence_score": data.get("confidence_score"),
            "algorithm_reasoning": data.get("reasoning"),
            "available_models": data.get("available_models", []),
            "selection_criteria": data.get("criteria"),
            "timestamp": datetime.now(),
            "algorithm_version": "1.0"
        }
        
        # Store in algorithm_decisions collection
        result = db.algorithm_decisions.insert_one(decision_doc)
        
        logger.info(f"Algorithm decision stored with ID: {result.inserted_id}")
        
        return jsonify({
            "status": "success",
            "decision_id": str(result.inserted_id),
            "selected_model": data.get("selected_model"),
            "message": "Algorithm decision stored successfully"
        })
        
    except Exception as e:
        logger.error(f"Error storing algorithm decision: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/store-model-response', methods=['POST'])
def store_model_response():
    """Store AI model response"""
    try:
        data = request.json
        
        # Create model response document
        response_doc = {
            "session_id": data.get("session_id"),
            "decision_id": data.get("decision_id"),
            "model_name": data.get("model_name"),
            "model_response": data.get("response"),
            "response_time_ms": data.get("response_time"),
            "token_count": data.get("token_count"),
            "cost": data.get("cost", 0),
            "quality_score": data.get("quality_score"),
            "timestamp": datetime.now(),
            "status": "completed"
        }
        
        # Store in model_responses collection
        result = db.model_responses.insert_one(response_doc)
        
        logger.info(f"Model response stored with ID: {result.inserted_id}")
        
        return jsonify({
            "status": "success",
            "response_id": str(result.inserted_id),
            "message": "Model response stored successfully"
        })
        
    except Exception as e:
        logger.error(f"Error storing model response: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-session-data/<session_id>', methods=['GET'])
def get_session_data(session_id):
    """Retrieve complete session data"""
    try:
        # Get user session
        session = db.user_sessions.find_one({"session_id": session_id})
        
        # Get algorithm decision
        decision = db.algorithm_decisions.find_one({"session_id": session_id})
        
        # Get model response
        response = db.model_responses.find_one({"session_id": session_id})
        
        return jsonify({
            "status": "success",
            "session": session,
            "decision": decision,
            "response": response
        })
        
    except Exception as e:
        logger.error(f"Error retrieving session data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    try:
        # Count documents in each collection
        user_sessions_count = db.user_sessions.count_documents({})
        decisions_count = db.algorithm_decisions.count_documents({})
        responses_count = db.model_responses.count_documents({})
        
        # Get most used models
        pipeline = [
            {"$group": {"_id": "$selected_model", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        top_models = list(db.algorithm_decisions.aggregate(pipeline))
        
        return jsonify({
            "status": "success",
            "summary": {
                "total_sessions": user_sessions_count,
                "total_decisions": decisions_count,
                "total_responses": responses_count,
                "top_models": top_models
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        # Test connection on startup
        client.admin.command('ping')
        logger.info("✅ Connected to MongoDB successfully!")
        logger.info("🚀 Starting OrchestrateX Storage API on http://localhost:5001")
        
        app.run(host='0.0.0.0', port=5001, debug=True)
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        print("Please make sure MongoDB is running on port 27018")
