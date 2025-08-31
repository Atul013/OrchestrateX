#!/usr/bin/env python3
"""
Model Selector API Server
Provides HTTP endpoints for model selection predictions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the Model directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
        "selected_model": "GPT-OSS",
        "confidence_scores": {
            "GPT-OSS": 0.45,
            "TNG DeepSeek": 0.23,
            ...
        },
        "reasoning": "Selected based on prompt features..."
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
        
        # Get confidence scores for all models (if available)
        confidence_scores = getattr(result, 'all_confidences', {selected_model: confidence})
        
        return jsonify({
            "selected_model": selected_model,
            "confidence_scores": confidence_scores,
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
    print("🚀 Starting Model Selector API Server...")
    
    # Initialize the model
    if not initialize_model():
        print("❌ Failed to start: Could not load model")
        sys.exit(1)
    
    print("📍 Health check: http://localhost:5000/health")
    print("🎯 Prediction endpoint: http://localhost:5000/predict")
    print("📋 Models list: http://localhost:5000/models")
    print("🔗 CORS enabled for frontend access")
    
    # Start the server
    app.run(host='0.0.0.0', port=5000, debug=True)
