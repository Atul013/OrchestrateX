#!/usr/bin/env python3
"""
Test GLM-4.5 Air and TNG DeepSeek models directly
"""
import requests
import json
import time

def test_model(model_name, model_id, api_key, prompt):
    """Test a specific model with OpenRouter API"""
    print(f"\n🧪 Testing {model_name} ({model_id})")
    print("=" * 60)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5174',
        'X-Title': 'OrchestrateX'
    }
    
    data = {
        "model": model_id,
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            content = result['choices'][0]['message']['content']
            print(f"📝 Response: {repr(content)}")  # Use repr to show any hidden characters
            print(f"📝 Actual content: {content}")
            print(f"🔢 Tokens used: {result.get('usage', {}).get('total_tokens', 'Unknown')}")
            return True
        else:
            print(f"❌ FAILED!")
            print(f"🚨 Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def main():
    print("🚀 Testing GLM-4.5 Air and TNG DeepSeek Models")
    print("=" * 60)
    
    # Test prompt
    test_prompt = "Explain the concept of machine learning in simple terms."
    print(f"📋 Test prompt: '{test_prompt}'")
    
    # Model configurations
    models = [
        {
            "name": "GLM-4.5 Air",
            "id": "z-ai/glm-4.5-air:free",
            "api_key": "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"
        },
        {
            "name": "TNG DeepSeek",
            "id": "tngtech/deepseek-r1t2-chimera:free", 
            "api_key": "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"
        }
    ]
    
    results = {}
    
    # Test each model
    for model in models:
        results[model["name"]] = test_model(
            model["name"],
            model["id"], 
            model["api_key"],
            test_prompt
        )
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    for model_name, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED"
        print(f"{model_name}: {status}")
    
    working_count = sum(results.values())
    print(f"\n🎯 Result: {working_count}/{len(models)} models working")
    
    if working_count == len(models):
        print("🎉 All models are working correctly!")
    else:
        print("⚠️  Some models have issues - check API keys or model availability")

if __name__ == "__main__":
    main()