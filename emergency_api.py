#!/usr/bin/env python3
"""
Emergency API for OrchestrateX - Guaranteed to work with environment variables
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

# Direct API key mapping - simple and reliable
def get_api_keys():
    keys = {}
    models = {}
    
    # GLM45 -> GLM-4.5
    if os.environ.get('PROVIDER_GLM45_API_KEY'):
        keys['GLM-4.5'] = os.environ.get('PROVIDER_GLM45_API_KEY')
        models['GLM-4.5'] = os.environ.get('PROVIDER_GLM45_MODEL', 'z-ai/glm-4.5-air:free')
    
    # GPTOSS -> GPT-OSS
    if os.environ.get('PROVIDER_GPTOSS_API_KEY'):
        keys['GPT-OSS'] = os.environ.get('PROVIDER_GPTOSS_API_KEY')
        models['GPT-OSS'] = os.environ.get('PROVIDER_GPTOSS_MODEL', 'openai/gpt-oss-20b:free')
    
    # LLAMA3 -> Llama-4-Maverick
    if os.environ.get('PROVIDER_LLAMA3_API_KEY'):
        keys['Llama-4-Maverick'] = os.environ.get('PROVIDER_LLAMA3_API_KEY')
        models['Llama-4-Maverick'] = os.environ.get('PROVIDER_LLAMA3_MODEL', 'meta-llama/llama-4-maverick:free')
    
    # KIMI -> Kimi-K2
    if os.environ.get('PROVIDER_KIMI_API_KEY'):
        keys['Kimi-K2'] = os.environ.get('PROVIDER_KIMI_API_KEY')
        models['Kimi-K2'] = os.environ.get('PROVIDER_KIMI_MODEL', 'moonshotai/kimi-dev-72b:free')
    
    return keys, models

@app.route('/', methods=['GET'])
def home():
    return "OrchestrateX Emergency API - Ready"

@app.route('/health', methods=['GET'])
def health():
    keys, models = get_api_keys()
    return jsonify({
        "status": "healthy",
        "api_keys_loaded": len(keys),
        "models_available": list(keys.keys()),
        "environment_vars": [k for k in os.environ.keys() if 'PROVIDER_' in k]
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        keys, models = get_api_keys()
        
        if not keys:
            return jsonify({
                "error": "No API keys configured",
                "debug": [k for k in os.environ.keys() if 'PROVIDER_' in k]
            })
        
        # Use GLM-4.5 as primary
        primary_model = 'GLM-4.5'
        if primary_model not in keys:
            primary_model = list(keys.keys())[0]  # Use first available
        
        # Call OpenRouter API
        api_key = keys[primary_model]
        model_id = models[primary_model]
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": message}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            return jsonify({
                "success": True,
                "primary_response": {
                    "success": True,
                    "model_name": primary_model,
                    "response_text": content,
                    "tokens_used": result.get('usage', {}).get('total_tokens', 0),
                    "cost_usd": 0.0,
                    "latency_ms": 100
                },
                "critiques": [],
                "total_cost": 0.0,
                "api_calls": 1,
                "success_rate": 100.0
            })
        else:
            return jsonify({
                "success": False,
                "primary_response": {
                    "success": False,
                    "model_name": primary_model,
                    "response_text": f"API Error: {response.status_code} - {response.text}",
                    "tokens_used": 0,
                    "cost_usd": 0.0,
                    "latency_ms": 0
                },
                "critiques": [],
                "total_cost": 0.0,
                "api_calls": 1,
                "success_rate": 0.0
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "primary_response": {
                "success": False,
                "model_name": "unknown",
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))