#!/usr/bin/env python3
"""
Simple Direct Test - Just store data and verify in MongoDB Docker
No unnecessary APIs or UIs!
"""

from pymongo import MongoClient
from datetime import datetime

def test_direct_storage():
    print("🎯 Direct Storage Test")
    print("Just storing data → MongoDB Docker → Verify")
    print("=" * 50)
    
    # Connect to MongoDB Docker
    connection_string = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
    client = MongoClient(connection_string)
    db = client.orchestratex
    
    # Test data (simulating user input from your existing UI)
    test_data = {
        "user_id": "frontend_user",
        "user_prompt": "Write a Python function to sort a list",
        "selected_model": "gpt-4",
        "algorithm_reasoning": "Coding task - GPT-4 best for programming",
        "confidence": 0.95,
        "model_response": "def sort_list(lst): return sorted(lst)",
        "timestamp": datetime.now(),
        "source": "direct_test"
    }
    
    print(f"📝 Storing: {test_data['user_prompt']}")
    
    # Store in MongoDB
    result = db.user_responses.insert_one(test_data)
    
    print(f"✅ Stored! Document ID: {result.inserted_id}")
    
    # Verify it's actually there
    stored_doc = db.user_responses.find_one({"_id": result.inserted_id})
    
    if stored_doc:
        print(f"✅ VERIFIED: Document exists in MongoDB Docker!")
        print(f"   User: {stored_doc['user_id']}")
        print(f"   Prompt: {stored_doc['user_prompt']}")
        print(f"   Model: {stored_doc['selected_model']}")
        print(f"   Response: {stored_doc['model_response']}")
    else:
        print("❌ Document not found!")
    
    # Count total documents
    total_docs = db.user_responses.count_documents({})
    print(f"📊 Total documents in collection: {total_docs}")
    
    client.close()
    
    print(f"\n🌐 View in MongoDB Express: http://localhost:8081")
    print(f"   Login: admin/admin")
    print(f"   Database: orchestratex")
    print(f"   Collection: user_responses")

if __name__ == "__main__":
    test_direct_storage()
