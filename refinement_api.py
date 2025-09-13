#!/usr/bin/env python3
"""
API endpoint for user-controlled refinement workflow
Integrates the new refinement feature into the OrchestrateX backend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import logging
from advanced_client import MultiModelOrchestrator, format_complete_result

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global orchestrator instance
orchestrator = None

@app.before_first_request
def initialize_orchestrator():
    """Initialize the orchestrator on first request"""
    global orchestrator
    if orchestrator is None:
        # Note: We'll need to handle async context properly in production
        logger.info("🚀 Initializing MultiModelOrchestrator...")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "OrchestrateX Refinement API",
        "version": "1.0.0",
        "features": ["orchestration", "critique_collection", "user_controlled_refinement"]
    })

@app.route('/orchestrate', methods=['POST'])
def orchestrate_basic():
    """Basic orchestration endpoint (original functionality)"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400
        
        prompt = data['prompt']
        logger.info(f"🎯 Basic orchestration request: {prompt[:50]}...")
        
        # Run async orchestration in sync context
        async def run_orchestration():
            async with MultiModelOrchestrator() as orch:
                return await orch.orchestrate_with_critiques(prompt)
        
        result = asyncio.run(run_orchestration())
        
        # Format for API response
        response = {
            "success": result.success,
            "prompt": result.original_prompt,
            "selected_model": result.selected_model,
            "primary_response": {
                "model": result.primary_response.model_name,
                "text": result.primary_response.response_text,
                "success": result.primary_response.success,
                "latency_ms": result.primary_response.latency_ms,
                "cost_usd": result.primary_response.cost_usd
            },
            "critiques": [
                {
                    "model": critique.model_name,
                    "text": critique.response_text,
                    "success": critique.success,
                    "confidence": critique.confidence_score,
                    "latency_ms": critique.latency_ms,
                    "cost_usd": critique.cost_usd
                }
                for critique in result.critique_responses
            ],
            "summary": {
                "total_cost_usd": result.total_cost_usd,
                "total_latency_ms": result.total_latency_ms,
                "successful_models": sum(1 for c in result.critique_responses if c.success) + (1 if result.primary_response.success else 0),
                "total_models": len(result.critique_responses) + 1
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Orchestration error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/refine', methods=['POST'])
def refine_response():
    """NEW: Refinement endpoint - refine response based on chosen critique"""
    try:
        data = request.get_json()
        required_fields = ['original_prompt', 'primary_model', 'original_response', 'chosen_critique', 'critique_model']
        
        # Validate request
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        original_prompt = data['original_prompt']
        primary_model = data['primary_model']
        original_response = data['original_response']
        chosen_critique = data['chosen_critique']
        critique_model = data['critique_model']
        
        logger.info(f"🔄 Refinement request: {primary_model} using {critique_model}'s feedback")
        
        # Run async refinement
        async def run_refinement():
            async with MultiModelOrchestrator() as orch:
                return await orch.refine_response_with_critique(
                    original_prompt=original_prompt,
                    primary_model=primary_model,
                    original_response=original_response,
                    chosen_critique=chosen_critique,
                    critique_model=critique_model
                )
        
        refined_response = asyncio.run(run_refinement())
        
        # Format response
        response = {
            "success": refined_response.success,
            "refined_response": {
                "model": refined_response.model_name,
                "text": refined_response.response_text,
                "success": refined_response.success,
                "latency_ms": refined_response.latency_ms,
                "cost_usd": refined_response.cost_usd,
                "response_type": refined_response.response_type
            },
            "metadata": {
                "original_length": len(original_response),
                "refined_length": len(refined_response.response_text),
                "critique_source": critique_model,
                "improvement_ratio": len(refined_response.response_text) / len(original_response) if original_response else 1.0
            }
        }
        
        if not refined_response.success:
            response["error"] = refined_response.error_message
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Refinement error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/orchestrate-with-refinement', methods=['POST'])
def orchestrate_with_refinement():
    """NEW: Complete workflow endpoint - orchestration + optional refinement"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request body"}), 400
        
        prompt = data['prompt']
        auto_refine = data.get('auto_refine', False)  # Whether to auto-select first critique
        critique_index = data.get('critique_index', 0)  # Which critique to use (if auto_refine)
        
        logger.info(f"🎭 Complete workflow request: {prompt[:50]}... (auto_refine: {auto_refine})")
        
        # Run async complete workflow
        async def run_complete_workflow():
            async with MultiModelOrchestrator() as orch:
                
                # Custom callback for refinement choice
                def refinement_callback(critiques):
                    if auto_refine and critiques:
                        # Auto-select specified critique index
                        index = min(critique_index, len(critiques) - 1)
                        return (index, True)
                    return (0, False)  # No refinement
                
                return await orch.orchestrate_with_user_refinement(
                    prompt=prompt,
                    user_choice_callback=refinement_callback
                )
        
        workflow_result = asyncio.run(run_complete_workflow())
        
        # Format comprehensive response
        initial = workflow_result["initial_result"]
        refined = workflow_result["refined_response"]
        
        response = {
            "success": workflow_result["stage"] == "complete",
            "stage": workflow_result["stage"],
            "prompt": prompt,
            "initial_result": {
                "selected_model": initial.selected_model,
                "primary_response": {
                    "model": initial.primary_response.model_name,
                    "text": initial.primary_response.response_text,
                    "success": initial.primary_response.success,
                    "latency_ms": initial.primary_response.latency_ms,
                    "cost_usd": initial.primary_response.cost_usd
                },
                "critiques": [
                    {
                        "model": critique.model_name,
                        "text": critique.response_text,
                        "success": critique.success,
                        "confidence": critique.confidence_score
                    }
                    for critique in initial.critique_responses if critique.success
                ]
            },
            "refinement_applied": refined is not None and refined.success,
            "final_response": {
                "text": refined.response_text if refined and refined.success else initial.primary_response.response_text,
                "model": initial.selected_model,
                "is_refined": refined is not None and refined.success,
                "critique_source": refined.metadata.get('critique_source') if refined and refined.success else None
            },
            "summary": {
                "total_cost_usd": initial.total_cost_usd + (refined.cost_usd if refined and refined.success else 0),
                "total_latency_ms": initial.total_latency_ms + (refined.latency_ms if refined and refined.success else 0),
                "models_used": len(initial.critique_responses) + 1 + (1 if refined and refined.success else 0)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Complete workflow error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/models', methods=['GET'])
def get_available_models():
    """Get list of available models"""
    try:
        # This would ideally come from the orchestrator's configuration
        available_models = [
            "TNG DeepSeek",
            "GLM4.5", 
            "GPT-OSS",
            "MoonshotAI Kimi",
            "Llama 4 Maverick",
            "Qwen3"
        ]
        
        return jsonify({
            "available_models": available_models,
            "total_models": len(available_models),
            "note": "Models require valid API keys in orche.env"
        })
        
    except Exception as e:
        logger.error(f"❌ Error getting models: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting OrchestrateX Refinement API Server...")
    print("📋 Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /models - Available models")
    print("  POST /orchestrate - Basic orchestration with critiques")
    print("  POST /refine - Refine response using chosen critique")
    print("  POST /orchestrate-with-refinement - Complete workflow")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
