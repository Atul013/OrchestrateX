#!/usr/bin/env python3
"""
Test with the corrected collection names
"""

import requests
import json

def test_with_correct_collections():
    print("🧪 Testing with Corrected Collection Names")
    print("=" * 50)
    
    try:
        # Test the chat endpoint
        print("1️⃣  Sending test message...")
        response = requests.post(
            'http://localhost:8002/chat',
            json={"message": "Testing with correct MongoDB collections"},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API responded successfully!")
            
            metadata = result.get('metadata', {})
            print(f"📊 Storage: {metadata.get('storage_method')}")
            print(f"🗄️  MongoDB: {metadata.get('mongodb_status')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_with_correct_collections()
    
    if success:
        print("\n🎯 SUCCESS! Now try your frontend:")
        print("   1. Go to: http://localhost:5176")
        print("   2. Send a message")
        print("   3. Check MongoDB Express: http://localhost:8081")
        print("   4. Look for data in 'prompts' collection")
    else:
        print("❌ Still having issues")
