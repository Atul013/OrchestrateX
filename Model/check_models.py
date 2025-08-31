import requests
import json

# Load API key
with open("orche.env", "r") as f:
    for line in f:
        if line.strip().startswith("PROVIDER_KIMI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
if response.status_code == 200:
    models = response.json()
    print("Available MoonshotAI models:")
    for model in models['data']:
        if 'moonshot' in model['id'].lower():
            print(f"  {model['id']} - {model['name']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
