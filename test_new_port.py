#!/usr/bin/env python3
"""
Test MongoDB connection with new port 27017
"""

from pymongo import MongoClient
from datetime import datetime

def test_mongodb_connection():
    print("🔍 Testing MongoDB Connection on Port 27017")
    print("=" * 50)
    
    # Try different connection methods
    connection_methods = [
        {
            "name": "Standard Port (27017)",
            "url": "mongodb://localhost:27017/"
        },
        {
            "name": "With Authentication",
            "url": "mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin"
        },
        {
            "name": "Root Authentication", 
            "url": "mongodb://root:rootPassword123@localhost:27017/?authSource=admin"
        }
    ]
    
    for method in connection_methods:
        print(f"\n🧪 Testing: {method['name']}")
        try:
            client = MongoClient(method['url'], serverSelectionTimeoutMS=5000)
            
            # Test connection
            client.admin.command('ping')
            print(f"✅ Connected successfully!")
            
            # List databases
            dbs = client.list_database_names()
            print(f"📊 Available databases: {dbs}")
            
            # Test writing to orchestratex database
            db = client.orchestratex
            test_collection = db.test_connection
            
            test_doc = {
                "test_message": "Connection test successful",
                "timestamp": datetime.now(),
                "port": "27017",
                "method": method['name']
            }
            
            result = test_collection.insert_one(test_doc)
            print(f"📝 Test document inserted: {result.inserted_id}")
            
            # Count documents
            count = test_collection.count_documents({})
            print(f"📊 Total test documents: {count}")
            
            client.close()
            print(f"🎉 SUCCESS with {method['name']}!")
            return True
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            continue
    
    print("\n❌ All connection methods failed!")
    print("💡 Suggestions:")
    print("1. Make sure MongoDB is running: docker-compose up -d")
    print("2. Check if port 27017 is accessible")
    print("3. Verify MongoDB Express is working at http://localhost:8081")
    return False

if __name__ == "__main__":
    test_mongodb_connection()
