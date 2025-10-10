#!/usr/bin/env python3
"""
Model Selector API Server
Provides HTTP endpoints for model selection predictions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging

# Add the Model directory and parent directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from orche.env
try:
    from env_loader import load_orchestratex_environment
    load_orchestratex_environment()
    print("✅ Environment variables loaded from orche.env")
except ImportError:
    print("⚠️ env_loader not found, environment variables may not be loaded")
except Exception as e:
    print(f"⚠️ Failed to load environment: {e}")

from model_selector import ModelSelector

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Global model selector instance
selector = None

def initialize_model():
    """Initialize the model selector with the trained model."""
    global selector
    try:
        selector = ModelSelector()
        selector.load_model('model_selector.pkl')
        print("✅ Model selector loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Model Selector API",
        "model_loaded": selector is not None
    })

@app.route('/predict', methods=['POST'])
def predict_model():
    """
    Predict the best model for a given prompt.
    
    Expected JSON payload:
    {
        "prompt": "Your prompt text here"
    }
    
    Returns:
    {
        "best_model": "GPT-OSS",
        "confidence_scores": {
            "GPT-OSS": 0.45,
            "TNG DeepSeek": 0.23,
            ...
        },
        "prediction_confidence": 0.45
    }
    """
    try:
        if selector is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        prompt = data['prompt']
        
        # Get prediction from model
        result = selector.predict(prompt)
        
        # Extract the model name and confidence
        selected_model = result['model']
        confidence = result['confidence']
        
        # Create confidence scores for all models (required by advanced_client.py)
        confidence_scores = {
            "GPT-OSS": 0.25,
            "TNG DeepSeek": 0.25, 
            "GLM4.5": 0.25,
            "MoonshotAI Kimi": 0.25,
            "Llama 4 Maverick": 0.25,
            "Qwen3": 0.25
        }
        
        # Set higher confidence for selected model
        if selected_model in confidence_scores:
            confidence_scores[selected_model] = confidence
            # Distribute remaining confidence among other models
            remaining = (1.0 - confidence) / (len(confidence_scores) - 1)
            for model in confidence_scores:
                if model != selected_model:
                    confidence_scores[model] = remaining
        
        return jsonify({
            "best_model": selected_model,
            "confidence_scores": confidence_scores,
            "prediction_confidence": confidence,
            "reasoning": f"Selected {selected_model} with {confidence:.3f} confidence based on prompt analysis",
            "success": True
        })
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/models', methods=['GET'])
def list_models():
    """List all available models that can be selected."""
    models = [
        "GPT-OSS",
        "TNG DeepSeek", 
        "GLM4.5",
        "MoonshotAI Kimi",
        "Llama 4 Maverick",
        "Qwen3"
    ]
    return jsonify({
        "available_models": models,
        "total_count": len(models)
    })

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Model Selector API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    args = parser.parse_args()
    
    print("🚀 Starting Model Selector API Server...")
    
    # Initialize the model
    if not initialize_model():
        print("❌ Failed to start: Could not load model")
        sys.exit(1)
    
    print(f"📍 Health check: http://localhost:{args.port}/health")
    print(f"🎯 Prediction endpoint: http://localhost:{args.port}/predict")
    print(f"📋 Models list: http://localhost:{args.port}/models")
    print("🔗 CORS enabled for frontend access")
    
    # Start the server
    app.run(host='0.0.0.0', port=args.port, debug=False)
