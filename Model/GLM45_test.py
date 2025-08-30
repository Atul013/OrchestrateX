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
API_KEY = load_api_key(env_path, "PROVIDER_GLM45_HF_API_KEY")
MODEL = "zai-org/GLM-4.5"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

user_message = input("> ")
payload = {
    "inputs": user_message,
    "parameters": {
        "max_new_tokens": 1000,
        "return_full_text": False
    }
}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    result = response.json()
    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
        print(result[0]['generated_text'])
    else:
        print(result)
else:
    print(f"Error: Request failed with status {response.status_code}")
