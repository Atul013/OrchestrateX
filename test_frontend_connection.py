#!/usr/bin/env python3
"""
Test the exact API call that frontend makes
"""

import requests
import json

def test_frontend_api_call():
    print("🧪 Testing Frontend → Backend Connection")
    
    # Test the exact call that the frontend makes
    url = "http://localhost:8002/chat"
    data = {"message": "Hello, this is a test message from frontend"}
    
    try:
        print(f"📤 Sending POST request to: {url}")
        print(f"📦 Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Frontend can connect to backend")
            print(f"🤖 Primary Model: {result.get('primary_response', {}).get('model_name', 'Unknown')}")
            print(f"💬 Response: {result.get('primary_response', {}).get('response_text', 'No response')[:100]}...")
            print(f"💾 Storage: {result.get('metadata', {}).get('storage_method', 'Unknown')}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot connect to localhost:8002")
        print("Make sure working_api.py is running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: API is taking too long to respond")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_frontend_api_call()
    
    if success:
        print("\n🎉 SOLUTION: Your system is working!")
        print("   Try sending a message in the frontend now.")
        print("   Frontend URL: http://localhost:5175")
    else:
        print("\n❌ ISSUE: API connection failed")
        print("   Check if working_api.py is running on port 8002")
