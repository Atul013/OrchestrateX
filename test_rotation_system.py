#!/usr/bin/env python3
"""
Test script for API Key Rotation System
"""

import requests
import json
import time
from datetime import datetime

def test_key_status():
    """Test the key status endpoint"""
    try:
        response = requests.get("http://localhost:8002/api/key-status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Key Status Endpoint Working!")
            print(f"Total Providers: {len(data['status'])}")
            for provider, status in data['status'].items():
                print(f"  📋 {provider}: {status['total_keys']} keys, current index: {status['current_key_index']}")
            return True
        else:
            print(f"❌ Key status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing key status: {e}")
        return False

def test_orchestration():
    """Test the orchestration endpoint"""
    try:
        data = {
            "prompt": "Hello! This is a test to verify API key rotation is working properly."
        }
        
        print("\n🧪 Testing orchestration endpoint...")
        response = requests.post(
            "http://localhost:8002/api/orchestration/process",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Orchestration endpoint working!")
                print(f"Primary model: {result['primary_response']['model_name']}")
                print(f"Response: {result['primary_response']['response_text'][:100]}...")
                print(f"Tokens used: {result['primary_response']['tokens_used']}")
                print(f"Critiques: {len(result['critiques'])}")
                return True
            else:
                print(f"❌ Orchestration failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Orchestration endpoint failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error testing orchestration: {e}")
        return False

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"Status: {data.get('status')}")
            print(f"API Rotation: {data.get('api_rotation', False)}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health: {e}")
        return False

if __name__ == "__main__":
    print("🔑 API Key Rotation System Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    
    # Test all endpoints
    tests = [
        ("Health Check", test_health),
        ("Key Status", test_key_status),
        ("Orchestration", test_orchestration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API key rotation system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the server logs.")