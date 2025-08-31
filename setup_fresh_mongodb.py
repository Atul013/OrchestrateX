#!/usr/bin/env python3
"""
Fresh MongoDB Setup & Connection Test
Fix the network/port issues
"""

import subprocess
import time
from pymongo import MongoClient
import requests

def start_fresh_mongodb():
    """Start MongoDB with fresh setup"""
    print("🐳 Setting up fresh MongoDB Docker...")
    
    # Stop any existing MongoDB containers
    try:
        subprocess.run(["docker", "stop", "mongodb"], capture_output=True)
        subprocess.run(["docker", "rm", "mongodb"], capture_output=True)
        print("✅ Cleaned up old containers")
    except:
        print("ℹ️  No existing containers to clean")
    
    # Start fresh MongoDB container on standard port
    mongodb_command = [
        "docker", "run", "-d",
        "--name", "mongodb",
        "-p", "27017:27017",  # Using standard MongoDB port
        "-e", "MONGO_INITDB_ROOT_USERNAME=admin",
        "-e", "MONGO_INITDB_ROOT_PASSWORD=password123",
        "-v", "mongodb_data:/data/db",
        "mongo:latest"
    ]
    
    try:
        result = subprocess.run(mongodb_command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MongoDB started on port 27017")
            print(f"   Container ID: {result.stdout.strip()}")
        else:
            print(f"❌ Failed to start MongoDB: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error starting MongoDB: {e}")
        return False
    
    # Wait for MongoDB to be ready
    print("⏳ Waiting for MongoDB to initialize...")
    time.sleep(10)
    
    return True

def test_mongodb_connection():
    """Test the new MongoDB connection"""
    print("\n🧪 Testing MongoDB connection...")
    
    # New connection string for standard port
    connection_string = "mongodb://admin:password123@localhost:27017/orchestratex?authSource=admin"
    
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Create test database and collection
        db = client.orchestratex
        test_doc = {
            "test": "Fresh MongoDB setup working",
            "timestamp": "2025-08-31",
            "status": "connected"
        }
        
        result = db.test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted: {result.inserted_id}")
        
        # List databases
        databases = client.list_database_names()
        print(f"📊 Available databases: {databases}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def start_mongo_express():
    """Start MongoDB Express admin interface"""
    print("\n🌐 Starting MongoDB Express admin interface...")
    
    # Stop existing mongo-express
    try:
        subprocess.run(["docker", "stop", "mongo-express"], capture_output=True)
        subprocess.run(["docker", "rm", "mongo-express"], capture_output=True)
    except:
        pass
    
    # Start mongo-express
    express_command = [
        "docker", "run", "-d",
        "--name", "mongo-express",
        "-p", "8081:8081",
        "-e", "ME_CONFIG_MONGODB_ADMINUSERNAME=admin",
        "-e", "ME_CONFIG_MONGODB_ADMINPASSWORD=password123",
        "-e", "ME_CONFIG_MONGODB_URL=mongodb://admin:password123@host.docker.internal:27017/",
        "-e", "ME_CONFIG_BASICAUTH_USERNAME=admin",
        "-e", "ME_CONFIG_BASICAUTH_PASSWORD=admin",
        "mongo-express:latest"
    ]
    
    try:
        result = subprocess.run(express_command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MongoDB Express started on port 8081")
            print("🌐 Access at: http://localhost:8081 (admin/admin)")
        else:
            print(f"❌ Failed to start MongoDB Express: {result.stderr}")
    except Exception as e:
        print(f"❌ Error starting MongoDB Express: {e}")

def main():
    """Main setup function"""
    print("🚀 Fresh MongoDB Setup for OrchestrateX")
    print("=" * 50)
    
    # Step 1: Start fresh MongoDB
    if not start_fresh_mongodb():
        return
    
    # Step 2: Test connection
    if not test_mongodb_connection():
        return
    
    # Step 3: Start admin interface
    start_mongo_express()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("📊 MongoDB: mongodb://admin:password123@localhost:27017/orchestratex?authSource=admin")
    print("🌐 Admin UI: http://localhost:8081 (admin/admin)")
    print("🔧 Next: Update your API connection strings to use port 27017")

if __name__ == "__main__":
    main()
