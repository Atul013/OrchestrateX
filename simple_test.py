import requests
import json

print("Testing API connection...")

try:
    # Test home endpoint first
    print("1. Testing home endpoint...")
    response = requests.get("http://localhost:8002/", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    
    # Test chat endpoint
    print("\n2. Testing chat endpoint...")
    chat_data = {
        "message": "Simple test message",
        "session_id": "test_session_123"
    }
    
    response = requests.post(
        "http://localhost:8002/chat",
        json=chat_data,
        headers={"Content-Type": "application/json"},
        timeout=20
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Success: {result.get('success', False)}")
        print(f"   Storage: {result['metadata']['storage_method']}")
        print(f"   MongoDB: {result['metadata']['mongodb_status']}")
    else:
        print(f"   Error: {response.text}")

except Exception as e:
    print(f"Error: {e}")
