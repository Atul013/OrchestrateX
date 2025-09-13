#!/usr/bin/env python3
"""
Fix MongoDB prompts collection index issue
"""

import pymongo
from pymongo import MongoClient

# Connect to MongoDB
try:
    client = MongoClient("mongodb://localhost:27019/")
    db = client.orchestratex
    prompts_collection = db.prompts
    
    print("🔧 Fixing prompts collection index...")
    
    # Drop the problematic index
    try:
        prompts_collection.drop_index("idx_hash")
        print("✅ Dropped problematic idx_hash index")
    except Exception as e:
        print(f"ℹ️  Index might not exist: {e}")
    
    # List all indexes
    indexes = list(prompts_collection.list_indexes())
    print("📋 Current indexes:")
    for idx in indexes:
        print(f"   - {idx['name']}: {idx.get('key', {})}")
    
    print("✅ Prompts collection is now ready for storing!")
    
except Exception as e:
    print(f"❌ Error: {e}")
