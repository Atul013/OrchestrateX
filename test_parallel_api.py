#!/usr/bin/env python3
"""
Quick test of the parallel API to verify it's working
"""

import requests
import json

# Test the parallel API
try:
    print("🧪 Testing Parallel 5-Model API...")
    
    # Test status endpoint
    status_response = requests.get('http://localhost:8002/status', timeout=5)
    print(f"✅ Status: {status_response.status_code}")
    print(f"📊 Response: {status_response.json()}")
    
    # Test chat endpoint
    print("\n🚀 Testing chat with parallel models...")
    chat_data = {"message": "What is machine learning?"}
    chat_response = requests.post(
        'http://localhost:8002/chat', 
        json=chat_data,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
    print(f"✅ Chat Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        result = chat_response.json()
        print(f"🏆 Best Model: {result['primary_response']['model_name']}")
        print(f"💬 Response: {result['primary_response']['response_text'][:100]}...")
        print(f"⚡ Processing Time: {result['metadata']['processing_time_seconds']}s")
        print(f"📊 Total Models: {result['metadata']['total_models']}")
        print("✅ Parallel API is working!")
    else:
        print(f"❌ Chat failed: {chat_response.text}")
        
except Exception as e:
    print(f"❌ Error testing API: {e}")
