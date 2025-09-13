#!/usr/bin/env python3
"""
Test GLM and TNG models with higher token limits like the frontend
"""
import requests
import json
import time

def test_model_with_more_tokens(model_name, model_id, api_key):
    """Test model with higher token allocation"""
    print(f"\n🧪 Testing {model_name} with higher token limit")
    print("=" * 60)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5174',
        'X-Title': 'OrchestrateX'
    }
    
    # Use a simple, direct prompt like in the frontend
    prompt = 'Quickly assess this response: "Machine learning is AI that learns from data."\n\nProvide ONLY a brief critique (2-4 words max) about depth. Examples: "Comprehensive coverage", "Surface level", "Needs detail", "Good depth".'
    
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,  # Much higher like in the frontend fix
        "temperature": 0.3   # Lower temp for reasoning models
    }
    
    try:
        print(f"📝 Prompt: {prompt[:100]}...")
        print(f"⚙️  Config: 500 tokens, temp 0.3")
        
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=30)
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print(f"✅ SUCCESS!")
            print(f"📝 Response content: '{content}'")
            print(f"📏 Content length: {len(content)}")
            print(f"🔢 Tokens used: {result.get('usage', {}).get('total_tokens', 'Unknown')}")
            print(f"🏁 Finish reason: {result['choices'][0].get('finish_reason', 'Unknown')}")
            
            # Check if there's reasoning data
            message = result['choices'][0]['message']
            if 'reasoning' in message and message['reasoning']:
                print(f"🧠 Has reasoning: {len(message['reasoning'])} chars")
                print(f"🧠 Reasoning preview: {message['reasoning'][:100]}...")
            
            return len(content.strip()) > 0
        else:
            print(f"❌ FAILED!")
            print(f"🚨 Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def main():
    print("🚀 Testing GLM-4.5 Air and TNG DeepSeek with Frontend Config")
    print("=" * 70)
    
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
    
    for model in models:
        results[model["name"]] = test_model_with_more_tokens(
            model["name"],
            model["id"], 
            model["api_key"]
        )
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    
    for model_name, has_content in results.items():
        status = "✅ PRODUCES CONTENT" if has_content else "❌ NO CONTENT"
        print(f"{model_name}: {status}")
    
    working_count = sum(results.values())
    if working_count == len(models):
        print("\n🎉 SUCCESS: Both models now produce content with higher token limits!")
        print("💡 The frontend fix should work now.")
    else:
        print(f"\n⚠️  Only {working_count}/{len(models)} models producing content")

if __name__ == "__main__":
    main()