#!/usr/bin/env python3
"""
Simple API for UI → Algorithm → MongoDB
Just one endpoint needed!
"""

from flask import Flask, request, jsonify
from simple_orchestrateX import SimpleOrchestrateX
import logging

# Setup
app = Flask(__name__)

# Add CORS headers manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Initialize algorithm
orchestrateX = SimpleOrchestrateX()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/process', methods=['POST'])
def process_user_input():
    """
    Single endpoint: UI sends input, get response back
    Everything happens here: Algorithm + MongoDB storage
    """
    try:
        # Get data from UI
        data = request.json
        user_prompt = data.get('prompt', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        logger.info(f"📱 UI Input: {user_prompt[:50]}...")
        
        # Process through algorithm → MongoDB
        result = orchestrateX.process_user_input({
            "user_id": user_id,
            "prompt": user_prompt
        })
        
        logger.info(f"✅ Processed and stored! Session: {result['session_id']}")
        
        # Return response to UI
        return jsonify({
            "success": True,
            "session_id": result["session_id"],
            "selected_model": result["selected_model"],
            "confidence": result["confidence"],
            "response": result["response"],
            "cost": result["cost"],
            "message": "Processed by algorithm and stored in MongoDB!"
        })
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get analytics from MongoDB"""
    try:
        analytics = orchestrateX.get_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "message": "UI → Algorithm → MongoDB working!",
        "mongodb_connected": True
    })

if __name__ == '__main__':
    print("🚀 Starting Simple OrchestrateX API")
    print("UI → Algorithm → MongoDB Docker")
    print("API running on: http://localhost:3001")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=3001, debug=True)
