#!/usr/bin/env python3
"""
Simple MongoDB connection test for OrchestrateX
"""

from pymongo import MongoClient
import sys

def test_mongodb_connection():
    """Test connection to MongoDB"""
    try:
        # Connection string from your database documentation
        connection_string = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
        
        print("Attempting to connect to MongoDB...")
        print(f"Connection string: {connection_string}")
        
        # Create client
        client = MongoClient(connection_string)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Get database
        db = client.orchestratex
        
        # List collections
        collections = db.list_collection_names()
        print(f"📂 Available collections: {collections}")
        
        # Test a simple operation
        if 'test_collection' not in collections:
            db.test_collection.insert_one({"test": "connection working", "timestamp": "2025-08-31"})
            print("✅ Test document inserted successfully!")
        
        # Count documents
        count = db.test_collection.count_documents({})
        print(f"📊 Test collection has {count} documents")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
