import requests
import json

print("🧪 Testing OrchestrateX API Endpoints")
print("=" * 50)

# Test 1: Check if API is running
try:
    response = requests.get("http://localhost:8002/", timeout=5)
    if response.status_code == 200:
        print("✅ API is running!")
        data = response.json()
        print(f"   Service: {data.get('service', 'Unknown')}")
    else:
        print(f"❌ API not responding: {response.status_code}")
except Exception as e:
    print(f"❌ API connection failed: {e}")

print()

# Test 2: Check status endpoint
try:
    response = requests.get("http://localhost:8002/status", timeout=10)
    if response.status_code == 200:
        print("✅ Status endpoint working!")
        data = response.json()
        print(f"   MongoDB connected: {data.get('mongodb_connected', False)}")
        print(f"   Prompts stored: {data.get('user_prompts_stored', 0)}")
        print(f"   Responses stored: {data.get('model_responses_stored', 0)}")
        print(f"   Storage method: {data.get('storage_method', 'Unknown')}")
    else:
        print(f"❌ Status failed: {response.status_code}")
except Exception as e:
    print(f"❌ Status error: {e}")

print()

# Test 3: Send a test prompt
try:
    print("📤 Sending test prompt...")
    test_data = {
        "message": "Hello, this is a test prompt to check storage",
        "session_id": "test_session_check"
    }
    
    response = requests.post("http://localhost:8002/chat", json=test_data, timeout=15)
    if response.status_code == 200:
        print("✅ Chat request successful!")
        data = response.json()
        print(f"   Primary model: {data['primary_response']['model_name']}")
        print(f"   Storage: {data['metadata']['storage_method']}")
        print(f"   MongoDB: {data['metadata']['mongodb_status']}")
    else:
        print(f"❌ Chat failed: {response.status_code}")
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"❌ Chat error: {e}")

print("\n" + "=" * 50)
print("💡 If everything shows ✅, then prompts should be stored!")
print("💡 Check MongoDB Express at http://localhost:8081 (admin/admin)")
print("💡 Look for the 'orchestratex' database and 'prompts' collection")
