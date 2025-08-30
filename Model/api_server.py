#!/usr/bin/env python3
"""
Flask API for AI Model Selection Service
Serves the trained ModelSelector model via REST API endpoints.
"""

from flask import Flask, request, jsonify
from model_selector import ModelSelector
import logging
import traceback
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('model_selector_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global model selector instance
selector = None

def initialize_model():
    """Initialize the model selector with error handling."""
    global selector
    try:
        logger.info("Loading model selector from 'model_selector.pkl'...")
        selector = ModelSelector()
        
        model_path = 'model_selector.pkl'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found")
            
        selector.load_model(model_path)
        logger.info("✅ Model selector loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load model: {str(e)}")
        return False

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict the best AI model for a given prompt.
    
    Expected JSON input:
    {
        "prompt": "Your text prompt here"
    }
    
    Returns JSON:
    {
        "best_model": "TNG DeepSeek",
        "prediction_confidence": 0.456,
        "confidence_scores": {
            "TNG DeepSeek": 0.456,
            "GLM4.5": 0.361,
            ...
        },
        "prompt_features": {...},
        "timestamp": "2025-08-31T10:30:00"
    }
    """
    try:
        # Validate content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        # Get JSON data
        data = request.get_json()
        if data is None:
            return jsonify({
                'error': 'Invalid JSON format'
            }), 400
        
        # Validate prompt parameter
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({
                'error': 'Missing prompt parameter'
            }), 400
        
        if not isinstance(prompt, str):
            return jsonify({
                'error': 'Prompt must be a string'
            }), 400
        
        if len(prompt.strip()) == 0:
            return jsonify({
                'error': 'Prompt cannot be empty'
            }), 400
        
        # Check if model is loaded
        if selector is None:
            return jsonify({
                'error': 'Model not loaded. Server initialization failed.'
            }), 500
        
        # Get prediction
        logger.info(f"Processing prediction for prompt: '{prompt[:50]}...'")
        result = selector.select_best_model(prompt)
        
        # Prepare response
        response = {
            'best_model': result['predicted_model'],
            'prediction_confidence': round(result['prediction_confidence'], 4),
            'confidence_scores': {
                model: round(score, 4) 
                for model, score in result['confidence_scores'].items()
            },
            'prompt_features': {
                'categories': result['prompt_features']['categories'],
                'topic_domain': result['prompt_features']['topic_domain'],
                'intent_type': result['prompt_features']['intent_type'],
                'token_count': result['prompt_features']['token_count'],
                'confidence': {
                    'overall': round(result['prompt_features']['confidence']['overall'], 4)
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Prediction successful: {result['predicted_model']} (confidence: {result['prediction_confidence']:.3f})")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error during prediction',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        status = {
            'status': 'healthy' if selector is not None else 'unhealthy',
            'model_loaded': selector is not None,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        if selector is not None:
            # Test with a simple prompt
            test_result = selector.select_best_model("test prompt")
            status['test_prediction'] = test_result['predicted_model']
        
        return jsonify(status), 200 if selector is not None else 503
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

@app.route('/models', methods=['GET'])
def get_available_models():
    """Get list of available AI models."""
    try:
        if selector is None:
            return jsonify({'error': 'Model not loaded'}), 500
            
        models = selector.model_classes.tolist() if hasattr(selector.model_classes, 'tolist') else list(selector.model_classes)
        
        return jsonify({
            'available_models': models,
            'count': len(models),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve available models',
            'details': str(e)
        }), 500

@app.route('/batch', methods=['POST'])
def batch_predict():
    """
    Batch prediction for multiple prompts.
    
    Expected JSON input:
    {
        "prompts": ["prompt 1", "prompt 2", "prompt 3"]
    }
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        prompts = data.get('prompts', [])
        
        if not isinstance(prompts, list):
            return jsonify({'error': 'prompts must be a list'}), 400
        
        if len(prompts) == 0:
            return jsonify({'error': 'prompts list cannot be empty'}), 400
        
        if len(prompts) > 100:  # Limit batch size
            return jsonify({'error': 'Maximum 100 prompts allowed per batch'}), 400
        
        if selector is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        results = []
        for i, prompt in enumerate(prompts):
            if not isinstance(prompt, str) or len(prompt.strip()) == 0:
                results.append({
                    'index': i,
                    'error': 'Invalid prompt at index ' + str(i)
                })
                continue
            
            try:
                result = selector.select_best_model(prompt)
                results.append({
                    'index': i,
                    'prompt': prompt,
                    'best_model': result['predicted_model'],
                    'prediction_confidence': round(result['prediction_confidence'], 4)
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'error': f'Prediction failed: {str(e)}'
                })
        
        return jsonify({
            'results': results,
            'total_processed': len(results),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'error': 'Batch prediction failed',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'POST /predict - Single prediction',
            'POST /batch - Batch prediction',
            'GET /health - Health check',
            'GET /models - Available models'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'allowed_methods': ['GET', 'POST']
    }), 405

if __name__ == "__main__":
    print("🚀 Starting AI Model Selection API...")
    print("=" * 50)
    
    # Initialize model
    if not initialize_model():
        print("❌ Failed to initialize model. Exiting.")
        exit(1)
    
    print("📡 API Endpoints:")
    print("   POST /predict - Single prediction")
    print("   POST /batch - Batch prediction")
    print("   GET /health - Health check")
    print("   GET /models - Available models")
    print()
    print("🌐 Starting server on http://0.0.0.0:5000")
    print("   Access locally: http://localhost:5000")
    print("   Health check: http://localhost:5000/health")
    print()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        print(f"❌ Server error: {str(e)}")
