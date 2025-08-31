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

# Add the current directory to Python path to import advanced_client
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from advanced_client import MultiModelOrchestrator
except ImportError as e:
    print(f"Error importing advanced_client: {e}")
    print("Make sure advanced_client.py is in the same directory")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "OrchestrateX API"})

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
        async with MultiModelOrchestrator() as orchestrator:
            result = await orchestrator.orchestrate_with_critiques(prompt)
            
            # Result is already an OrchestrationResult object, convert to dict for JSON
            if hasattr(result, '__dict__'):
                result_dict = result.__dict__
            else:
                result_dict = result
            
            # Convert the result to the format expected by frontend
            response_data = {
                "success": True,
                "primary_response": {
                    "success": result_dict["primary_response"].success,
                    "model_name": result_dict["primary_response"].model_name,
                    "response_text": result_dict["primary_response"].response_text,
                    "tokens_used": result_dict["primary_response"].tokens_used,
                    "cost_usd": result_dict["primary_response"].cost_usd,
                    "latency_ms": result_dict["primary_response"].latency_ms
                },
                "critiques": [],
                "total_cost": result_dict.get("total_cost_usd", 0.0),
                "api_calls": len(result_dict.get("critique_responses", [])) + 1,
                "success_rate": (result_dict["success"] and 100.0) or 0.0
            }
            
            # Process critiques from critique_responses
            if "critique_responses" in result_dict:
                for critique in result_dict["critique_responses"]:
                    if critique.success:  # Only include successful critiques
                        response_data["critiques"].append({
                            "model_name": critique.model_name,
                            "critique_text": critique.response_text,
                            "tokens_used": critique.tokens_used,
                            "cost_usd": critique.cost_usd,
                            "latency_ms": critique.latency_ms
                        })
            
            return response_data
            
    except Exception as e:
        print(f"Error in orchestration: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    print("🚀 Starting OrchestrateX API Server...")
    print("📍 Health check: http://localhost:8000/health")
    print("🎯 Orchestrate endpoint: http://localhost:8000/orchestrate")
    print("🔗 CORS enabled for frontend access")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=True)
