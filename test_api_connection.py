#!/usr/bin/env python3
"""
Quick test to verify API connection
"""

import requests
import json

def test_api():
    try:
        print("🧪 Testing OrchestrateX API Connection...")
        
        # Test basic connection
        print("1. Testing root endpoint...")
        response = requests.get('http://localhost:8002/', timeout=10)
        print(f"   ✅ Root: {response.status_code}")
        
        # Test status endpoint
        print("2. Testing status endpoint...")
        status_response = requests.get('http://localhost:8002/status', timeout=10)
        print(f"   ✅ Status: {status_response.status_code}")
        
        if status_response.status_code == 200:
            data = status_response.json()
            print(f"   📊 Storage: {data.get('storage_method', 'unknown')}")
            print(f"   🤖 Models: {len(data.get('models_available', []))} models")
            
        # Test a simple chat request
        print("3. Testing chat endpoint...")
        chat_data = {
            "message": "Hello, this is a test message",
            "user_id": "test_user"
        }
        
        chat_response = requests.post(
            'http://localhost:8002/chat', 
            json=chat_data,
            timeout=30
        )
        print(f"   ✅ Chat: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            print("   🎉 API is working perfectly!")
            print(f"   🌐 Frontend can connect to: http://localhost:8002")
        else:
            print(f"   ❌ Chat failed: {chat_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - API not running on port 8002")
    except requests.exceptions.Timeout:
        print("❌ Request timeout - API might be overloaded")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_api()
