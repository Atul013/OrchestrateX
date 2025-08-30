# MoonshotAI Kimi Dev 72B test script for OpenRouter
import requests
import json
import os

# Load API key from orche.env
def load_api_key(env_path, key_name):
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith(key_name + "="):
                return line.split("=", 1)[1].strip()
    raise ValueError(f"{key_name} not found in {env_path}")

env_path = os.path.join(os.path.dirname(__file__), "orche.env")
API_KEY = load_api_key(env_path, "PROVIDER_KIMI_API_KEY")
MODEL_NAME = load_api_key(env_path, "PROVIDER_KIMI_MODEL")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

user_message = input("> ")
payload = {
    "model": MODEL_NAME,
    "messages": [
        {"role": "user", "content": user_message}
    ],
    "max_tokens": 1000
}



response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    result = response.json()
    print(f"DEBUG: Response received from model: {result.get('model', 'Unknown')}")
    try:
        print("\nActual Response:")
        print(result["choices"][0]["message"]["content"])
    except Exception:
        print(result)
else:
    print(f"Error: Request failed with status {response.status_code}")
    try:
        error_response = response.json()
        print("Error details:", error_response)
    except Exception:
        print(response.text)
