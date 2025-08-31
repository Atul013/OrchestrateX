#!/usr/bin/env python3
"""
Test MongoDB Storage - Check if data is being stored correctly
"""

from pymongo import MongoClient
from datetime import datetime

# Connect to Docker MongoDB
CONNECTION_STRING = "mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin"

def test_mongodb_connection():
    try:
        client = MongoClient(CONNECTION_STRING)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Docker!")
        
        # Get database
        db = client.orchestratex
        
        # List all databases
        print(f"📊 Available databases: {client.list_database_names()}")
        
        # List collections in orchestratex
        collections = db.list_collection_names()
        print(f"📁 Collections in orchestratex: {collections}")
        
        # Check user_responses collection
        if 'user_responses' in collections:
            count = db.user_responses.count_documents({})
            print(f"💬 User responses count: {count}")
            
            if count > 0:
                print("\n📝 Recent user responses:")
                for doc in db.user_responses.find().limit(3):
                    print(f"  - Message: {doc.get('user_message', 'N/A')[:50]}...")
                    print(f"    Model: {doc.get('selected_model', 'N/A')}")
                    print(f"    Time: {doc.get('timestamp', 'N/A')}")
                    print(f"    ID: {doc.get('_id', 'N/A')}")
                    print("    ---")
            else:
                print("⚠️  No user responses found!")
                
        else:
            print("⚠️  user_responses collection doesn't exist yet!")
            
        # Insert a test record
        test_data = {
            "user_message": "Test from MongoDB checker",
            "selected_model": "test-model",
            "confidence": 1.0,
            "reasoning": "Test insertion",
            "ai_response": "Test response",
            "timestamp": datetime.now(),
            "source": "test_script"
        }
        
        result = db.user_responses.insert_one(test_data)
        print(f"✅ Test record inserted with ID: {result.inserted_id}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_mongodb_connection()
