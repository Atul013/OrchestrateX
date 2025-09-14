#!/usr/bin/env python3
"""
Docker entrypoint for OrchestrateX
Serves both frontend static files and backend API
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import sys
from datetime import datetime
import json
import asyncio

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from advanced_client import MultiModelOrchestrator
    ADVANCED_CLIENT_AVAILABLE = True
    print("✅ Advanced client available - will use real AI models")
except ImportError as e:
    ADVANCED_CLIENT_AVAILABLE = False
    print(f"⚠️ Advanced client not available: {e}")

# Create a new Flask app that combines both frontend and backend
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, origins="*", methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type'])

# Initialize the orchestrator if available
orchestrator = None
if ADVANCED_CLIENT_AVAILABLE:
    try:
        # Don't initialize here - we'll do it per request
        print("✅ Orchestrator class available")
    except Exception as e:
        print(f"❌ Failed to import orchestrator: {e}")
        ADVANCED_CLIENT_AVAILABLE = False

# Main chat endpoint (copied from super_simple_api.py)
@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Chat endpoint with AI orchestration"""
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"})
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({"error": "Empty message"}), 400
        
        print(f"📨 Received message: {message[:50]}...")
        
        if ADVANCED_CLIENT_AVAILABLE:
            # Use real AI orchestration with proper async context
            async def get_ai_response():
                async with MultiModelOrchestrator() as orch:
                    return await orch.orchestrate_with_critiques(message)
            
            # Run the async function
            result = asyncio.run(get_ai_response())
            
            return jsonify({
                "success": True,
                "primary_response": {
                    "success": True,
                    "model_name": result.primary_response.model_name,
                    "response_text": result.primary_response.response_text,
                    "tokens_used": result.primary_response.tokens_used,
                    "cost_usd": result.primary_response.cost_usd,
                    "latency_ms": result.primary_response.latency_ms
                },
                "critiques": [
                    {
                        "model_name": critique.model_name,
                        "critique_text": critique.response_text,
                        "tokens_used": critique.tokens_used,
                        "cost_usd": critique.cost_usd,
                        "latency_ms": critique.latency_ms,
                        "success": critique.success
                    }
                    for critique in result.critique_responses
                ],
                "total_cost": result.total_cost_usd,
                "api_calls": len(result.critique_responses) + 1,
                "success_rate": len([c for c in result.critique_responses if c.success]) / len(result.critique_responses) if result.critique_responses else 1.0
            })
        else:
            # Fallback demo response
            return jsonify({
                "primary_response": f"Demo response to: {message}",
                "selected_model": "Demo Model",
                "critique_responses": [],
                "total_cost_usd": 0.0,
                "processing_time_ms": 100,
                "success": True
            })
            
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e),
            "success": False
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_models": "available" if ADVANCED_CLIENT_AVAILABLE else "demo_mode",
        "version": "1.0.0"
    })

@app.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    return jsonify({
        "api": "OrchestrateX",
        "status": "running",
        "features": {
            "ai_models": ADVANCED_CLIENT_AVAILABLE,
            "intelligent_routing": True,
            "multi_model_critique": True
        }
    })

# Serve React frontend
@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files (JS, CSS, images, etc.)"""
    try:
        return send_from_directory(app.static_folder, path)
    except:
        # If file not found, serve index.html for React Router
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 8002))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("=" * 70)
    print("🚀 ORCHESTRATEX FULL-STACK CONTAINER")
    print(f"🌐 Frontend: http://{host}:{port}")
    print(f"🔌 Backend API: http://{host}:{port}/chat")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print(f"🤖 AI Models: {'✅ Available' if ADVANCED_CLIENT_AVAILABLE else '❌ Demo Mode'}")
    print("📁 Static Files: Served from /static")
    print("=" * 70)
    
    app.run(host=host, port=port, debug=debug, threaded=True)