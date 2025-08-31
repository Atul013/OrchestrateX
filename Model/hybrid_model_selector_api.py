#!/usr/bin/env python3
"""
Enhanced Model Selector API with Hybrid Approach
Combines rule-based logic (90%+ accuracy) with ML fallback
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hybrid_model_selector import HybridModelSelector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the hybrid selector
hybrid_selector = HybridModelSelector()

@app.route('/predict', methods=['POST'])
def predict_model():
    """
    Predict the best model for a given prompt using hybrid approach.
    
    Expected JSON payload:
    {
        "prompt": "Your prompt text here",
        "use_ml_fallback": true,  // optional, default true
        "confidence_threshold": 0.75  // optional, default 0.75
    }
    
    Returns:
    {
        "model": "TNG DeepSeek",
        "confidence": 0.98,
        "method": "rule_based",
        "reasoning": "Python/ML coding expertise",
        "prompt_preview": "Write a Python function...",
        "status": "success"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'error': 'Missing prompt in request',
                'status': 'error'
            }), 400
        
        prompt = data['prompt']
        use_ml_fallback = data.get('use_ml_fallback', True)
        confidence_threshold = data.get('confidence_threshold', 0.75)
        
        # Get prediction from hybrid selector
        result = hybrid_selector.select_model(
            prompt=prompt,
            use_ml_if_low_confidence=use_ml_fallback,
            confidence_threshold=confidence_threshold
        )
        
        # Add success status
        result['status'] = 'success'
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'hybrid_model_selector_api',
        'version': '2.0',
        'has_ml_fallback': hybrid_selector.has_ml_fallback
    })

@app.route('/models', methods=['GET'])
def list_models():
    """List available models."""
    return jsonify({
        'models': [
            'TNG DeepSeek',
            'GLM4.5', 
            'GPT-OSS',
            'Qwen3',
            'MoonshotAI Kimi',
            'Llama 4 Maverick'
        ],
        'selection_methods': [
            'rule_based',
            'ml_fallback', 
            'rule_based_fallback'
        ],
        'status': 'success'
    })

@app.route('/test', methods=['GET'])
def test_predictions():
    """Test endpoint with sample predictions."""
    
    test_prompts = [
        "Write a Python function for sorting",
        "Analyze market trends", 
        "Create a story about robots",
        "Design a secure API",
        "Explain machine learning basics"
    ]
    
    results = []
    for prompt in test_prompts:
        result = hybrid_selector.select_model(prompt)
        results.append({
            'prompt': prompt,
            'prediction': result
        })
    
    return jsonify({
        'test_results': results,
        'status': 'success'
    })

if __name__ == '__main__':
    print("🚀 Starting Hybrid Model Selector API...")
    print("🎯 Rule-based + ML approach for 90%+ accuracy")
    print(f"🔧 ML Fallback Available: {hybrid_selector.has_ml_fallback}")
    print("📡 Server will run on http://localhost:5000")
    print("\n📋 Available endpoints:")
    print("  POST /predict - Get model prediction")
    print("  GET  /health  - Health check")
    print("  GET  /models  - List available models") 
    print("  GET  /test    - Test predictions")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
