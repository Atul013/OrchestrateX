# Database Setup and Testing Script for OrchestrateX Cloud MongoDB

import pymongo
import json
from datetime import datetime

# MongoDB connection details
MONGODB_HOST = "34.46.82.84"
MONGODB_PORT = 27017
DATABASE_NAME = "orchestratex"

def test_mongodb_connection():
    """Test MongoDB connection and create initial schema"""
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/")
        db = client[DATABASE_NAME]
        
        print("🔗 Testing MongoDB connection...")
        
        # Test connection with ping
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Create collections and indexes
        print("📋 Creating database schema...")
        
        # User Sessions Collection
        user_sessions = db.user_sessions
        user_sessions.create_index([("user_id", 1)])
        user_sessions.create_index([("session_start", 1)])
        user_sessions.create_index([("status", 1)])
        
        # Prompts Collection
        prompts = db.prompts
        prompts.create_index([("user_id", 1)])
        prompts.create_index([("timestamp", 1)])
        prompts.create_index([("session_id", 1)])
        
        # Responses Collection
        responses = db.responses
        responses.create_index([("prompt_id", 1)])
        responses.create_index([("model_name", 1)])
        responses.create_index([("timestamp", 1)])
        
        # Orchestration Workflows Collection
        workflows = db.orchestration_workflows
        workflows.create_index([("session_id", 1)])
        workflows.create_index([("status", 1)])
        
        # AI Model Metrics Collection
        model_metrics = db.ai_model_metrics
        model_metrics.create_index([("model_name", 1)])
        model_metrics.create_index([("timestamp", 1)])
        
        # System Logs Collection
        system_logs = db.system_logs
        system_logs.create_index([("timestamp", 1)])
        system_logs.create_index([("level", 1)])
        
        print("✅ Database schema created successfully!")
        
        # Insert test data
        print("📝 Inserting test data...")
        
        # Test session
        test_session = {
            "user_id": "test_user_001",
            "session_start": datetime.now(),
            "max_iterations": 5,
            "status": "active",
            "total_cost": 0.0,
            "settings": {
                "preferred_models": ["GLM4.5", "GPT-OSS"],
                "max_response_time": 30
            }
        }
        session_result = user_sessions.insert_one(test_session)
        
        # Test prompt
        test_prompt = {
            "session_id": str(session_result.inserted_id),
            "user_id": "test_user_001",
            "content": "What are the benefits of AI orchestration?",
            "timestamp": datetime.now(),
            "metadata": {
                "source": "web_interface",
                "ip_address": "127.0.0.1"
            }
        }
        prompt_result = prompts.insert_one(test_prompt)
        
        # Test response
        test_response = {
            "prompt_id": str(prompt_result.inserted_id),
            "model_name": "GLM4.5",
            "response_text": "AI orchestration provides enhanced accuracy, diverse perspectives, and improved reliability through multi-model collaboration.",
            "timestamp": datetime.now(),
            "metadata": {
                "response_time": 2.5,
                "token_count": 156,
                "cost": 0.002
            }
        }
        responses.insert_one(test_response)
        
        # System log entry
        test_log = {
            "timestamp": datetime.now(),
            "level": "INFO",
            "message": "Database initialization completed successfully",
            "component": "database_setup",
            "metadata": {
                "collections_created": 6,
                "indexes_created": 12
            }
        }
        system_logs.insert_one(test_log)
        
        print("✅ Test data inserted successfully!")
        
        # Verify collections
        collections = db.list_collection_names()
        print(f"📊 Created collections: {', '.join(collections)}")
        
        # Count documents
        print("\n📈 Collection statistics:")
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            print(f"  - {collection_name}: {count} documents")
        
        print("\n🎉 MongoDB database setup complete!")
        print(f"🌐 Database accessible at: mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{DATABASE_NAME}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    print("🚀 OrchestrateX Cloud Database Setup")
    print("=====================================")
    success = test_mongodb_connection()
    
    if success:
        print("\n✅ Your OrchestrateX database is ready on Google Cloud!")
        print("The application can now store user sessions, prompts, and AI responses.")
    else:
        print("\n❌ Database setup failed. Please check the configuration.")