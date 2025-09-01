#!/usr/bin/env python3
"""
Debug test to check if prompts are being stored in MongoDB
"""

import requests
import json
import time
from pymongo import MongoClient

# Configuration
API_URL = "http://localhost:8002"
MONGO_URL = "mongodb://localhost:27019"

def check_mongodb_connection():
    """Check if MongoDB is connected and accessible"""
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection
        db = client.orchestratex
        print("✅ MongoDB connection successful!")
        
        # List all collections
        collections = db.list_collection_names()
        print(f"📁 Available collections: {collections}")
        
        # Check prompts collection specifically
        prompts_count = db.prompts.count_documents({})
        print(f"📝 Current prompts in database: {prompts_count}")
        
        if prompts_count > 0:
            latest_prompts = list(db.prompts.find().sort("timestamp", -1).limit(3))
            print("\n🔍 Latest prompts:")
            for i, prompt in enumerate(latest_prompts, 1):
                print(f"   {i}. {prompt.get('user_message', 'No message')[:50]}...")
                print(f"      Session: {prompt.get('session_id', 'No session')}")
                print(f"      Timestamp: {prompt.get('timestamp', 'No timestamp')}")
        
        return True, db
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False, None

def test_api_prompt_storage():
    """Test if API is storing prompts correctly"""
    print("\n🧪 Testing API prompt storage...")
    
    test_message = f"Test prompt from debug script - {int(time.time())}"
    
    payload = {
        "message": test_message,
        "session_id": f"debug_session_{int(time.time())}"
    }
    
    try:
        print(f"📤 Sending test prompt: {test_message}")
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API response received successfully!")
            print(f"   Primary model: {result['primary_response']['model_name']}")
            print(f"   Storage method: {result['metadata']['storage_method']}")
            print(f"   MongoDB status: {result['metadata']['mongodb_status']}")
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API request error: {e}")
        return False

def main():
    print("🔍 OrchestrateX Prompt Storage Debug")
    print("=" * 50)
    
    # 1. Check MongoDB connection
    mongodb_ok, db = check_mongodb_connection()
    
    if not mongodb_ok:
        print("\n❌ MongoDB not accessible - prompts won't be stored!")
        return
    
    # 2. Get initial prompt count
    initial_count = db.prompts.count_documents({})
    print(f"\n📊 Initial prompts count: {initial_count}")
    
    # 3. Test API storage
    if test_api_prompt_storage():
        # 4. Check if count increased
        time.sleep(2)  # Wait for storage to complete
        final_count = db.prompts.count_documents({})
        print(f"\n📊 Final prompts count: {final_count}")
        
        if final_count > initial_count:
            print("✅ SUCCESS: Prompt was stored in MongoDB!")
            
            # Show the newly added prompt
            latest_prompt = db.prompts.find().sort("timestamp", -1).limit(1)[0]
            print(f"\n🆕 Latest stored prompt:")
            print(f"   Message: {latest_prompt.get('user_message', 'No message')}")
            print(f"   Session: {latest_prompt.get('session_id', 'No session')}")
            print(f"   Source: {latest_prompt.get('source', 'No source')}")
            print(f"   Timestamp: {latest_prompt.get('timestamp', 'No timestamp')}")
        else:
            print("❌ PROBLEM: Prompt was NOT stored in MongoDB!")
            print("   Check API logs for errors")
    
    print("\n" + "=" * 50)
    print("Debug complete!")

if __name__ == "__main__":
    main()
