#!/usr/bin/env python3
"""
Check MongoDB data directly - see what's actually stored
"""

from pymongo import MongoClient
import json
from datetime import datetime

def check_mongodb_data():
    """Check what's in MongoDB collections"""
    try:
        print("🔍 Checking MongoDB Collections...")
        print("=" * 50)
        
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27019", serverSelectionTimeoutMS=5000)
        db = client.orchestratex
        
        # List all collections
        collections = db.list_collection_names()
        print(f"📁 Available Collections: {collections}")
        print()
        
        # Check each collection
        for collection_name in ['prompts', 'model_responses', 'model_outputs', 'model_critiques', 'model_suggestions']:
            if collection_name in collections:
                collection = db[collection_name]
                count = collection.count_documents({})
                print(f"📊 {collection_name}: {count} documents")
                
                if count > 0:
                    # Show latest 3 documents
                    latest = list(collection.find().sort("timestamp", -1).limit(3))
                    print(f"   📝 Latest entries:")
                    for i, doc in enumerate(latest, 1):
                        # Remove MongoDB _id for cleaner display
                        doc.pop('_id', None)
                        
                        if collection_name == 'prompts':
                            print(f"      {i}. Message: {doc.get('user_message', 'N/A')[:50]}...")
                            print(f"         Session: {doc.get('session_id', 'N/A')}")
                            print(f"         Source: {doc.get('source', 'N/A')}")
                            print(f"         Time: {doc.get('timestamp', 'N/A')}")
                        
                        elif collection_name == 'model_outputs':
                            print(f"      {i}. Model: {doc.get('model_name', 'N/A')}")
                            print(f"         Response: {doc.get('response_text', 'N/A')[:40]}...")
                            print(f"         Session: {doc.get('session_id', 'N/A')}")
                        
                        elif collection_name == 'model_suggestions':
                            print(f"      {i}. Recommended: {doc.get('recommended_model', 'N/A')}")
                            print(f"         Confidence: {doc.get('confidence_score', 'N/A')}")
                            print(f"         Session: {doc.get('session_id', 'N/A')}")
                        
                        else:
                            # For other collections, show first few keys
                            keys = list(doc.keys())[:3]
                            print(f"      {i}. Keys: {keys}")
                        
                        print()
            else:
                print(f"❌ {collection_name}: Collection doesn't exist")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Error: {e}")
        return False

def main():
    print("🔍 OrchestrateX MongoDB Data Check")
    print(f"⏰ Time: {datetime.now()}")
    print("=" * 50)
    
    if check_mongodb_data():
        print("✅ MongoDB check completed!")
    else:
        print("❌ MongoDB check failed!")
    
    print("\n💡 If you see prompts above, then storage is working!")
    print("💡 If no prompts, try sending a message through the UI")

if __name__ == "__main__":
    main()
