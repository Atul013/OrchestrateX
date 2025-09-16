#!/usr/bin/env python3
"""
Backend API Only Server for OrchestrateX
Returns JSON responses only - no frontend components
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from advanced_client import MultiModelOrchestrator
    ADVANCED_CLIENT_AVAILABLE = True
    print("✅ Advanced client available - will use real AI models")
except ImportError as e:
    ADVANCED_CLIENT_AVAILABLE = False
    print(f"⚠️ Advanced client not available: {e}")

# Create Flask app for API only
app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])

@app.route("/health", methods=["GET"])
def health():
    """API health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_models": "available" if ADVANCED_CLIENT_AVAILABLE else "demo_mode",
        "service": "OrchestrateX Backend API",
        "version": "1.0.0"
    })

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    """Chat API endpoint"""
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})
    
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data["message"].strip()
        if not message:
            return jsonify({"error": "Empty message"}), 400
        
        print(f"📨 API received message: {message[:50]}...")
        
        if ADVANCED_CLIENT_AVAILABLE:
            # Use real AI orchestration
            import asyncio
            async def get_ai_response():
                orchestrator = MultiModelOrchestrator()
                return await orchestrator.process_request(message)
            
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
                "critique_responses": [{
                    "model_name": c.model_name,
                    "critique_text": c.critique_text,
                    "tokens_used": c.tokens_used,
                    "cost_usd": c.cost_usd
                } for c in result.critique_responses],
                "metadata": {
                    "total_cost_usd": result.metadata.total_cost_usd,
                    "total_tokens": result.metadata.total_tokens,
                    "processing_time_ms": result.metadata.processing_time_ms,
                    "models_used": result.metadata.models_used
                }
            })
        else:
            # Demo response
            return jsonify({
                "success": True,
                "primary_response": {
                    "success": True,
                    "model_name": "Demo Mode",
                    "response_text": f"API Backend Response to: {message}",
                    "tokens_used": 100,
                    "cost_usd": 0.001,
                    "latency_ms": 500
                },
                "critique_responses": [],
                "metadata": {
                    "total_cost_usd": 0.001,
                    "total_tokens": 100,
                    "processing_time_ms": 500,
                    "models_used": ["demo"]
                }
            })
    
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def api_root():
    """API root endpoint - should return JSON, not HTML"""
    return jsonify({
        "service": "OrchestrateX Backend API",
        "status": "running",
        "endpoints": {
            "POST /chat": "Chat with AI models",
            "GET /health": "Health check",
            "GET /": "This endpoint"
        },
        "ai_models": "available" if ADVANCED_CLIENT_AVAILABLE else "demo_mode",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print("="*50)
    print("🚀 ORCHESTRATEX BACKEND API ONLY")
    print(f"🔌 API Server: http://{host}:{port}")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print(f"🤖 AI Models: {'✅ Available' if ADVANCED_CLIENT_AVAILABLE else '❌ Demo Mode'}")
    print("📡 Returns JSON responses only")
    print("="*50)
    
    app.run(host=host, port=port, debug=False, threaded=True)