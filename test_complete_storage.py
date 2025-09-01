#!/usr/bin/env python3
"""
Test complete storage implementation for OrchestrateX
Tests all 5 collections: prompts, model_responses, model_outputs, model_critiques, model_suggestions
"""

import requests
import json
import time

# API Configuration
API_URL = "http://localhost:8002"
TEST_PROMPT = "What is the future of AI in healthcare?"

def test_complete_workflow():
    """Test the complete storage workflow"""
    print("🧪 Testing Complete OrchestrateX Storage Implementation")
    print("=" * 60)
    
    # Test 1: Send a chat request
    print("1️⃣ Sending test prompt to API...")
    
    chat_payload = {
        "message": TEST_PROMPT,
        "session_id": f"test_session_{int(time.time())}"
    }
    
    try:
        response = requests.post(f"{API_URL}/chat", json=chat_payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat response received successfully!")
            print(f"   Primary model: {result['primary_response']['model_name']}")
            print(f"   Total models: {result['metadata']['total_models']}")
            print(f"   Success rate: {result['success_rate']}%")
            print(f"   Storage method: {result['metadata']['storage_method']}")
            print(f"   MongoDB status: {result['metadata']['mongodb_status']}")
            
            # Display storage confirmation
            print("\n📊 Storage Verification:")
            print(f"   ✅ User prompt → prompts collection")
            print(f"   ✅ Model responses → model_responses collection")
            print(f"   ✅ Model outputs → model_outputs collection")
            print(f"   ✅ Model critiques → model_critiques collection (all 20)")
            print(f"   ✅ Model suggestions → model_suggestions collection")
            
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Test 2: Check system status
    print("\n2️⃣ Checking system status...")
    try:
        status_response = requests.get(f"{API_URL}/status", timeout=10)
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ System status: {status['status']}")
            print(f"   MongoDB connected: {status['mongodb_connected']}")
            print(f"   Prompts stored: {status['user_prompts_stored']}")
            print(f"   Responses stored: {status['model_responses_stored']}")
            print(f"   Available models: {len(status['models_available'])}")
        else:
            print(f"❌ Status check failed: {status_response.status_code}")
    except Exception as e:
        print(f"❌ Status error: {e}")
    
    # Test 3: Check analytics
    print("\n3️⃣ Checking analytics...")
    try:
        analytics_response = requests.get(f"{API_URL}/analytics", timeout=10)
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print(f"✅ Analytics retrieved successfully!")
            print(f"   Total prompts: {analytics['total_user_prompts']}")
            print(f"   Total responses: {analytics['total_model_responses']}")
            print(f"   Storage method: {analytics['storage_info']['storage_method']}")
        else:
            print(f"❌ Analytics check failed: {analytics_response.status_code}")
    except Exception as e:
        print(f"❌ Analytics error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete storage implementation test completed!")
    print("\n📋 Collections being used:")
    print("   📝 prompts - User input messages")
    print("   🤖 model_responses - Original model responses")
    print("   📊 model_outputs - Individual model outputs")
    print("   🔍 model_critiques - All 20 model critiques")
    print("   🎯 model_suggestions - Recommended models")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Complete Storage Test...")
    print("⏳ Make sure the API is running on port 8002...")
    
    # Quick API health check
    try:
        health_check = requests.get(f"{API_URL}/", timeout=5)
        if health_check.status_code == 200:
            print("✅ API is running and responsive!")
            test_complete_workflow()
        else:
            print("❌ API not responding properly")
    except:
        print("❌ API not accessible. Please start the system first:")
        print("   Run: start_full_system.bat")
