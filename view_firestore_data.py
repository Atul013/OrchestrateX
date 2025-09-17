#!/usr/bin/env python3
"""
Script to view Firestore collections and data
"""

import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import json
from datetime import datetime

def initialize_firestore():
    """Initialize Firestore connection"""
    try:
        # Initialize Firebase Admin if not already done
        if not firebase_admin._apps:
            # Try to use default credentials first
            try:
                firebase_admin.initialize_app()
                print("✅ Firebase initialized with default credentials")
            except Exception as e:
                print(f"⚠️ Default credentials failed: {e}")
                # Try with service account key file if it exists
                service_account_path = "service-account-key.json"
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    print(f"✅ Firebase initialized with service account: {service_account_path}")
                else:
                    print("❌ No Firebase credentials found")
                    return None
        
        # Initialize Firestore client
        db = firestore.Client()
        print("✅ Firestore connected successfully!")
        return db
        
    except Exception as e:
        print(f"❌ Firestore connection failed: {e}")
        return None

def view_collection(db, collection_name, limit=5):
    """View documents in a Firestore collection"""
    try:
        print(f"\n📊 Collection: {collection_name}")
        print("-" * 50)
        
        # Query collection
        docs = db.collection(collection_name).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        doc_count = 0
        for doc in docs:
            doc_count += 1
            doc_data = doc.to_dict()
            print(f"\n📄 Document ID: {doc.id}")
            
            # Pretty print the document data
            for key, value in doc_data.items():
                if isinstance(value, datetime):
                    print(f"   {key}: {value.strftime('%Y-%m-%d %H:%M:%S')}")
                elif len(str(value)) > 100:
                    print(f"   {key}: {str(value)[:100]}...")
                else:
                    print(f"   {key}: {value}")
        
        if doc_count == 0:
            print("   No documents found in this collection")
        else:
            print(f"\n   Total documents shown: {doc_count}")
            
        return doc_count
        
    except Exception as e:
        print(f"❌ Error reading collection {collection_name}: {e}")
        return 0

def get_collection_count(db, collection_name):
    """Get total count of documents in a collection"""
    try:
        # Get a sample to estimate count (Firestore doesn't have a direct count)
        docs = list(db.collection(collection_name).limit(1000).stream())
        return len(docs)
    except Exception as e:
        print(f"❌ Error counting collection {collection_name}: {e}")
        return 0

def main():
    print("🔍 Firestore Database Viewer")
    print("=" * 60)
    
    # Initialize Firestore
    db = initialize_firestore()
    if not db:
        print("❌ Could not connect to Firestore")
        return
    
    # Collections to check
    collections = [
        "user_prompts",
        "model_responses", 
        "model_critiques",
        "model_suggestions",
        "sessions"
    ]
    
    print("\n📈 Collection Summary:")
    print("-" * 30)
    total_docs = 0
    
    for collection in collections:
        count = get_collection_count(db, collection)
        total_docs += count
        print(f"   • {collection}: {count} documents")
    
    print(f"\n🎯 Total documents across all collections: {total_docs}")
    
    if total_docs > 0:
        print("\n" + "=" * 60)
        print("📄 Recent Documents (showing last 3 per collection):")
        
        for collection in collections:
            view_collection(db, collection, limit=3)
    else:
        print("\n⚠️ No data found. Try sending a message to the API first:")
        print("   POST http://localhost:8002/chat")
        print("   Body: {\"message\": \"Test message\"}")
    
    print("\n" + "=" * 60)
    print("🌐 View in Google Cloud Console:")
    print("   https://console.cloud.google.com/firestore")

if __name__ == "__main__":
    main()