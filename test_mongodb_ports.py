#!/usr/bin/env python3
"""
Test MongoDB connection on different ports
"""

from pymongo import MongoClient
import sys

def test_mongodb_port(port):
    try:
        print(f"🧪 Testing MongoDB on port {port}...")
        connection_string = f"mongodb://project_admin:project_password@localhost:{port}/orchestratex?authSource=admin"
        
        client = MongoClient(connection_string, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        
        print(f"✅ MongoDB is working on port {port}!")
        
        # Test database access
        db = client.orchestratex
        collections = db.list_collection_names()
        print(f"📊 Available collections: {collections}")
        
        return True, connection_string
        
    except Exception as e:
        print(f"❌ Port {port} failed: {e}")
        return False, None

def main():
    print("🔍 Finding the correct MongoDB port...")
    
    # Test common MongoDB ports
    ports_to_test = [27017, 27018, 27019]
    
    for port in ports_to_test:
        success, connection_string = test_mongodb_port(port)
        if success:
            print(f"\n🎯 FOUND IT! MongoDB is running on port {port}")
            print(f"📝 Connection string: {connection_string}")
            return port, connection_string
    
    print("\n❌ MongoDB not found on any standard port")
    print("   Try starting MongoDB with: docker-compose up -d")
    return None, None

if __name__ == "__main__":
    port, connection = main()
    if port:
        print(f"\n🔧 Update working_api.py to use port {port}")
    else:
        print("\n💡 Start MongoDB first with: start_mongodb.bat")
