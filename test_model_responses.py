#!/usr/bin/env python3
"""
Quick test to check model_responses collection specifically
"""

import requests
import time

def test_model_responses():
    """Test if model_responses collection is working"""
    print("🧪 Testing model_responses storage specifically...")
    
    test_data = {
        "message": f"Test for model_responses at {int(time.time())}",
        "session_id": f"test_model_responses_{int(time.time())}"
    }
    
    try:
        print(f"📤 Sending test prompt: {test_data['message']}")
        response = requests.post(
            "http://localhost:8002/chat",
            json=test_data,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Success!")
            print(f"   Primary model: {result['primary_response']['model_name']}")
            print(f"   Storage method: {result['metadata']['storage_method']}")
            print(f"   MongoDB status: {result['metadata']['mongodb_status']}")
            
            # Check the logs - they should show model_responses storage
            print("\n📋 Look at the API logs above to see if model_responses storage appears")
            print("    You should see: '✅ Stored in model_responses: [some_id]'")
            
        else:
            print(f"❌ API Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request error: {e}")

if __name__ == "__main__":
    test_model_responses()
