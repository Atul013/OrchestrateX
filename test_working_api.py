#!/usr/bin/env python3
"""
Test the working API
"""

import requests
import json

def test_working_api():
    print("🧪 Testing Working API on localhost:8002")
    print("=" * 50)
    
    try:
        # Test status endpoint
        print("1️⃣ Testing /status endpoint...")
        status_response = requests.get('http://localhost:8002/status', timeout=5)
        print(f"Status: {status_response.status_code}")
        if status_response.status_code == 200:
            print(f"Response: {status_response.json()}")
        
        # Test chat endpoint
        print("\n2️⃣ Testing /chat endpoint...")
        chat_data = {"message": "What is machine learning?"}
        chat_response = requests.post(
            'http://localhost:8002/chat', 
            json=chat_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Chat Status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            result = chat_response.json()
            print(f"✅ SUCCESS!")
            print(f"🏆 Best Model: {result['primary_response']['model_name']}")
            print(f"💬 Response: {result['primary_response']['response_text'][:100]}...")
            print(f"⚡ Processing Time: {result['metadata']['processing_time_seconds']}s")
            print(f"📊 Total Models: {result['metadata']['total_models']}")
            print(f"💾 Session ID: {result['metadata']['session_id']}")
        else:
            print(f"❌ Chat failed: {chat_response.text}")
            
        # Test analytics
        print("\n3️⃣ Testing /analytics endpoint...")
        analytics_response = requests.get('http://localhost:8002/analytics', timeout=5)
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print(f"📊 Analytics: {analytics}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_working_api()
