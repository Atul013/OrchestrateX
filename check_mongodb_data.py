#!/usr/bin/env python3
"""
Check MongoDB data directly - see what's actually stored
"""

from pymongo import MongoClient
import json
from datetime import datetimein/env python3
"""
Check MongoDB data directly to see if your prompt was stored
"""

from pymongo import MongoClient
import json
from datetime import datetime

def check_mongodb_data():
    print("🔍 Checking MongoDB for Your Recent Prompt")
    print("=" * 50)
    
    try:
        # Connect to MongoDB on the new port
        client = MongoClient("mongodb://project_admin:project_password@localhost:27019/orchestratex?authSource=admin")
        db = client.orchestratex
        
        print("✅ Connected to MongoDB successfully!")
        
        # Check user_prompts collection
        print("\n📊 Checking user_prompts collection...")
        user_prompts = list(db.user_prompts.find().sort("timestamp", -1).limit(5))
        
        if user_prompts:
            print(f"   Found {len(user_prompts)} recent prompts:")
            for i, prompt in enumerate(user_prompts, 1):
                timestamp = prompt.get('timestamp', 'No timestamp')
                message = prompt.get('user_message', 'No message')
                session_id = prompt.get('session_id', 'No session')
                print(f"   {i}. [{timestamp}] Session: {session_id}")
                print(f"      Message: {message[:100]}...")
                print()
        else:
            print("   ❌ No user prompts found in MongoDB")
        
        # Check model_responses collection
        print("🤖 Checking model_responses collection...")
        model_responses = list(db.model_responses.find().sort("timestamp", -1).limit(5))
        
        if model_responses:
            print(f"   Found {len(model_responses)} recent responses:")
            for i, response in enumerate(model_responses, 1):
                timestamp = response.get('timestamp', 'No timestamp')
                model_name = response.get('model_name', 'Unknown model')
                session_id = response.get('session_id', 'No session')
                print(f"   {i}. [{timestamp}] {model_name} - Session: {session_id}")
        else:
            print("   ❌ No model responses found in MongoDB")
            
        # Collection stats
        print("\n📈 Collection Statistics:")
        print(f"   User prompts: {db.user_prompts.count_documents({})}")
        print(f"   Model responses: {db.model_responses.count_documents({})}")
        
        client.close()
        return len(user_prompts) > 0 or len(model_responses) > 0
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running on port 27019")
        return False

if __name__ == "__main__":
    has_data = check_mongodb_data()
    
    print("\n" + "=" * 50)
    if has_data:
        print("🎉 SUCCESS! Your data is being stored in MongoDB!")
        print("🌐 View it in MongoDB Express: http://localhost:8081")
        print("   - Username: admin")
        print("   - Password: admin")
    else:
        print("⚠️  No data found yet. This could mean:")
        print("   1. Frontend not connecting to backend")
        print("   2. CORS issue with port 5176")
        print("   3. MongoDB connection issue")
        print("\n💡 Try sending another message in the frontend")
