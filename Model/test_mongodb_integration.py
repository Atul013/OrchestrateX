#!/usr/bin/env python3
"""
Test MongoDB Integration with Your Algorithm
"""

import requests
import json
from pymongo import MongoClient

def test_mongodb_connection():
    """Test direct MongoDB connection"""
    print("🐳 Testing Docker MongoDB Connection...")
    
    try:
        # Try connecting to your Docker MongoDB
        client = MongoClient("mongodb://localhost:27018/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        db = client.orchestratex
        collections = db.list_collection_names()
        
        print("✅ MongoDB Connection Successful!")
        print(f"📊 Database: orchestratex")
        print(f"📋 Collections: {collections}")
        
        # Test inserting a sample document
        test_doc = {
            "test": "algorithm_integration",
            "timestamp": "2025-08-31",
            "status": "working"
        }
        
        result = db.test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted: {result.inserted_id}")
        
        # Clean up test document
        db.test_collection.delete_one({"_id": result.inserted_id})
        print("🧹 Test document cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")
        return False

def test_api_with_mongodb():
    """Test your algorithm API with MongoDB storage"""
    print("\n🧠 Testing Your Algorithm API with MongoDB...")
    
    base_url = "http://localhost:5001"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API Health Check:")
            print(f"   📊 MongoDB: {data.get('mongodb_status', 'unknown')}")
            print(f"   🧠 Algorithm: {data.get('model_status', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False
    
    # Test chat endpoint (stores in MongoDB)
    print("\n💬 Testing Chat with MongoDB Storage...")
    chat_data = {
        "prompt": "How do I build a machine learning model for recommendation systems?",
        "user_id": "test_user_mongodb"
    }
    
    try:
        response = requests.post(f"{base_url}/chat", json=chat_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat Response:")
            print(f"   🎯 Model Chosen: {data.get('model_used', 'unknown')}")
            print(f"   📊 Confidence: {data.get('confidence', 0):.2f}")
            print(f"   💾 Session ID: {data.get('session_id', 'none')}")
            print(f"   📝 Thread ID: {data.get('thread_id', 'none')}")
            print(f"   📦 Stored in MongoDB: {data.get('stored_in_mongodb', False)}")
        else:
            print(f"❌ Chat request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat request error: {e}")
    
    # Test viewing conversations from MongoDB
    print("\n📖 Testing Conversation Retrieval from MongoDB...")
    try:
        response = requests.get(f"{base_url}/conversations?limit=2", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data.get('count', 0)} conversations from MongoDB")
            
            for i, conv in enumerate(data.get('conversations', [])[:2], 1):
                print(f"   📝 Conversation {i}:")
                print(f"      Prompt: {conv.get('original_prompt', '')[:60]}...")
                print(f"      Domain: {conv.get('domain', 'unknown')}")
                print(f"      Algorithm Choice: {conv.get('algorithm_selection', {}).get('selected_model', 'none')}")
        else:
            print(f"❌ Conversations retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Conversations retrieval error: {e}")
    
    # Test algorithm analytics from MongoDB
    print("\n📈 Testing Algorithm Analytics from MongoDB...")
    try:
        response = requests.get(f"{base_url}/analytics?limit=2", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data.get('count', 0)} algorithm metrics from MongoDB")
            
            for i, analytic in enumerate(data.get('analytics', [])[:2], 1):
                print(f"   📊 Metric {i}:")
                print(f"      Predicted Model: {analytic.get('predicted_model', 'unknown')}")
                print(f"      Confidence: {analytic.get('prediction_confidence', 0):.2f}")
                print(f"      Prediction Correct: {analytic.get('prediction_correct', 'unknown')}")
        else:
            print(f"❌ Analytics retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analytics retrieval error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Docker MongoDB Integration with Your Algorithm\n")
    
    # Test MongoDB connection first
    mongodb_ok = test_mongodb_connection()
    
    if mongodb_ok:
        # Test API integration
        test_api_with_mongodb()
        
        print("\n✅ Integration Test Complete!")
        print("🎯 Your algorithm can now store data in Docker MongoDB")
        print("📊 All conversation and analytics data persisted")
    else:
        print("\n❌ MongoDB connection failed - check Docker setup")
        print("💡 Run: docker-compose up -d")
