
import requests
import json
import os

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load API key from orche.env
def load_api_key(env_path, key_name):
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith(key_name + "="):
                return line.split("=", 1)[1].strip()
    raise ValueError(f"{key_name} not found in {env_path}")

env_path = os.path.join(os.path.dirname(__file__), "orche.env")
API_KEY = load_api_key(env_path, "PROVIDER_LLAMA3_API_KEY")
MODEL = load_api_key(env_path, "PROVIDER_LLAMA3_MODEL")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# Prompt the user for input
user_message = input("> ")

payload = {
    "model": MODEL,  # Use model from environment
    "messages": [
        {"role": "user", "content": user_message}
    ],
    "max_tokens": 4000,
    "temperature": 0.7
}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error: Request failed with status {response.status_code}")
