#!/usr/bin/env python3
"""
Test the MongoDB-connected API
"""

import requests
import json

def test_mongodb_api():
    print("🧪 Testing MongoDB-Connected API")
    print("=" * 50)
    
    try:
        # Test status endpoint
        print("1️⃣ Testing /status endpoint...")
        status_response = requests.get('http://localhost:8002/status', timeout=5)
        print(f"Status: {status_response.status_code}")
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ MongoDB Connected: {status_data.get('mongodb_connected')}")
            print(f"📊 Storage Method: {status_data.get('storage_method')}")
            print(f"💾 User Prompts Stored: {status_data.get('user_prompts_stored')}")
            print(f"🤖 Model Responses Stored: {status_data.get('model_responses_stored')}")
            print(f"🔥 Models Available: {status_data.get('models_available')}")
        
        # Test chat endpoint with latest models
        print("\n2️⃣ Testing /chat endpoint with latest models...")
        chat_data = {"message": "Tell me about artificial intelligence and machine learning"}
        chat_response = requests.post(
            'http://localhost:8002/chat', 
            json=chat_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        print(f"Chat Status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            result = chat_response.json()
            print(f"🏆 Best Model: {result['primary_response']['model_name']}")
            print(f"💬 Response: {result['primary_response']['response_text'][:100]}...")
            print(f"⚡ Processing Time: {result['metadata']['processing_time_seconds']}s")
            print(f"📊 Total Models: {result['metadata']['total_models']}")
            print(f"💾 Storage Method: {result['metadata']['storage_method']}")
            print(f"🗄️ MongoDB Status: {result['metadata']['mongodb_status']}")
            
            # Show alternatives from other models
            if 'critiques' in result and result['critiques']:
                print(f"\n🔄 Alternative models also responded:")
                for critique in result['critiques'][:2]:
                    print(f"   • {critique['model_name']}: {critique['critique_text'][:60]}...")
        else:
            print(f"❌ Chat failed: {chat_response.text}")
            
        # Test analytics
        print("\n3️⃣ Testing /analytics endpoint...")
        analytics_response = requests.get('http://localhost:8002/analytics', timeout=5)
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print(f"📊 Total Prompts: {analytics['total_user_prompts']}")
            print(f"🤖 Total Responses: {analytics['total_model_responses']}")
            print(f"📈 Model Usage: {analytics['model_usage']}")
            print(f"💾 Storage Info: {analytics['storage_info']}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_mongodb_api()
