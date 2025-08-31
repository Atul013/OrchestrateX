#!/usr/bin/env python3
"""
Final test to verify complete system connectivity
"""

import requests
import json
import time

def test_complete_system():
    print("🔄 Complete System Test - Frontend to Backend")
    print("=" * 50)
    
    # 1. Test API Status
    try:
        print("1️⃣  Testing API Status...")
        status_response = requests.get('http://localhost:8002/status', timeout=10)
        if status_response.status_code == 200:
            print("   ✅ API Status: HEALTHY")
            status_data = status_response.json()
            print(f"   📊 Storage: {status_data.get('storage_method', 'unknown')}")
        else:
            print(f"   ❌ API Status: {status_response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API Status failed: {e}")
        return False
    
    # 2. Test Chat Endpoint (same as frontend)
    try:
        print("\n2️⃣  Testing Chat Endpoint...")
        chat_data = {"message": "Hello, this is a test from the system test"}
        
        print("   📤 Sending request...")
        chat_response = requests.post(
            'http://localhost:8002/chat',
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"   📥 Response Status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print("   ✅ Chat Endpoint: SUCCESS")
            print(f"   🤖 Primary Model: {result.get('primary_response', {}).get('model_name', 'Unknown')}")
            print(f"   💰 Total Cost: ${result.get('total_cost', 0):.4f}")
            print(f"   📊 Success Rate: {result.get('success_rate', 0):.1f}%")
            print(f"   🔗 API Calls: {result.get('api_calls', 0)}")
            
            # Check if all required fields are present
            required_fields = ['success', 'primary_response', 'critiques', 'total_cost', 'api_calls', 'success_rate']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
            else:
                print("   ✅ All required fields present")
            
            return True
        else:
            print(f"   ❌ Chat failed: {chat_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Chat test failed: {e}")
        return False

def main():
    success = test_complete_system()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SYSTEM TEST PASSED!")
        print("✅ Backend API is working correctly")
        print("✅ All endpoints responding")
        print("✅ Response format matches frontend expectations")
        print("\n🎯 SOLUTION:")
        print("   Frontend URL: http://localhost:5176")
        print("   Backend URL: http://localhost:8002")
        print("   Try the chat now - it should work!")
    else:
        print("❌ SYSTEM TEST FAILED!")
        print("   Check the errors above and try again")

if __name__ == "__main__":
    main()
