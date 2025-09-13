import requests
import json

def test_openrouter_api():
    print("🔄 Testing OpenRouter API...")
    
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:5176',
        'X-Title': 'OrchestrateX'
    }
    
    data = {
        'model': 'deepseek/deepseek-chat-v3.1:free',
        'messages': [
            {
                'role': 'user',
                'content': 'Hello, this is a test message'
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
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API SUCCESS!")
            print(f"Response: {result['choices'][0]['message']['content']}")
            print(f"Tokens used: {result.get('usage', {}).get('total_tokens', 'unknown')}")
        else:
            print(f"❌ API ERROR: {response.status_code}")
            print(f"Error details: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: {e}")
    except Exception as e:
        print(f"❌ GENERAL ERROR: {e}")

if __name__ == "__main__":
    test_openrouter_api()
