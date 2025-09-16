#!/usr/bin/env python3
"""
Detailed diagnosis of GLM-4.5 Air and TNG DeepSeek models
"""
import requests
import json
import time

def test_model_detailed(model_name, model_id, api_key):
    """Test a specific model with multiple prompts and detailed analysis"""
    print(f"\n🔍 DETAILED TEST: {model_name} ({model_id})")
    print("=" * 70)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5174',
        'X-Title': 'OrchestrateX'
    }
    
    # Test different prompts
    test_prompts = [
        "Hello, how are you?",
        "What is 2 + 2?",
        "Write a short sentence about cats.",
        "Explain AI in one sentence."
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: '{prompt}'")
        print("-" * 50)
        
        data = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.5
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=20)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Full response structure: {json.dumps(result, indent=2)}")
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"Content length: {len(content)}")
                    print(f"Content repr: {repr(content)}")
                    
                    if content.strip():
                        print(f"✅ Got content: {content}")
                    else:
                        print("❌ Empty/whitespace only content")
                else:
                    print("❌ No choices in response")
            else:
                print(f"❌ HTTP Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

def main():
    print("🔬 DETAILED MODEL DIAGNOSIS")
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
    
    for model in models:
        test_model_detailed(model["name"], model["id"], model["api_key"])

if __name__ == "__main__":
    main()