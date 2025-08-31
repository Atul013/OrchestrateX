#!/usr/bin/env python3
"""
Test MongoDB Connection - Check different ports and connection strings
"""

from pymongo import MongoClient
import time

def test_mongodb_connections():
    print("🔍 Testing MongoDB Connections...")
    print("=" * 50)
    
    # Connection strings to try
    connections = [
        {
            "name": "Original (Port 27018)",
            "url": "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
        },
        {
            "name": "Standard MongoDB (Port 27017)", 
            "url": "mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin"
        },
        {
            "name": "Default MongoDB (No auth)",
            "url": "mongodb://localhost:27017/orchestratex"
        },
        {
            "name": "Docker MongoDB (Standard port)",
            "url": "mongodb://localhost:27017/"
        }
    ]
    
    working_connection = None
    
    for conn in connections:
        print(f"\n🧪 Testing: {conn['name']}")
        print(f"   URL: {conn['url']}")
        
        try:
            client = MongoClient(conn['url'], serverSelectionTimeoutMS=3000)
            # Test connection
            client.admin.command('ping')
            print(f"   ✅ SUCCESS! Connection working")
            
            # Try to list databases
            dbs = client.list_database_names()
            print(f"   📊 Available databases: {dbs}")
            
            # Check if orchestratex exists
            if 'orchestratex' in dbs:
                db = client.orchestratex
                collections = db.list_collection_names()
                print(f"   📁 Collections in orchestratex: {collections}")
            
            working_connection = conn['url']
            client.close()
            break
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
    
    if working_connection:
        print(f"\n🎯 WORKING CONNECTION FOUND:")
        print(f"   {working_connection}")
        return working_connection
    else:
        print(f"\n❌ NO WORKING CONNECTIONS FOUND")
        return None

if __name__ == "__main__":
    working_url = test_mongodb_connections()
    
    if working_url:
        print(f"\n📝 Update your APIs to use:")
        print(f'CONNECTION_STRING = "{working_url}"')
    else:
        print(f"\n🚀 Need to start MongoDB Docker:")
        print(f"   docker-compose up -d")
