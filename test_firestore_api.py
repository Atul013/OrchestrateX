#!/usr/bin/env python3
"""
Test script to verify Firestore collections are created properly
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8002"

def test_status_endpoint():
    """Test the status endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/status")
        print("🔍 Status Endpoint Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"❌ Status endpoint failed: {e}")
        return None

def test_chat_endpoint():
    """Test the chat endpoint to trigger data storage"""
    try:
        test_message = {
            "message": "Test message to verify Firestore collections are created properly. This should trigger storage in all 5 collections."
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat", 
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        
        print("💬 Chat Endpoint Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"❌ Chat endpoint failed: {e}")
        return None

def test_analytics_endpoint():
    """Test the analytics endpoint to see collection data"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics")
        print("📊 Analytics Endpoint Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"❌ Analytics endpoint failed: {e}")
        return None

def main():
    print("🚀 Testing OrchestrateX API with Firestore Collections")
    print("=" * 60)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Test 1: Check status
    print("\n1️⃣ Testing Status Endpoint...")
    status_result = test_status_endpoint()
    
    if status_result and status_result.get("firestore_connected"):
        print("✅ Firestore is connected!")
    else:
        print("⚠️ Firestore might not be connected")
    
    # Test 2: Send a chat message to trigger data storage
    print("\n2️⃣ Testing Chat Endpoint (triggers data storage)...")
    chat_result = test_chat_endpoint()
    
    if chat_result and chat_result.get("success"):
        print("✅ Chat endpoint successful - data should be stored in Firestore!")
        print(f"📝 Session ID: {chat_result.get('metadata', {}).get('session_id')}")
        print(f"🤖 Models used: {chat_result.get('metadata', {}).get('total_models')}")
    else:
        print("❌ Chat endpoint failed")
    
    # Wait a bit for data to be stored
    print("\n⏳ Waiting for data to be stored...")
    time.sleep(3)
    
    # Test 3: Check analytics to see collection counts
    print("\n3️⃣ Testing Analytics Endpoint (check collection counts)...")
    analytics_result = test_analytics_endpoint()
    
    if analytics_result:
        collections = analytics_result.get("collections_summary", {})
        print("\n📊 Firestore Collections Summary:")
        for collection, count in collections.items():
            print(f"   • {collection}: {count} documents")
    
    print("\n" + "=" * 60)
    print("🎯 Test Complete! Check the output above to verify collections were created.")

if __name__ == "__main__":
    main()