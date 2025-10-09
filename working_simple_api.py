#!/usr/bin/env python3
"""
Simple Working API for OrchestrateX - Domain Ready
Guaranteed to work with your environment variables
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import time

app = Flask(__name__)
CORS(app)

# Load API keys from environment - simple and reliable
API_KEYS = {}
MODELS = {}

def load_keys():
    global API_KEYS, MODELS
    
    # Direct mapping from your environment variables
    mappings = {
        'PROVIDER_GLM45_API_KEY': ('GLM-4.5', 'z-ai/glm-4.5-air:free'),
        'PROVIDER_GPTOSS_API_KEY': ('GPT-OSS', 'openai/gpt-oss-20b:free'),
        'PROVIDER_LLAMA3_API_KEY': ('Llama-4-Maverick', 'meta-llama/llama-4-maverick:free'),
        'PROVIDER_KIMI_API_KEY': ('Kimi-K2', 'moonshotai/kimi-dev-72b:free'),
        'PROVIDER_QWEN3_API_KEY': ('Qwen3', 'qwen/Qwen3-coder:free'),
        'PROVIDER_FALCON_API_KEY': ('TNG DeepSeek', 'tngtech/deepseek-r1t2-chimera:free')
    }
    
    for env_var, (model_name, model_id) in mappings.items():
        api_key = os.environ.get(env_var)
        if api_key:
            API_KEYS[model_name] = api_key.strip()
            MODELS[model_name] = model_id
            print(f"✅ Loaded {model_name}")
    
    print(f"🎯 Total models loaded: {len(API_KEYS)}")

# Load keys on startup
load_keys()

def call_openrouter(model_id, prompt, api_key):
    """Call OpenRouter API"""
    try:
        start_time = time.time()
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://orchestratex.me",
                "X-Title": "OrchestrateX"
            },
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000
            },
            timeout=30
        )
        
        latency = int((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            tokens = result.get('usage', {}).get('total_tokens', 0)
            
            return {
                "success": True,
                "content": content,
                "tokens": tokens,
                "latency_ms": latency
            }
        else:
            return {
                "success": False,
                "error": f"API Error {response.status_code}: {response.text[:200]}",
                "latency_ms": latency
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "latency_ms": 0
        }

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "OrchestrateX API Ready",
        "models_available": len(API_KEYS),
        "service": "working"
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "api_keys_loaded": len(API_KEYS),
        "models_available": list(API_KEYS.keys())
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not API_KEYS:
            return jsonify({
                "success": False,
                "error": "No API keys configured"
            })
        
        # Use GLM-4.5 as primary if available, otherwise first available
        primary_model = 'GLM-4.5' if 'GLM-4.5' in API_KEYS else list(API_KEYS.keys())[0]
        api_key = API_KEYS[primary_model]
        model_id = MODELS[primary_model]
        
        # Get primary response
        result = call_openrouter(model_id, message, api_key)
        
        # Get critiques from other models (max 3)
        critiques = []
        other_models = [m for m in API_KEYS.keys() if m != primary_model][:3]
        
        for model_name in other_models:
            critique_prompt = f"Provide a brief critique of this response: {result.get('content', '')[:300]}"
            critique_result = call_openrouter(MODELS[model_name], critique_prompt, API_KEYS[model_name])
            
            if critique_result['success']:
                critiques.append({
                    "model_name": model_name,
                    "critique_text": critique_result['content'],
                    "tokens_used": critique_result['tokens'],
                    "cost_usd": 0.0,
                    "latency_ms": critique_result['latency_ms']
                })
        
        # Format response for frontend compatibility
        return jsonify({
            "success": True,
            "primary_response": {
                "success": result['success'],
                "model_name": primary_model,
                "response_text": result.get('content', result.get('error', '')),
                "tokens_used": result.get('tokens', 0),
                "cost_usd": 0.0,
                "latency_ms": result.get('latency_ms', 0)
            },
            "critiques": critiques,
            "total_cost": 0.0,
            "api_calls": len(critiques) + 1,
            "success_rate": 100.0 if result['success'] else 0.0,
            "metadata": {
                "processing_time_seconds": sum(c['latency_ms'] for c in critiques) / 1000 + result.get('latency_ms', 0) / 1000,
                "total_models": len(API_KEYS),
                "session_id": f"session_{int(time.time())}"
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "primary_response": {
                "success": False,
                "model_name": "error",
                "response_text": f"Error: {str(e)}",
                "tokens_used": 0,
                "cost_usd": 0.0,
                "latency_ms": 0
            },
            "critiques": [],
            "total_cost": 0.0,
            "api_calls": 0,
            "success_rate": 0.0
        })

# Compatibility endpoints
@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    """Compatibility endpoint for /orchestrate"""
    return chat()

@app.route('/api/orchestration/process', methods=['POST'])
def process():
    """Compatibility endpoint for /api/orchestration/process"""
    return chat()

if __name__ == '__main__':
    print("🚀 OrchestrateX Working API Starting...")
    print(f"🔑 API Keys loaded: {len(API_KEYS)}")
    print(f"🎯 Models: {list(API_KEYS.keys())}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)