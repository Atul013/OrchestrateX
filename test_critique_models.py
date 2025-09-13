import requests

def test_critique_models():
    print("🔄 Testing critique models...")
    
    # Test GLM-4.5 Air
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5176',
        'X-Title': 'OrchestrateX'
    }
    
    data = {
        'model': 'z-ai/glm-4.5-air:free',
        'messages': [
            {
                'role': 'user',
                'content': 'Please provide a brief critique of this response about Virat Kohli: "He is a great cricket player." Focus on what could be improved.'
            }
        ],
        'max_tokens': 100,
        'temperature': 0.7
    }
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"GLM-4.5 Air Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ GLM-4.5 Air SUCCESS!")
            print(f"Critique: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ GLM-4.5 Air ERROR: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_critique_models()
