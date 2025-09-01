import requests
import json

# Test the API
try:
    print("Testing API...")
    response = requests.post(
        "http://localhost:8002/chat",
        json={"message": "Test prompt storage", "session_id": "test_session"},
        timeout=10
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Success!")
        data = response.json()
        print(f"Storage: {data['metadata']['storage_method']}")
        print(f"MongoDB: {data['metadata']['mongodb_status']}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Exception: {e}")

# Test status endpoint
try:
    print("\nTesting status...")
    response = requests.get("http://localhost:8002/status")
    if response.status_code == 200:
        data = response.json()
        print(f"Prompts stored: {data['user_prompts_stored']}")
        print(f"MongoDB connected: {data['mongodb_connected']}")
    else:
        print(f"Status error: {response.text}")
except Exception as e:
    print(f"Status exception: {e}")
