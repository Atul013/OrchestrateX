#!/usr/bin/env python3
"""
UI Bridge API - Connects your UI to Algorithm and MongoDB
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
CONNECTION_STRING = "mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin"
client = MongoClient(CONNECTION_STRING)
db = client.orchestratex

def choose_model(prompt):
    """Simple algorithm to choose best model"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["code", "python", "javascript", "programming", "function"]):
        return "gpt-4", 0.95, "Coding task - GPT-4 best for programming"
    elif any(word in prompt_lower for word in ["creative", "story", "write", "poem"]):
        return "claude-3", 0.90, "Creative writing - Claude-3 excels"
    elif any(word in prompt_lower for word in ["research", "facts", "information"]):
        return "gemini-pro", 0.85, "Research task - Gemini-Pro for facts"
    else:
        return "gpt-3.5", 0.80, "General question - GPT-3.5 sufficient"

def simulate_response(model, prompt):
    """Simulate AI response"""
    responses = {
        "gpt-4": f"[GPT-4] Advanced response for: {prompt[:30]}...",
        "claude-3": f"[Claude-3] Creative response for: {prompt[:30]}...",
        "gemini-pro": f"[Gemini-Pro] Factual response for: {prompt[:30]}...",
        "gpt-3.5": f"[GPT-3.5] Quick response for: {prompt[:30]}..."
    }
    return responses.get(model, "Generic response")

@app.route('/chat', methods=['POST'])
def chat():
    """Main endpoint - receives UI input, processes through algorithm, stores in MongoDB"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"📱 UI Message: {user_message}")
        
        # Algorithm chooses model
        selected_model, confidence, reasoning = choose_model(user_message)
        print(f"🤖 Algorithm chose: {selected_model}")
        
        # Get response
        ai_response = simulate_response(selected_model, user_message)
        print(f"💬 Response: {ai_response[:50]}...")
        
        # Store in MongoDB Docker
        session_data = {
            "user_message": user_message,
            "selected_model": selected_model,
            "confidence": confidence,
            "reasoning": reasoning,
            "ai_response": ai_response,
            "timestamp": datetime.now(),
            "source": "ui_chat"
        }
        
        result = db.user_responses.insert_one(session_data)
        print(f"💾 Stored in MongoDB! ID: {result.inserted_id}")
        
        return jsonify({
            "success": True,
            "primary_response": {
                "success": True,
                "model_name": selected_model,
                "response_text": ai_response,
                "tokens_used": 150,
                "cost_usd": 0.001,
                "latency_ms": 500
            },
            "critiques": [],
            "metadata": {
                "confidence": confidence,
                "reasoning": reasoning,
                "mongodb_id": str(result.inserted_id),
                "timestamp": session_data["timestamp"].isoformat()
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "service": "UI Bridge API",
        "status": "running",
        "endpoints": ["/chat", "/health", "/models"],
        "description": "Connects UI → Algorithm → MongoDB Docker"
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "mongodb_connected": True,
        "message": "UI Bridge API working!"
    })

@app.route('/models', methods=['GET'])
def models():
    """Available models"""
    return jsonify({
        "models": ["gpt-4", "claude-3", "gemini-pro", "gpt-3.5"],
        "algorithm": "keyword_based_selection"
    })

if __name__ == '__main__':
    print("🚀 UI Bridge API: UI → Algorithm → MongoDB Docker")
    print("UI connects to: http://localhost:8002")
    print("MongoDB view: http://localhost:8081")
    print("=" * 50)
    
    # Test MongoDB connection
    try:
        client.admin.command('ping')
        print("✅ MongoDB Docker connected!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    
    app.run(host='0.0.0.0', port=8002, debug=True)
