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
API_KEY = load_api_key(env_path, "PROVIDER_GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={API_KEY}"

user_message = input("> ")
payload = {
    "contents": [
        {"parts": [{"text": user_message}]}
    ]
}

headers = {"Content-Type": "application/json"}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    result = response.json()
    try:
        print(result["candidates"][0]["content"]["parts"][0]["text"])
    except Exception:
        print(result)
else:
    print(f"Error: Request failed with status {response.status_code}")
