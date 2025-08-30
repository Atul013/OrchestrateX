import requests
import json
import os

# Load API key and model from orche.env
def load_api_key(env_path, key_name):
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith(key_name + "="):
                return line.split("=", 1)[1].strip()
    raise ValueError(f"{key_name} not found in {env_path}")

env_path = os.path.join(os.path.dirname(__file__), "orche.env")
API_KEY = load_api_key(env_path, "PROVIDER_FALCON_API_KEY")
MODEL = load_api_key(env_path, "PROVIDER_FALCON_MODEL")

# OpenRouter API configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

user_message = input("> ")
payload = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": user_message}
    ],
    "max_tokens": 1000
}

try:
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print(content)
        else:
            print("Unexpected response format:", result)
    else:
        print(f"Error: Request failed with status {response.status_code}")
        print("Response:", response.text)
        
except Exception as e:
    print(f"Error: {e}")
