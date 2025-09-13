#!/usr/bin/env python3
"""
Direct Flask API Server - Bypasses Unicode Issues
Direct import and minimal logging
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple print-based logging to avoid Unicode issues
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# Global orchestrator components
api_keys = {}
openrouter_api_key = None

def load_api_keys():
    """Load API keys from orche.env"""
    global api_keys, openrouter_api_key
    
    env_file = 'orche.env'
    if not os.path.exists(env_file):
        log(f"ERROR: {env_file} not found")
        return False
        
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            
        # Parse the API keys using the actual format
        lines = content.split('\n')
        temp_keys = {}
        
        for line in lines:
            line = line.strip()
            if '=' in line and not line.startswith('#') and not line.startswith('—'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if key.startswith('PROVIDER_') and key.endswith('_API_KEY'):
                    temp_keys[key] = value
                elif key.startswith('PROVIDER_') and key.endswith('_MODEL'):
                    temp_keys[key] = value
        
        # Map to model configurations
        api_keys = {
            'GLM4.5': {
                'api_key': temp_keys.get('PROVIDER_GLM45_API_KEY'),
                'model_id': temp_keys.get('PROVIDER_GLM45_MODEL')
            },
            'GPT-OSS': {
                'api_key': temp_keys.get('PROVIDER_GPTOSS_API_KEY'),
                'model_id': temp_keys.get('PROVIDER_GPTOSS_MODEL')
            },
            'Llama 4 Maverick': {
                'api_key': temp_keys.get('PROVIDER_LLAMA3_API_KEY'),
                'model_id': temp_keys.get('PROVIDER_LLAMA3_MODEL')
            },
            'MoonshotAI Kimi': {
                'api_key': temp_keys.get('PROVIDER_KIMI_API_KEY'),
                'model_id': temp_keys.get('PROVIDER_KIMI_MODEL')
            },
            'Qwen3': {
                'api_key': temp_keys.get('PROVIDER_QWEN3_API_KEY'),
                'model_id': temp_keys.get('PROVIDER_QWEN3_MODEL')
            },
            'TNG DeepSeek': {
                'api_key': temp_keys.get('PROVIDER_FALCON_API_KEY'),
                'model_id': temp_keys.get('PROVIDER_FALCON_MODEL')
            }
        }
        
        # Use any API key as the OpenRouter key (they're all OpenRouter keys)
        openrouter_api_key = api_keys['GLM4.5']['api_key']
        
        # Count valid models
        valid_models = sum(1 for model in api_keys.values() if model['api_key'] and model['model_id'])
        
        log(f"Loaded {valid_models} models with API keys and model IDs")
        return True
        
    except Exception as e:
        log(f"ERROR loading API keys: {e}")
        return False

def call_openrouter_api(model_id, prompt):
    """Direct OpenRouter API call"""
    import requests
    
    try:
        headers = {
            'Authorization': f'Bearer {openrouter_api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:8002',
            'X-Title': 'OrchestrateX'
        }
        
        data = {
            'model': model_id,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 2000,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return {'success': True, 'content': content}
        else:
            return {'success': False, 'error': f'API error {response.status_code}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def process_orchestration_simple(prompt):
    """Simple orchestration without complex logging"""
    
    # Primary model (Llama)
    primary_model = 'Llama 4 Maverick'
    
    if primary_model not in api_keys:
        return {'success': False, 'error': f'Primary model {primary_model} not configured'}
    
    primary_config = api_keys[primary_model]
    
    log(f"Processing with primary model: {primary_model}")
    
    # Get primary response
    primary_result = call_openrouter_api(primary_config['model_id'], prompt)
    
    if not primary_result['success']:
        return {
            'success': False,
            'error': f'Primary model failed: {primary_result["error"]}'
        }
    
    # Get critiques from other models
    critiques = []
    other_models = [name for name in api_keys.keys() if name != primary_model]
    
    log(f"Getting critiques from {len(other_models)} other models")
    
    for model_name in other_models[:2]:  # Limit to 2 critiques for speed
        if model_name not in api_keys:
            continue
            
        model_config = api_keys[model_name]
        critique_prompt = f"Please provide a constructive critique of this response to the prompt '{prompt[:100]}...':\n\n{primary_result['content']}"
        
        critique_result = call_openrouter_api(model_config['model_id'], critique_prompt)
        
        if critique_result['success']:
            critiques.append({
                'model_name': model_name,
                'critique': critique_result['content']
            })
    
    # Format result
    result = {
        'primary_response': {
            'model_name': primary_model,
            'content': primary_result['content'],
            'success': True
        },
        'critiques': critiques,
        'summary': {
            'primary_model': primary_model,
            'critiques_count': len(critiques),
            'total_models': len(critiques) + 1
        }
    }
    
    log(f"Orchestration completed: Primary + {len(critiques)} critiques")
    return {'success': True, 'result': result}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': len(api_keys),
        'openrouter_ready': openrouter_api_key is not None
    })

@app.route('/api/orchestration/process', methods=['POST'])
def process_orchestration():
    """Process orchestration request"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request'}), 400
        
        prompt = data['prompt']
        
        log(f"Received orchestration request: {prompt[:50]}...")
        
        if not openrouter_api_key:
            return jsonify({'error': 'OpenRouter API key not loaded'}), 500
        
        # Process the prompt
        result = process_orchestration_simple(prompt)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error'],
                'timestamp': datetime.now().isoformat()
            }), 500
        
        # Format response for frontend
        response = {
            'success': True,
            'result': result['result'],
            'timestamp': datetime.now().isoformat(),
            'models_used': result['result']['summary']['total_models']
        }
        
        log("Orchestration completed successfully")
        return jsonify(response)
        
    except Exception as e:
        log(f"Error in orchestration: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    try:
        log("=== Direct Flask API Starting ===")
        
        if not load_api_keys():
            log("Failed to load API keys. Exiting.")
            sys.exit(1)
        
        log("Starting Flask server on http://localhost:8002")
        log("Endpoints available:")
        log("  GET  /health")
        log("  POST /api/orchestration/process")
        
        # Start the server
        app.run(
            host='localhost',
            port=8002,
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        log("Server stopped by user")
    except Exception as e:
        log(f"Server error: {e}")
        sys.exit(1)
