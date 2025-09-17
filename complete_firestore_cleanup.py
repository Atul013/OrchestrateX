#!/usr/bin/env python3
"""
Discover and clear ALL Firestore collections
"""

from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
import os

def discover_and_clear_all_collections():
    """Discover all collections and clear them completely"""
    
    try:
        # Initialize Firebase Admin if not already done
        if not firebase_admin._apps:
            try:
                firebase_admin.initialize_app()
                print("✅ Firebase initialized with default credentials")
            except Exception as e:
                print(f"⚠️ Default credentials failed: {e}")
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
        
        # Get all collections
        print("\n🔍 Discovering all collections...")
        collections = db.collections()
        collection_names = []
        
        for collection in collections:
            collection_names.append(collection.id)
            print(f"   📁 Found collection: {collection.id}")
        
        if not collection_names:
            print("   ℹ️ No collections found")
            return True
        
        print(f"\n📊 Total collections found: {len(collection_names)}")
        
        # Clear each collection
        total_deleted = 0
        
        for collection_name in collection_names:
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
                    print(f"   📦 Committed batch of {batch_count} deletions...")
                    batch = db.batch()
                    batch_count = 0
            
            # Commit any remaining operations
            if batch_count > 0:
                batch.commit()
            
            total_deleted += deleted_count
            print(f"   ✅ Deleted {deleted_count} documents from {collection_name}")
        
        print(f"\n🎉 Successfully cleared ALL Firestore collections!")
        print(f"📊 Total documents deleted: {total_deleted}")
        print(f"🗂️ Collections cleared: {', '.join(collection_names)}")
        
        # Verify all collections are empty
        print(f"\n🔍 Verifying all collections are empty:")
        for collection_name in collection_names:
            collection_ref = db.collection(collection_name)
            docs = list(collection_ref.limit(1).stream())
            if len(docs) == 0:
                print(f"   ✅ {collection_name}: Empty")
            else:
                print(f"   ⚠️ {collection_name}: Still has {len(docs)} documents")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing Firestore: {e}")
        return False

if __name__ == "__main__":
    print("🧹 Starting COMPLETE Firestore database cleanup...")
    print("⚠️ This will discover and delete ALL collections and data")
    
    # Confirmation prompt
    response = input("\nDo you want to proceed with COMPLETE cleanup? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y']:
        success = discover_and_clear_all_collections()
        if success:
            print("\n✅ Complete database cleanup finished!")
        else:
            print("\n❌ Database cleanup failed!")
    else:
        print("\n🚫 Operation cancelled.")