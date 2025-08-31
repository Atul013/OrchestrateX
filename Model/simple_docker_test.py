#!/usr/bin/env python3
"""
Simple test for Docker database storage
"""

from pymongo import MongoClient
import datetime

def test_docker_storage():
    print("🐳 Testing Your Docker Database for Response Storage")
    print("=" * 60)
    
    try:
        # Connect to your Docker MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client.orchestratex
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to Docker MongoDB!")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📋 Collections: {collections}")
        
        # Store a test response
        response_doc = {
            "user_prompt": "Test storing algorithm response",
            "algorithm_choice": "gpt4", 
            "response_text": "This response was stored by your algorithm in Docker MongoDB",
            "confidence": 0.85,
            "timestamp": datetime.datetime.utcnow()
        }
        
        result = db.model_responses.insert_one(response_doc)
        print(f"✅ Stored response: {result.inserted_id}")
        
        # Count responses
        count = db.model_responses.count_documents({})
        print(f"📊 Total responses in database: {count}")
        
        print("\n🎯 SUCCESS! Your Docker database is ready to store algorithm responses!")
        print("🌐 View data at: http://localhost:8081")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_docker_storage()
