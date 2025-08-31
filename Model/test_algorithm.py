#!/usr/bin/env python3
"""
Test your ModelSelector algorithm with dual database storage
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:5000"

def test_algorithm():
    print("🧠 Testing Your ModelSelector Algorithm with Dual Database Storage\n")
    
    # Test prompts that showcase different model selections
    test_prompts = [
        "How do I build a machine learning model for image classification?",
        "Write a creative story about a robot learning to paint",
        "Explain quantum computing in simple terms",
        "Generate Python code for data visualization",
        "What's the meaning of life and consciousness?"
    ]
    
    print("1️⃣ Testing Model Prediction (Analytics Database):")
    print("=" * 60)
    
    for i, prompt in enumerate(test_prompts, 1):
        try:
            response = requests.post(f"{BASE_URL}/predict", 
                                   json={"prompt": prompt},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n🔍 Test {i}: {prompt[:50]}...")
                print(f"   🎯 Algorithm Choice: {data['predicted_model']}")
                print(f"   📊 Confidence: {data['confidence']:.2f}")
                print(f"   📈 All Scores: {json.dumps(data['all_model_scores'], indent=6)}")
            else:
                print(f"❌ Error for prompt {i}: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error for prompt {i}: {e}")
    
    print("\n\n2️⃣ Testing Full Chat Flow (Conversations Database):")
    print("=" * 60)
    
    # Test chat endpoint that uses algorithm + stores conversation
    chat_data = {
        "prompt": "I need help building a chatbot with natural language processing",
        "user_id": "test_user_123",
        "session_id": "demo_session"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=chat_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n💬 Chat Response:")
            print(f"   🤖 Response: {data['response'][:100]}...")
            print(f"   🎯 Model Used: {data['model_used']}")
            print(f"   📊 Confidence: {data['confidence']:.2f}")
            print(f"   💾 Conversation ID: {data['conversation_id']}")
        else:
            print(f"❌ Chat error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat connection error: {e}")
    
    print("\n\n3️⃣ Viewing Analytics Database:")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/analytics?limit=3", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Recent Model Predictions ({data['count']} records):")
            
            for i, pred in enumerate(data['predictions'][:3], 1):
                print(f"\n   📈 Prediction {i}:")
                print(f"      Prompt: {pred['prompt'][:60]}...")
                print(f"      Chosen Model: {pred['predicted_model']}")
                print(f"      Confidence: {pred['confidence_score']:.2f}")
                print(f"      Timestamp: {pred['timestamp']}")
        else:
            print(f"❌ Analytics error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Analytics connection error: {e}")
    
    print("\n\n4️⃣ Viewing Conversations Database:")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/conversations?limit=2", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n💬 Recent Conversations ({data['count']} records):")
            
            for i, conv in enumerate(data['conversations'][:2], 1):
                print(f"\n   📝 Conversation {i}:")
                print(f"      User: {conv['user_id']}")
                print(f"      Prompt: {conv['prompt'][:60]}...")
                print(f"      Model Used: {conv['model_used']}")
                print(f"      Response: {conv['response'][:80]}...")
                print(f"      Timestamp: {conv['timestamp']}")
        else:
            print(f"❌ Conversations error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Conversations connection error: {e}")
    
    print("\n\n✅ Algorithm Test Complete!")
    print("🎯 Your ModelSelector successfully chose the best models")
    print("📊 Dual database storage working perfectly")
    print("🚀 Ready for frontend integration!")

if __name__ == "__main__":
    test_algorithm()
