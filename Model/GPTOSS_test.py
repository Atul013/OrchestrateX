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
API_KEY = load_api_key(env_path, "PROVIDER_GPTOSS_API_KEY")
MODEL = "openai/gpt-oss-120b:free"
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
    "max_tokens": 1000,
    "temperature": 0.7
}



response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    result = response.json()
    try:
        raw_content = result["choices"][0]["message"]["content"]
        # Clean up special tokens from GPT-OSS output
        cleaned_content = raw_content
        tokens_to_remove = ["<|start|>", "<|assistant|>", "<|channel|>", "<|final|>", "<|message|>", "<|end|>", "assistant", "final", "channel"]
        for token in tokens_to_remove:
            cleaned_content = cleaned_content.replace(token, "")
        print(cleaned_content.strip())
    except Exception:
        print(result)
else:
    print(f"Error: Request failed with status {response.status_code}")
    try:
        print(response.json())
    except Exception:
        print(response.text)