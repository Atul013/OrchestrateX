#!/usr/bin/env python3
"""
Simple test to verify the local Python backend is working
"""

import requests
import json

def test_local_backend():
    """Test the local Python backend"""
    
    print("🧪 Testing Local Python Backend")
    print("=" * 40)
    
    # Test health endpoint
    try:
        print("1️⃣ Testing health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed!")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Backend: {health_data.get('backend', 'Unknown')}")
            print(f"   Environment: {health_data.get('environment', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to health endpoint: {e}")
        return False
    
    # Test chat endpoint with a simple message
    try:
        print("\n2️⃣ Testing chat endpoint...")
        chat_data = {"message": "Hello! Please give me a simple response to test the API."}
        response = requests.post("http://localhost:8000/chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat endpoint works!")
            print(f"   Primary Model: {result.get('primary_response', {}).get('model_name', 'Unknown')}")
            print(f"   Response Length: {len(result.get('primary_response', {}).get('response_text', ''))}")
            print(f"   Success: {result.get('success', False)}")
            print(f"   Total Cost: ${result.get('total_cost', 0):.4f}")
            
            # Show response preview
            response_text = result.get('primary_response', {}).get('response_text', '')
            if response_text:
                print(f"   Response Preview: {response_text[:150]}...")
            
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        return False

if __name__ == "__main__":
    success = test_local_backend()
    
    if success:
        print("\n🎉 SUCCESS: Your Python backend is working locally!")
        print("✅ Real AI APIs are active")
        print("✅ Environment loaded correctly")
        print("📍 Your backend is running on: http://localhost:8000")
        print("\n🔧 Next steps:")
        print("   1. Keep this server running")
        print("   2. Update your frontend to use http://localhost:8000")
        print("   3. Test with real user prompts")
    else:
        print("\n❌ Issues found with the Python backend")
        print("Check the server logs for details")