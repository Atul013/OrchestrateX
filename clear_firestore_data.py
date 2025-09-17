#!/usr/bin/env python3
"""
Clear all data from Firestore collections while keeping the collections themselves
"""

from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
import os

def clear_firestore_collections():
    """Clear all documents from Firestore collections but keep the collections"""
    
    try:
        # Initialize Firebase Admin if not already done
        if not firebase_admin._apps:
            # Try to use default credentials or service account key file
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
                    return False
        
        # Initialize Firestore client
        db = firestore.Client()
        print("✅ Firestore connected successfully!")
        
        # Define the collections to clear
        collections = [
            'user_prompts',
            'model_responses', 
            'model_critiques',
            'model_suggestions',
            'sessions'
        ]
        
        total_deleted = 0
        
        for collection_name in collections:
            print(f"\n🗑️ Clearing collection: {collection_name}")
            
            # Get all documents in the collection
            collection_ref = db.collection(collection_name)
            docs = collection_ref.stream()
            
            # Count and delete documents
            deleted_count = 0
            batch = db.batch()
            batch_count = 0
            
            for doc in docs:
                batch.delete(doc.reference)
                batch_count += 1
                deleted_count += 1
                
                # Firestore batch operations have a limit of 500
                if batch_count >= 500:
                    batch.commit()
                    batch = db.batch()
                    batch_count = 0
            
            # Commit any remaining operations
            if batch_count > 0:
                batch.commit()
            
            total_deleted += deleted_count
            print(f"   ✅ Deleted {deleted_count} documents from {collection_name}")
        
        print(f"\n🎉 Successfully cleared Firestore database!")
        print(f"📊 Total documents deleted: {total_deleted}")
        print(f"🗂️ Collections preserved: {', '.join(collections)}")
        
        # Verify collections are empty
        print(f"\n🔍 Verifying collections are empty:")
        for collection_name in collections:
            collection_ref = db.collection(collection_name)
            docs = list(collection_ref.limit(1).stream())
            if len(docs) == 0:
                print(f"   ✅ {collection_name}: Empty")
            else:
                print(f"   ⚠️ {collection_name}: Still has documents")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing Firestore: {e}")
        return False

if __name__ == "__main__":
    print("🧹 Starting Firestore database cleanup...")
    print("⚠️ This will delete ALL data but keep empty collections")
    
    # Confirmation prompt
    response = input("\nDo you want to proceed? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        success = clear_firestore_collections()
        if success:
            print("\n✅ Database cleanup completed successfully!")
        else:
            print("\n❌ Database cleanup failed!")
    else:
        print("\n🚫 Operation cancelled.")