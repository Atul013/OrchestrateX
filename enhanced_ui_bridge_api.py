#!/usr/bin/env python3
"""
Enhanced UI Bridge API - Full Frontend Integration
Connects React UI to Advanced Client with Refinement Workflow
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import asyncio
import json
import sys
import os
from datetime import datetime
import logging

# Add current directory to path to import our advanced client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our advanced orchestration client
try:
    from advanced_client import MultiModelOrchestrator
    ORCHESTRATOR_AVAILABLE = True
    print("✅ Advanced orchestration client imported successfully")
except ImportError as e:
    print(f"⚠️  Warning: Could not import advanced client: {e}")
    ORCHESTRATOR_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = None

async def initialize_orchestrator():
    """Initialize the multi-model orchestrator"""
    global orchestrator
    if ORCHESTRATOR_AVAILABLE:
        try:
            orchestrator = MultiModelOrchestrator()
            await orchestrator.__aenter__()
            logger.info("🎭 Advanced orchestrator initialized")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize orchestrator: {e}")
            return False
    return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "OrchestrateX UI Bridge",
        "orchestrator_available": ORCHESTRATOR_AVAILABLE,
        "orchestrator_initialized": orchestrator is not None,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/orchestration/process', methods=['POST'])
def process_orchestration():
    """
    Enhanced orchestration endpoint that mirrors the FastAPI backend structure
    """
    try:
        data = request.json
        prompt = data.get('prompt', '')
        include_critiques = data.get('include_critiques', True)
        store_result = data.get('store_result', True)
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        logger.info(f"🎭 Processing orchestration request: '{prompt[:50]}...'")

        # Run orchestration asynchronously
        if ORCHESTRATOR_AVAILABLE and orchestrator:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    orchestrator.orchestrate_with_critiques(prompt)
                )
                
                # Format response to match frontend expectations
                response = {
                    "success": result.success,
                    "selected_model": result.selected_model,
                    "confidence_scores": result.model_confidence_scores,
                    "primary_response": {
                        "success": result.primary_response.success,
                        "model_name": result.primary_response.model_name,
                        "response_text": result.primary_response.response_text,
                        "tokens_used": result.primary_response.tokens_used,
                        "cost_usd": result.primary_response.cost_usd,
                        "latency_ms": result.primary_response.latency_ms,
                        "confidence_score": result.model_confidence_scores.get(result.selected_model, 0.0)
                    },
                    "critique_responses": [
                        {
                            "model_name": critique.model_name,
                            "response_text": critique.response_text,
                            "tokens_used": critique.tokens_used,
                            "cost_usd": critique.cost_usd,
                            "latency_ms": critique.latency_ms,
                            "success": critique.success
                        }
                        for critique in result.critique_responses
                    ],
                    "total_cost_usd": result.total_cost_usd,
                    "total_latency_ms": result.total_latency_ms,
                    "timestamp": result.timestamp,
                    "api_calls": len(result.critique_responses) + 1,
                    "success_rate": (sum(1 for c in result.critique_responses if c.success) + (1 if result.primary_response.success else 0)) / (len(result.critique_responses) + 1) * 100,
                    "original_prompt": prompt,
                    "refinement_available": len([c for c in result.critique_responses if c.success]) > 0
                }
                
                logger.info(f"✅ Orchestration completed: {result.selected_model}")
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"❌ Orchestration failed: {e}")
                return jsonify({
                    "error": "Orchestration failed",
                    "details": str(e)
                }), 500
            finally:
                loop.close()
        else:
            # Fallback to mock response
            logger.warning("⚠️  Using mock response - orchestrator not available")
            return jsonify(create_mock_response(prompt))

    except Exception as e:
        logger.error(f"❌ API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/refine', methods=['POST'])
def refine_response():
    """
    Refinement endpoint - the missing feature that was just implemented!
    """
    try:
        data = request.json
        original_result = data.get('original_result')
        selected_critique_index = data.get('selected_critique_index')
        
        if not original_result or selected_critique_index is None:
            return jsonify({"error": "Original result and critique index required"}), 400

        logger.info(f"🔄 Processing refinement request for critique index {selected_critique_index}")

        if ORCHESTRATOR_AVAILABLE and orchestrator:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Extract data for refinement
                prompt = original_result.get('original_prompt', '')
                primary_model = original_result.get('selected_model', '')
                original_response = original_result.get('primary_response', {}).get('response_text', '')
                
                critiques = original_result.get('critique_responses', [])
                if selected_critique_index >= len(critiques):
                    return jsonify({"error": "Invalid critique index"}), 400
                
                selected_critique = critiques[selected_critique_index]
                
                # Call refinement method
                refined_response = loop.run_until_complete(
                    orchestrator.refine_response_with_critique(
                        original_prompt=prompt,
                        primary_model=primary_model,
                        original_response=original_response,
                        chosen_critique=selected_critique['response_text'],
                        critique_model=selected_critique['model_name']
                    )
                )
                
                # Format refinement response
                response = {
                    "success": refined_response.success,
                    "refined_response": {
                        "model_name": refined_response.model_name,
                        "response_text": refined_response.response_text,
                        "tokens_used": refined_response.tokens_used,
                        "cost_usd": refined_response.cost_usd,
                        "latency_ms": refined_response.latency_ms,
                        "metadata": refined_response.metadata
                    },
                    "comparison": {
                        "original_length": len(original_response),
                        "refined_length": len(refined_response.response_text),
                        "improvement": refined_response.success,
                        "total_cost": original_result.get('total_cost_usd', 0) + refined_response.cost_usd
                    }
                }
                
                logger.info(f"✨ Refinement completed using {selected_critique['model_name']}'s feedback")
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"❌ Refinement failed: {e}")
                return jsonify({
                    "error": "Refinement failed",
                    "details": str(e)
                }), 500
            finally:
                loop.close()
        else:
            # Mock refinement response
            return jsonify(create_mock_refinement_response(original_result, selected_critique_index))

    except Exception as e:
        logger.error(f"❌ Refinement API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Legacy endpoint for backward compatibility"""
    try:
        data = request.json
        message = data.get('message', '')
        
        # Convert to new format and process
        return process_orchestration()
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_mock_response(prompt):
    """Create mock response when orchestrator is not available"""
    return {
        "success": True,
        "selected_model": "GPT-OSS",
        "confidence_scores": {"GPT-OSS": 0.85},
        "primary_response": {
            "success": True,
            "model_name": "GPT-OSS",
            "response_text": f"Mock response for: '{prompt}'. The advanced orchestration system is not currently connected to live AI models. To enable real responses, ensure OpenRouter API keys are configured.",
            "tokens_used": 100,
            "cost_usd": 0.0000,
            "latency_ms": 1000,
            "confidence_score": 0.85
        },
        "critique_responses": [
            {
                "model_name": "Claude-3.5-Sonnet",
                "response_text": "The response could be more detailed and include specific examples.",
                "tokens_used": 50,
                "cost_usd": 0.0000,
                "latency_ms": 800,
                "success": True
            },
            {
                "model_name": "GPT-4o",
                "response_text": "Consider adding more context and actionable advice.",
                "tokens_used": 45,
                "cost_usd": 0.0000,
                "latency_ms": 900,
                "success": True
            }
        ],
        "total_cost_usd": 0.0000,
        "total_latency_ms": 2700,
        "timestamp": datetime.now().isoformat(),
        "api_calls": 3,
        "success_rate": 100.0,
        "original_prompt": prompt,
        "refinement_available": True
    }

def create_mock_refinement_response(original_result, selected_critique_index):
    """Create mock refinement response"""
    critiques = original_result.get('critique_responses', [])
    selected_critique = critiques[selected_critique_index] if selected_critique_index < len(critiques) else {}
    
    return {
        "success": True,
        "refined_response": {
            "model_name": original_result.get('selected_model', 'GPT-OSS'),
            "response_text": f"Refined response based on {selected_critique.get('model_name', 'Unknown')} feedback: The original response has been improved with more detail, specific examples, and actionable advice as suggested.",
            "tokens_used": 150,
            "cost_usd": 0.0001,
            "latency_ms": 1200,
            "metadata": {
                "is_refinement": True,
                "critique_source": selected_critique.get('model_name', 'Unknown'),
                "original_response_length": len(original_result.get('primary_response', {}).get('response_text', '')),
            }
        },
        "comparison": {
            "original_length": len(original_result.get('primary_response', {}).get('response_text', '')),
            "refined_length": 150,
            "improvement": True,
            "total_cost": original_result.get('total_cost_usd', 0) + 0.0001
        }
    }

@app.route('/')
def status_page():
    """Status page showing system information"""
    status_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OrchestrateX UI Bridge API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { padding: 20px; border-radius: 8px; margin: 20px 0; }
            .success { background: #1a4f3a; border: 1px solid #22c55e; }
            .warning { background: #4f3a1a; border: 1px solid #eab308; }
            .error { background: #4f1a1a; border: 1px solid #ef4444; }
            .endpoint { background: #2a2a2a; padding: 15px; border-radius: 5px; margin: 10px 0; }
            h1 { color: #60a5fa; }
            h2 { color: #34d399; }
            code { background: #3a3a3a; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 OrchestrateX UI Bridge API</h1>
            <p>Enhanced backend integration for React frontend with full orchestration and refinement workflow</p>
            
            <div class="status success">
                <h3>✅ Service Status: Active</h3>
                <p>UI Bridge API is running on port 8002</p>
            </div>

            <div class="status {{ 'success' if orchestrator_available else 'warning' }}">
                <h3>🤖 Advanced Orchestrator: {{ 'Available' if orchestrator_available else 'Mock Mode' }}</h3>
                <p>{{ 'Full multi-model orchestration with refinement' if orchestrator_available else 'Using mock responses - configure OpenRouter keys for live AI' }}</p>
            </div>

            <h2>📡 API Endpoints</h2>
            
            <div class="endpoint">
                <h4>POST /api/orchestration/process</h4>
                <p>Main orchestration endpoint - processes prompts through multi-model workflow</p>
                <code>{"prompt": "Your question here", "include_critiques": true}</code>
            </div>

            <div class="endpoint">
                <h4>POST /api/orchestration/refine</h4>
                <p>Refinement endpoint - improves responses based on selected critique</p>
                <code>{"original_result": {...}, "selected_critique_index": 0}</code>
            </div>

            <div class="endpoint">
                <h4>GET /health</h4>
                <p>Health check endpoint</p>
            </div>

            <h2>🎯 Frontend Integration</h2>
            <p>This API powers the React frontend with:</p>
            <ul>
                <li>🤖 Multi-model AI orchestration</li>
                <li>📝 Real-time critique collection</li>
                <li>✨ Response refinement workflow</li>
                <li>💾 MongoDB result storage</li>
                <li>📊 Performance analytics</li>
            </ul>

            <h2>🔗 Related Services</h2>
            <ul>
                <li>Landing Page: <a href="http://localhost:5173">http://localhost:5173</a></li>
                <li>Chat UI: <a href="http://localhost:5174">http://localhost:5174</a></li>
                <li>FastAPI Backend: <a href="http://localhost:8000">http://localhost:8000</a></li>
                <li>MongoDB: mongodb://localhost:27017</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(status_html, orchestrator_available=ORCHESTRATOR_AVAILABLE)

if __name__ == '__main__':
    print("🎭 Starting OrchestrateX UI Bridge API...")
    print("="*50)
    
    # Initialize orchestrator if available
    if ORCHESTRATOR_AVAILABLE:
        print("🔄 Initializing advanced orchestrator...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(initialize_orchestrator())
        loop.close()
        
        if success:
            print("✅ Advanced orchestrator ready")
        else:
            print("⚠️  Using mock mode - orchestrator initialization failed")
    else:
        print("⚠️  Using mock mode - advanced client not available")
    
    print("\n🚀 Starting Flask server...")
    print("📡 API available at: http://localhost:8002")
    print("🎯 Status page: http://localhost:8002")
    print("="*50)
    
    app.run(host='0.0.0.0', port=8002, debug=True)
