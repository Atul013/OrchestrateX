#!/usr/bin/env python3
"""
Simple test to send a prompt via the UI interface
"""

import requests
import json
import time

def test_ui_prompt():
    """Test sending a prompt like the UI would"""
    print("🧪 Testing UI Prompt Storage")
    print("=" * 40)
    
    # This mimics what the frontend sends
    test_payload = {
        "message": "Hello from UI test - what is machine learning?",
        "session_id": f"ui_test_{int(time.time())}"
    }
    
    try:
        print(f"📤 Sending prompt: {test_payload['message']}")
        
        response = requests.post(
            "http://localhost:8002/chat", 
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Response received successfully!")
            print(f"   Primary model: {result['primary_response']['model_name']}")
            print(f"   Storage method: {result['metadata']['storage_method']}")
            print(f"   MongoDB status: {result['metadata']['mongodb_status']}")
            
            if result['metadata']['mongodb_status'] == 'connected':
                print("✅ MongoDB is connected - prompts should be stored!")
            else:
                print("❌ MongoDB not connected - prompts saved to files!")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ui_prompt()
