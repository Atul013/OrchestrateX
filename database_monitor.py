#!/usr/bin/env python3
"""
OrchestrateX Database Monitor
Real-time monitoring tool to check if prompts are being stored in the database
"""

import pymongo
import time
import datetime
from bson import ObjectId
import json

# Database connection
MONGODB_URI = "mongodb://34.46.82.84:27017/orchestratex"

def connect_to_database():
    """Connect to MongoDB database"""
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.orchestratex
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        return db
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def monitor_collections(db):
    """Monitor all collections for new data"""
    print("\n🔍 Available collections:")
    collections = db.list_collection_names()
    for i, collection in enumerate(collections, 1):
        count = db[collection].count_documents({})
        print(f"  {i}. {collection} ({count} documents)")
    
    if not collections:
        print("  No collections found yet.")
    
    return collections

def watch_for_new_prompts(db):
    """Watch for new prompt insertions in real-time"""
    print("\n👀 Watching for new prompts and interactions...")
    print("Press Ctrl+C to stop monitoring\n")
    
    # Collections that might store prompts
    prompt_collections = ['prompts', 'conversations', 'interactions', 'requests', 'messages']
    
    try:
        # Get initial counts
        initial_counts = {}
        for collection_name in db.list_collection_names():
            initial_counts[collection_name] = db[collection_name].count_documents({})
        
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Check for changes in document counts
            changes_detected = False
            for collection_name in db.list_collection_names():
                current_count = db[collection_name].count_documents({})
                if collection_name not in initial_counts:
                    initial_counts[collection_name] = 0
                
                if current_count > initial_counts[collection_name]:
                    changes_detected = True
                    new_docs = current_count - initial_counts[collection_name]
                    print(f"🆕 [{current_time}] NEW DATA in '{collection_name}': +{new_docs} documents")
                    
                    # Show the latest document
                    latest_doc = db[collection_name].find().sort("_id", -1).limit(1)
                    for doc in latest_doc:
                        print(f"   📄 Latest document: {json.dumps(doc, default=str, indent=2)[:500]}...")
                    
                    initial_counts[collection_name] = current_count
            
            if not changes_detected:
                print(f"⏰ [{current_time}] No new data detected... (monitoring)")
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")

def show_recent_data(db):
    """Show recent data from all collections"""
    print("\n📊 Recent data in database:")
    
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"\n📁 Collection: {collection_name} ({count} documents)")
        
        # Show latest 3 documents
        recent_docs = collection.find().sort("_id", -1).limit(3)
        for i, doc in enumerate(recent_docs, 1):
            print(f"  {i}. {json.dumps(doc, default=str)[:200]}...")

def main():
    print("🚀 OrchestrateX Database Monitor")
    print("=" * 50)
    
    # Connect to database
    db = connect_to_database()
    if db is None:
        return
    
    print(f"🔗 Connected to: {MONGODB_URI}")
    
    # Show current collections
    collections = monitor_collections(db)
    
    # Show recent data
    if collections:
        show_recent_data(db)
    
    print("\n" + "=" * 50)
    print("Choose monitoring option:")
    print("1. Real-time monitoring (watch for new prompts)")
    print("2. Show current database contents")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        watch_for_new_prompts(db)
    elif choice == "2":
        show_recent_data(db)
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()