#shit failed

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
API_KEY = load_api_key(env_path, "PROVIDER_ANTHROPIC_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"

headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

user_message = input("> ")
payload = {
    "model": "claude-3-5-sonnet-latest",
    "max_tokens": 1000,
    "messages": [
        {"role": "user", "content": user_message}
    ]
}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    result = response.json()
    try:
        print(result["content"][0]["text"])
    except Exception:
        print(result)
else:
    print(f"Error: Request failed with status {response.status_code}")
