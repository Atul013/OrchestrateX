#!/usr/bin/env python3
"""
Test the updated frontend configuration
"""

import requests
import json

def test_frontend_api_config():
    """Test if the new API endpoints work"""
    print("🧪 Testing Updated Frontend API Configuration")
    print("=" * 60)
    
    # New API URL
    api_url = "https://orchestratex-api-84388526388.us-central1.run.app"
    
    # Test 1: Health/Status check
    print("1️⃣ Testing /status endpoint...")
    try:
        response = requests.get(f"{api_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status')}")
            print(f"   🔥 Firestore: {data.get('firestore_connected')}")
            print(f"   📊 Models: {len(data.get('models_available', []))} available")
        else:
            print(f"   ❌ Status failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Status error: {e}")
    
    # Test 2: Chat endpoint
    print("\n2️⃣ Testing /chat endpoint (like frontend will use)...")
    try:
        test_message = {
            "message": "Frontend test - checking if new API configuration works!"
        }
        
        response = requests.post(f"{api_url}/chat", json=test_message, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Chat successful!")
            print(f"   🤖 Primary model: {data.get('primary_response', {}).get('model_name')}")
            print(f"   💬 Response: {data.get('primary_response', {}).get('response_text', '')[:100]}...")
            print(f"   📈 Success rate: {data.get('success_rate')}%")
            print(f"   💰 Total cost: ${data.get('total_cost')}")
        else:
            print(f"   ❌ Chat failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Chat error: {e}")
    
    # Test 3: Analytics endpoint
    print("\n3️⃣ Testing /analytics endpoint...")
    try:
        response = requests.get(f"{api_url}/analytics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            collections = data.get('collections_summary', {})
            print(f"   ✅ Analytics working!")
            print(f"   📊 Collections data:")
            for collection, count in collections.items():
                print(f"      • {collection}: {count} documents")
        else:
            print(f"   ❌ Analytics failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Analytics error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Frontend API Configuration Updated!")
    print("🌐 Your frontend now points to:")
    print(f"   {api_url}")
    print("\n📋 Next Steps:")
    print("1. Build your frontend:")
    print("   cd FRONTEND/CHAT BOT UI/ORCHACHATBOT/project")
    print("   npm run build")
    print("2. Deploy updated frontend to your hosting service")
    print("3. Test on orchestratex.me")

if __name__ == "__main__":
    test_frontend_api_config()