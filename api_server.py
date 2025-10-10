#!/usr/bin/env python3
"""
Simple HTTP API wrapper for OrchestrateX advanced_client.py
This creates a web service that the frontend can call.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the current directory to Python path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from orche.env FIRST
try:
    from env_loader import load_orchestratex_environment
    env_loaded = load_orchestratex_environment()
    if env_loaded:
        logger.info("✅ Environment variables loaded from orche.env")
    else:
        logger.warning("⚠️ Failed to load environment variables")
except ImportError:
    logger.warning("⚠️ env_loader not found, environment variables may not be loaded")
except Exception as e:
    logger.error(f"❌ Failed to load environment: {e}")

try:
    from advanced_client import MultiModelOrchestrator
    logger.info("✅ Successfully imported MultiModelOrchestrator")
except ImportError as e:
    logger.error(f"❌ Error importing advanced_client: {e}")
    logger.error("Make sure advanced_client.py is in the same directory")
    sys.exit(1)

app = Flask(__name__)

# Enable CORS for frontend access with specific origins
CORS(app, origins=[
    "http://localhost:3000",    # React dev server
    "http://localhost:5173",    # Vite dev server  
    "http://localhost:5175",    # Alternative Vite port
    "http://localhost:8080",    # Vue dev server
    "https://chat.orchestratex.me",  # Production frontend
    "https://orchestratex-frontend-84388526388.us-central1.run.app"  # Cloud frontend
], methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "OrchestrateX Python API",
        "backend": "advanced_client.py",
        "features": ["Real AI Model Orchestration", "OpenRouter API Integration", "Multi-Model Critiques"],
        "environment": "loaded" if 'PROVIDER_GLM45_API_KEY' in os.environ else "missing"
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for frontend compatibility"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request"}), 400
        
        message = data['message']
        session_id = data.get('session_id', 'default-session')
        
        logger.info(f"💬 Chat request: {message[:50]}...")
        
        # Use the orchestrate endpoint
        return asyncio.run(run_orchestration(message))
        
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    """Main orchestration endpoint"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        prompt = data['prompt']
        
        # Run the async orchestration
        result = asyncio.run(run_orchestration(prompt))
        
        if result is None:
            return jsonify({"error": "Orchestration failed"}), 500
        
        # Convert OrchestrationResult to dict if needed
        if hasattr(result, '__dict__'):
            result = result.__dict__
            
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in orchestrate endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

async def run_orchestration(prompt: str):
    """Run the orchestration process"""
    try:
        logger.info(f"🚀 Starting orchestration for: {prompt[:50]}...")
        
        async with MultiModelOrchestrator() as orchestrator:
            result = await orchestrator.orchestrate_with_critiques(prompt)
            
            if not result or not result.success:
                logger.error("❌ Orchestration failed")
                return jsonify({"error": "Orchestration failed"}), 500
            
            # Convert the result to the format expected by frontend
            response_data = {
                "success": True,
                "primary_response": {
                    "success": result.primary_response.success,
                    "model_name": result.primary_response.model_name,
                    "response_text": result.primary_response.response_text,
                    "tokens_used": result.primary_response.tokens_used,
                    "cost_usd": result.primary_response.cost_usd,
                    "latency_ms": result.primary_response.latency_ms
                },
                "critiques": [],
                "total_cost": result.total_cost_usd,
                "api_calls": len(result.critique_responses) + 1,
                "success_rate": 100.0 if result.success else 0.0,
                "metadata": {
                    "session_id": "python-backend",
                    "backend_type": "real_api",
                    "model_selector": "ml_based",
                    "total_models": len(result.critique_responses) + 1
                }
            }
            
            # Process critiques from critique_responses
            for critique in result.critique_responses:
                if critique.success:  # Only include successful critiques
                    response_data["critiques"].append({
                        "model_name": critique.model_name,
                        "critique_text": critique.response_text,
                        "tokens_used": critique.tokens_used,
                        "cost_usd": critique.cost_usd,
                        "latency_ms": critique.latency_ms
                    })
            
            logger.info(f"✅ Orchestration completed: {result.selected_model} primary, {len(response_data['critiques'])} critiques")
            return jsonify(response_data)
            
    except Exception as e:
        logger.error(f"❌ Error in orchestration: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting OrchestrateX Python API Server...")
    logger.info("📍 Health check: http://localhost:8000/health")
    logger.info("🎯 Orchestrate endpoint: http://localhost:8000/orchestrate")
    logger.info("💬 Chat endpoint: http://localhost:8000/chat")
    logger.info("🔗 CORS enabled for frontend access")
    logger.info("🧠 Using advanced_client.py with real AI models")
    
    # Check environment
    api_keys_count = len([k for k in os.environ.keys() if 'API_KEY' in k])
    logger.info(f"🔑 API keys available: {api_keys_count}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
