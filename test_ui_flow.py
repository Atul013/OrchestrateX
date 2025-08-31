#!/usr/bin/env python3
"""
Test the complete UI → Algorithm → MongoDB flow
"""

import requests
import json

def test_ui_to_mongodb():
    """Test the complete flow"""
    
    print("🧪 Testing Complete Flow:")
    print("UI Input → Algorithm → MongoDB Docker")
    print("=" * 50)
    
    # Test data (simulating UI input)
    test_cases = [
        {
            "prompt": "Write a Python function to reverse a string",
            "user_id": "ui_test_user_1"
        },
        {
            "prompt": "Tell me a creative story about space",
            "user_id": "ui_test_user_2"  
        },
        {
            "prompt": "What is machine learning?",
            "user_id": "ui_test_user_3"
        }
    ]
    
    api_url = "http://localhost:3001/process"
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📱 Test {i}: UI sends input")
        print(f"   User: {test_input['user_id']}")
        print(f"   Prompt: {test_input['prompt']}")
        
        try:
            # Send to API (simulating UI)
            response = requests.post(api_url, json=test_input, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   🤖 Algorithm chose: {result['selected_model']}")
                print(f"   📝 Response: {result['response'][:60]}...")
                print(f"   💾 Session ID: {result['session_id']}")
                print(f"   💰 Cost: ${result['cost']:.4f}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
    
    # Test analytics
    print(f"\n📊 Getting analytics...")
    try:
        analytics_response = requests.get("http://localhost:3001/analytics", timeout=5)
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print(f"   Total sessions in MongoDB: {analytics['total_sessions']}")
            print(f"   Model usage: {analytics['model_usage']}")
        else:
            print(f"   ❌ Analytics error: {analytics_response.status_code}")
    except Exception as e:
        print(f"   ❌ Analytics connection error: {e}")
    
    print(f"\n🎉 Test Complete!")
    print(f"🌐 View stored data at: http://localhost:8081 (admin/admin)")
    print(f"📊 MongoDB collection: user_sessions")

if __name__ == "__main__":
    test_ui_to_mongodb()
