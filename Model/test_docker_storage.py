#!/usr/bin/env python3
"""
Test storing responses in your Docker database
"""

import requests
import json
from pymongo import MongoClient
import datetime

def test_store_response_in_docker():
    print("🐳 Testing Response Storage in Your Docker Database")
    print("=" * 60)
    
    # Test direct MongoDB connection
    print("\n1️⃣ Testing Direct MongoDB Connection...")
    try:
        client = MongoClient("mongodb://root:rootPassword123@localhost:27018/orchestratex?authSource=admin")
        db = client.orchestratex
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to Docker MongoDB!")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📋 Available Collections: {collections}")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        # Try without auth
        try:
            client = MongoClient("mongodb://localhost:27018/")
            db = client.orchestratex
            client.admin.command('ping')
            print("✅ Connected to Docker MongoDB (no auth)!")
            collections = db.list_collection_names()
            print(f"📋 Available Collections: {collections}")
        except Exception as e2:
            print(f"❌ MongoDB connection failed (no auth): {e2}")
            return
    
    # Test storing a sample response
    print("\n2️⃣ Storing Sample Response in Collections...")
    
    try:
        # Store in user_sessions
        session_doc = {
            "user_id": "test_user_docker",
            "session_start": datetime.datetime.utcnow(),
            "max_iterations": 5,
            "status": "active",
            "total_cost": 0.0,
            "created_at": datetime.datetime.utcnow()
        }
        session_result = db.user_sessions.insert_one(session_doc)
        print(f"✅ Stored user session: {session_result.inserted_id}")
        
        # Store in conversation_threads
        thread_doc = {
            "session_id": session_result.inserted_id,
            "original_prompt": "Test prompt for algorithm response storage",
            "domain": "general",
            "algorithm_selection": {
                "selected_model": "gpt4",
                "confidence_score": 0.85,
                "selection_reasoning": "Algorithm chose GPT-4 for general query"
            },
            "created_at": datetime.datetime.utcnow()
        }
        thread_result = db.conversation_threads.insert_one(thread_doc)
        print(f"✅ Stored conversation thread: {thread_result.inserted_id}")
        
        # Store in model_responses
        response_doc = {
            "thread_id": thread_result.inserted_id,
            "model_name": "gpt4",
            "response_text": "This is a test response stored in your Docker database by the algorithm",
            "confidence_score": 0.85,
            "created_at": datetime.datetime.utcnow()
        }
        response_result = db.model_responses.insert_one(response_doc)
        print(f"✅ Stored model response: {response_result.inserted_id}")
        
        # Store in algorithm_metrics
        metrics_doc = {
            "prompt": "Test prompt for algorithm response storage",
            "predicted_model": "gpt4",
            "prediction_confidence": 0.85,
            "algorithm_version": "1.0",
            "created_at": datetime.datetime.utcnow()
        }
        metrics_result = db.algorithm_metrics.insert_one(metrics_doc)
        print(f"✅ Stored algorithm metrics: {metrics_result.inserted_id}")
        
        print("\n✅ Response Storage Test Complete!")
        print("🎯 All data stored in your Docker MongoDB collections")
        print("📊 Check Mongo Express at http://localhost:8081 to view data")
        
        # Count documents in each collection
        print(f"\n📊 Collection Counts:")
        print(f"   👥 user_sessions: {db.user_sessions.count_documents({})}")
        print(f"   💬 conversation_threads: {db.conversation_threads.count_documents({})}")
        print(f"   🤖 model_responses: {db.model_responses.count_documents({})}")
        print(f"   📈 algorithm_metrics: {db.algorithm_metrics.count_documents({})}")
        
    except Exception as e:
        print(f"❌ Error storing response: {e}")

if __name__ == "__main__":
    test_store_response_in_docker()
