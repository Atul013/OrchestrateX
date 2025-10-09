#!/usr/bin/env python3
"""
Fixed API for OrchestrateX - Simplified API key handling
Focuses on getting API keys working from environment variables
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import time
import random

app = Flask(__name__)
CORS(app)

# Simple API key mapping from environment variables
API_KEYS = {}
MODELS = {}

def load_api_keys():
    """Load API keys from environment variables"""
    global API_KEYS, MODELS
    
    providers = {
        'GLM45': 'GLM-4.5',
        'GPTOSS': 'GPT-OSS',
        'LLAMA3': 'Llama-4-Maverick',
        'KIMI': 'Kimi-K2',
        'QWEN3': 'Qwen3',
        'FALCON': 'TNG DeepSeek'
    }
    
    print("🔑 Loading API keys from environment variables...")
    
    for provider_env, model_name in providers.items():
        api_key = os.environ.get(f'PROVIDER_{provider_env}_API_KEY')
        model_id = os.environ.get(f'PROVIDER_{provider_env}_MODEL')
        
        if api_key:
            API_KEYS[model_name] = api_key.strip()
            if model_id:
                MODELS[model_name] = model_id.strip()
            print(f"✅ Loaded {model_name}: {api_key[:20]}...")
        else:
            print(f"❌ Missing {model_name}: PROVIDER_{provider_env}_API_KEY")
    
    print(f"🎯 Total API keys loaded: {len(API_KEYS)}")
    return len(API_KEYS) > 0

# Load keys on startup
load_api_keys()

def call_openrouter_api(model_id, prompt, api_key):
    """Call OpenRouter API with the given model"""
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://orchestratex.me",
            "X-Title": "OrchestrateX"
        }
        
        data = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=30)
        latency_ms = int((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            usage = result.get('usage', {})
            
            return {
                'success': True,
                'content': content,
                'tokens': usage.get('total_tokens', 0),
                'latency_ms': latency_ms
            }
        else:
            return {
                'success': False,
                'error': f"API Error {response.status_code}: {response.text}",
                'latency_ms': latency_ms
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f"Request failed: {str(e)}",
            'latency_ms': 0
        }

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "api_keys_loaded": len(API_KEYS),
        "models_available": list(API_KEYS.keys())
    })

@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    """Main orchestration endpoint"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400
        
        prompt = data['prompt']
        
        if not API_KEYS:
            return jsonify({
                "error": "No API keys available",
                "debug": {
                    "env_vars": [k for k in os.environ.keys() if 'PROVIDER_' in k]
                }
            }), 500
        
        # Select primary model (GLM-4.5 if available)
        primary_model = 'GLM-4.5' if 'GLM-4.5' in API_KEYS else random.choice(list(API_KEYS.keys()))
        primary_api_key = API_KEYS[primary_model]
        primary_model_id = MODELS.get(primary_model, "z-ai/glm-4.5-air:free")
        
        # Get primary response
        primary_result = call_openrouter_api(primary_model_id, prompt, primary_api_key)
        
        # Get critiques from other models
        critiques = []
        critique_models = [m for m in API_KEYS.keys() if m != primary_model][:3]  # Max 3 critiques
        
        for model_name in critique_models:
            api_key = API_KEYS[model_name]
            model_id = MODELS.get(model_name, "openai/gpt-3.5-turbo")
            critique_prompt = f"Provide a critique of this response: {primary_result.get('content', '')}"
            
            critique_result = call_openrouter_api(model_id, critique_prompt, api_key)
            if critique_result['success']:
                critiques.append({
                    "model_name": model_name,
                    "critique_text": critique_result['content'],
                    "tokens_used": critique_result['tokens'],
                    "cost_usd": 0.0,
                    "latency_ms": critique_result['latency_ms']
                })
        
        return jsonify({
            "success": True,
            "primary_response": {
                "success": primary_result['success'],
                "model_name": primary_model,
                "response_text": primary_result.get('content', primary_result.get('error', '')),
                "tokens_used": primary_result.get('tokens', 0),
                "cost_usd": 0.0,
                "latency_ms": primary_result.get('latency_ms', 0)
            },
            "critiques": critiques,
            "total_cost": 0.0,
            "api_calls": len(critiques) + 1,
            "success_rate": 100.0 if primary_result['success'] else 0.0,
            "debug": {
                "primary_model": primary_model,
                "primary_model_id": primary_model_id,
                "api_keys_count": len(API_KEYS)
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reload-keys', methods=['POST'])
def reload_keys():
    """Reload API keys from environment"""
    success = load_api_keys()
    return jsonify({
        "success": success,
        "keys_loaded": len(API_KEYS),
        "models": list(API_KEYS.keys())
    })

if __name__ == '__main__':
    print("🚀 Starting Fixed OrchestrateX API Server...")
    print(f"📍 API keys loaded: {len(API_KEYS)}")
    print(f"🎯 Models available: {list(API_KEYS.keys())}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))