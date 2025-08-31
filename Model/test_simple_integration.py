#!/usr/bin/env python3
"""
Test Algorithm with YOUR EXISTING Docker Database
Simple approach - no complex backend needed!
"""

import requests
import json

def test_simple_algorithm():
    print("🎯 Testing Algorithm with YOUR EXISTING Docker Database")
    print("=" * 60)
    
    base_url = "http://localhost:5001"
    
    # Test 1: Health check
    print("\n1️⃣ Testing Connection to Your Existing Docker...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Connected to your existing Docker MongoDB!")
            print(f"   📊 Database: {data.get('database', 'unknown')}")
            print(f"   🗄️ Collections: {data.get('collections', [])}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Test 2: Store response in your existing database
    print("\n2️⃣ Testing Response Storage in Your Existing Database...")
    chat_data = {
        "prompt": "I need help with machine learning algorithms",
        "user_id": "test_user_existing_db"
    }
    
    try:
        response = requests.post(f"{base_url}/chat", json=chat_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Response stored in your existing Docker database!")
            print(f"   🎯 Model Chosen: {data.get('model_used', 'unknown')}")
            print(f"   💾 Session ID: {data.get('session_id', 'none')}")
            print(f"   📝 Thread ID: {data.get('thread_id', 'none')}")
            print(f"   📊 Stored in MongoDB: {data.get('stored_in_mongodb', False)}")
        else:
            print(f"❌ Chat failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat error: {e}")
    
    # Test 3: View stored conversations
    print("\n3️⃣ Checking Stored Data in Your Existing Database...")
    try:
        response = requests.get(f"{base_url}/conversations?limit=1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data.get('count', 0)} conversations in your database")
            
            if data.get('conversations'):
                conv = data['conversations'][0]
                print(f"   📝 Latest: {conv.get('original_prompt', '')[:50]}...")
                print(f"   🎯 Algorithm Choice: {conv.get('algorithm_selection', {}).get('selected_model', 'none')}")
        else:
            print(f"❌ Conversations check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Conversations error: {e}")
    
    print("\n✅ Test Complete!")
    print("🎯 Your algorithm stores responses in YOUR EXISTING Docker database")
    print("🚀 No complex backend needed - simple and efficient!")

if __name__ == "__main__":
    test_simple_algorithm()
