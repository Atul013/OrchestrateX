#!/usr/bin/env python3
"""
Quick test to check API status and trigger data creation
"""

import requests
import json
import time

def test_api():
    print("🚀 Quick API Test")
    print("=" * 40)
    
    try:
        # Test status endpoint
        print("1️⃣ Checking API status...")
        response = requests.get("http://localhost:8002/status", timeout=5)
        status_data = response.json()
        
        print(f"   Status: {status_data.get('status')}")
        print(f"   Firestore: {status_data.get('firestore_connected')}")
        print(f"   User prompts stored: {status_data.get('user_prompts_stored', 0)}")
        print(f"   Model responses stored: {status_data.get('model_responses_stored', 0)}")
        
        # Send a test message
        print("\n2️⃣ Sending test message...")
        test_message = {
            "message": "Hello! This is a test to create Firestore collections and verify they work properly."
        }
        
        response = requests.post("http://localhost:8002/chat", json=test_message, timeout=30)
        chat_data = response.json()
        
        if chat_data.get("success"):
            print("   ✅ Message sent successfully!")
            print(f"   Session ID: {chat_data.get('metadata', {}).get('session_id')}")
            print(f"   Models used: {chat_data.get('metadata', {}).get('total_models')}")
        else:
            print("   ❌ Message failed")
            
        # Check status again to see new counts
        print("\n3️⃣ Checking updated status...")
        response = requests.get("http://localhost:8002/status", timeout=5)
        new_status = response.json()
        
        print(f"   User prompts stored: {new_status.get('user_prompts_stored', 0)}")
        print(f"   Model responses stored: {new_status.get('model_responses_stored', 0)}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Is the server running on http://localhost:8002?")
        print("   Run: python working_api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_api()
