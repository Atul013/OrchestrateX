import requests
import json

try:
    print("Testing API connection...")
    response = requests.get('http://localhost:8002/status', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ API is accessible!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ API returned: {response.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
