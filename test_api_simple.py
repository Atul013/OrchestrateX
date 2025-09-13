#!/usr/bin/env python3
"""
Simple API connectivity test for enhanced_ui_bridge_api.py
"""

import requests
import json

def test_api_connectivity():
    """Test basic API connectivity"""
    try:
        print("🔗 Testing API connectivity...")
        
        # Test basic status endpoint
        response = requests.get("http://localhost:8002", timeout=10)
        print(f"✅ Status endpoint: {response.status_code}")
        
        # Test orchestration endpoint with simple query
        test_data = {
            "query": "Hello, can you tell me what 2+2 equals?",
            "settings": {
                "enableRefinement": False,
                "temperature": 0.7
            }
        }
        
        print("🚀 Testing orchestration endpoint...")
        response = requests.post(
            "http://localhost:8002/api/orchestration/process",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Orchestration successful!")
            print(f"Primary response: {len(result.get('primaryResponse', ''))} characters")
            print(f"Critiques: {len(result.get('critiques', []))} received")
            return True
        else:
            print(f"❌ Orchestration failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - API not accessible")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_api_connectivity()
    if success:
        print("\n🎉 API is working correctly!")
    else:
        print("\n💥 API connectivity issues detected")
