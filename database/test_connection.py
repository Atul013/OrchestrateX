"""
OrchestrateX MongoDB Connection Test
Test script to verify database connection and basic operations
"""

from pymongo import MongoClient
from datetime import datetime
import json

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    
    # Connection string
    connection_string = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
    
    try:
        # Create client and connect
        print("🔌 Connecting to MongoDB...")
        client = MongoClient(connection_string)
        db = client.orchestratex
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to OrchestrateX MongoDB successfully!")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📁 Collections found: {len(collections)}")
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"   - {collection}: {count} documents")
        
        # Test insert operation - create a sample user session
        print("\n🧪 Testing insert operation...")
        sample_session = {
            "user_id": "test_user_001",
            "session_start": datetime.now(),
            "max_iterations": 5,
            "status": "active",
            "total_cost": 0.0,
            "settings": {
                "preferred_models": ["gpt4", "claude"],
                "cost_limit": 10.0,
                "quality_threshold": 8.0
            },
            "created_at": datetime.now()
        }
        
        result = db.user_sessions.insert_one(sample_session)
        print(f"✅ Inserted test session with ID: {result.inserted_id}")
        
        # Test query operation
        print("\n🔍 Testing query operation...")
        session = db.user_sessions.find_one({"user_id": "test_user_001"})
        if session:
            print(f"✅ Found test session: {session['user_id']}")
            print(f"   Status: {session['status']}")
            print(f"   Max iterations: {session['max_iterations']}")
        
        # Test AI model profiles
        print("\n🤖 Testing AI model profiles...")
        models = list(db.ai_model_profiles.find({}, {"model_name": 1, "provider": 1, "specialties": 1}))
        print(f"✅ Found {len(models)} AI models:")
        for model in models:
            specialties = ", ".join(model['specialties'])
            print(f"   - {model['model_name']} ({model['provider']}): {specialties}")
        
        # Clean up test data
        print("\n🧹 Cleaning up test data...")
        db.user_sessions.delete_one({"user_id": "test_user_001"})
        print("✅ Test data cleaned up")
        
        # Connection summary
        print("\n" + "="*50)
        print("🎉 DATABASE CONNECTION TEST SUCCESSFUL!")
        print("="*50)
        print("Your OrchestrateX MongoDB database is ready for development!")
        print("\nConnection details:")
        print(f"  - Host: localhost:27018")
        print(f"  - Database: orchestratex")
        print(f"  - Collections: {len(collections)}")
        print(f"  - AI Models: {len(models)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
    
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_mongodb_connection()
