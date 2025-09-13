import requests

def check_available_models():
    print("🔄 Checking available free models...")
    
    headers = {
        'Authorization': 'Bearer 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',
    }
    
    try:
        response = requests.get(
            'https://openrouter.ai/api/v1/models',
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            models = response.json()
            print("✅ Available models:")
            
            # Look for free models
            free_models = []
            for model in models['data']:
                if model.get('pricing', {}).get('prompt', '0') == '0':
                    free_models.append(model['id'])
            
            print("🆓 Free models:")
            for model in free_models[:10]:  # Show first 10
                print(f"  - {model}")
                
            return free_models
        else:
            print(f"❌ Error getting models: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_available_models()
