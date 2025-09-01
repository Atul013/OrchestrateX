#!/usr/bin/env python3
"""
Comprehensive test to verify prompt storage in both API and MongoDB
"""

import requests
import time
from pymongo import MongoClient

def test_mongodb_direct():
    """Test MongoDB connection and check collections"""
    try:
        print("🔍 Testing MongoDB Direct Connection...")
        client = MongoClient("mongodb://localhost:27019", serverSelectionTimeoutMS=5000)
        db = client.orchestratex
        
        # Check collections
        collections = db.list_collection_names()
        print(f"📁 Collections: {collections}")
        
        # Check prompts count before
        prompts_before = db.prompts.count_documents({})
        print(f"📝 Prompts before: {prompts_before}")
        
        return True, db, prompts_before
    except Exception as e:
        print(f"❌ MongoDB error: {e}")
        return False, None, 0

def test_api_request():
    """Test API request"""
    print("\n🧪 Testing API Request...")
    
    test_data = {
        "message": f"Test prompt at {int(time.time())} - Hello AI!",
        "session_id": f"test_{int(time.time())}"
    }
    
    try:
        response = requests.post(
            "http://localhost:8002/chat",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Success!")
            print(f"   Model: {result['primary_response']['model_name']}")
            print(f"   Storage: {result['metadata']['storage_method']}")
            print(f"   MongoDB: {result['metadata']['mongodb_status']}")
            return True
        else:
            print(f"❌ API Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def test_status_endpoint():
    """Test status endpoint"""
    print("\n📊 Testing Status Endpoint...")
    
    try:
        response = requests.get("http://localhost:8002/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Status Success!")
            print(f"   Prompts stored: {data['user_prompts_stored']}")
            print(f"   Responses stored: {data['model_responses_stored']}")
            print(f"   MongoDB connected: {data['mongodb_connected']}")
            return True, data['user_prompts_stored']
        else:
            print(f"❌ Status failed: {response.status_code}")
            return False, 0
    except Exception as e:
        print(f"❌ Status error: {e}")
        return False, 0

def main():
    print("🚀 Comprehensive Prompt Storage Test")
    print("=" * 50)
    
    # 1. Test MongoDB direct
    mongo_ok, db, prompts_before = test_mongodb_direct()
    
    # 2. Test API request
    api_ok = test_api_request()
    
    # 3. Wait a moment for processing
    if api_ok:
        print("\n⏳ Waiting 3 seconds for storage to complete...")
        time.sleep(3)
    
    # 4. Test status endpoint
    status_ok, api_prompts_count = test_status_endpoint()
    
    # 5. Check MongoDB after
    if mongo_ok and db:
        print("\n🔍 Checking MongoDB After Request...")
        prompts_after = db.prompts.count_documents({})
        print(f"📝 Prompts after: {prompts_after}")
        
        if prompts_after > prompts_before:
            print("✅ SUCCESS: Prompt was stored in MongoDB!")
            
            # Show latest prompt
            latest = list(db.prompts.find().sort("timestamp", -1).limit(1))
            if latest:
                prompt = latest[0]
                print(f"\n🆕 Latest Prompt:")
                print(f"   Message: {prompt.get('user_message', 'N/A')}")
                print(f"   Session: {prompt.get('session_id', 'N/A')}")
                print(f"   Source: {prompt.get('source', 'N/A')}")
        else:
            print("❌ PROBLEM: No new prompt in MongoDB!")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print(f"   MongoDB Connected: {'✅' if mongo_ok else '❌'}")
    print(f"   API Working: {'✅' if api_ok else '❌'}")
    print(f"   Status Endpoint: {'✅' if status_ok else '❌'}")
    
    if mongo_ok and api_ok and status_ok:
        print("🎉 All systems operational!")
    else:
        print("⚠️  Some issues detected - check logs above")

if __name__ == "__main__":
    main()
