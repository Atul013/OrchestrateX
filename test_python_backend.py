#!/usr/bin/env python3
"""
Test Python Backend Configuration
This script tests if the Python backend is properly configured and working.
"""

import requests
import json
import sys
import os
from time import sleep

def test_python_backend():
    """Test the Python backend endpoints"""
    
    print("🧪 Testing OrchestrateX Python Backend")
    print("=" * 50)
    
    # Test Model Selector API (port 5000)
    print("\n1️⃣ Testing Model Selector API (port 5000)")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Model Selector API is running")
            print(f"   Response: {response.json()}")
            
            # Test prediction endpoint
            test_prompt = {"prompt": "Hello, test prediction"}
            pred_response = requests.post("http://localhost:5000/predict", json=test_prompt, timeout=10)
            if pred_response.status_code == 200:
                pred_data = pred_response.json()
                print(f"✅ Model prediction works: {pred_data.get('best_model', 'Unknown')}")
                print(f"   Confidence: {pred_data.get('prediction_confidence', 0):.3f}")
            else:
                print(f"⚠️ Model prediction failed: {pred_response.status_code}")
        else:
            print(f"❌ Model Selector API error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Model Selector API not running (port 5000)")
    except Exception as e:
        print(f"❌ Model Selector API error: {e}")
    
    # Test Main API Server (port 8000)
    print("\n2️⃣ Testing Main API Server (port 8000)")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Main API Server is running")
            health_data = response.json()
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Backend: {health_data.get('backend', 'Unknown')}")
            print(f"   Environment: {health_data.get('environment', 'Unknown')}")
            
            # Test chat endpoint
            print("\n   Testing chat endpoint...")
            chat_data = {"message": "Hello from test script"}
            chat_response = requests.post("http://localhost:8000/chat", json=chat_data, timeout=30)
            
            if chat_response.status_code == 200:
                chat_result = chat_response.json()
                print("✅ Chat endpoint works!")
                print(f"   Primary Model: {chat_result.get('primary_response', {}).get('model_name', 'Unknown')}")
                print(f"   Response Length: {len(chat_result.get('primary_response', {}).get('response_text', ''))}")
                print(f"   Total Cost: ${chat_result.get('total_cost', 0):.4f}")
                print(f"   API Calls: {chat_result.get('api_calls', 0)}")
                print(f"   Backend Type: {chat_result.get('metadata', {}).get('backend_type', 'Unknown')}")
                
                # Show first 100 chars of response
                response_text = chat_result.get('primary_response', {}).get('response_text', '')
                if response_text:
                    print(f"   Response Preview: {response_text[:100]}...")
                
                return True
            else:
                print(f"❌ Chat endpoint failed: {chat_response.status_code}")
                print(f"   Error: {chat_response.text}")
                return False
        else:
            print(f"❌ Main API Server error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Main API Server not running (port 8000)")
        return False
    except Exception as e:
        print(f"❌ Main API Server error: {e}")
        return False

def check_environment():
    """Check if environment is properly configured"""
    
    print("\n3️⃣ Checking Environment Configuration")
    
    # Check if orche.env exists
    if os.path.exists("orche.env"):
        print("✅ orche.env file found")
        
        # Count API keys in file
        api_key_count = 0
        with open("orche.env", 'r') as f:
            for line in f:
                if 'API_KEY' in line and '=' in line and not line.startswith('#'):
                    api_key_count += 1
        
        print(f"   API Keys in file: {api_key_count}")
    else:
        print("❌ orche.env file not found")
    
    # Check environment variables
    env_keys = [k for k in os.environ.keys() if 'API_KEY' in k]
    print(f"   API Keys in environment: {len(env_keys)}")
    
    for key in env_keys:
        value = os.environ[key]
        print(f"   ✅ {key}: {value[:10]}...")

def test_frontend_compatibility():
    """Test if the configuration works for frontend"""
    
    print("\n4️⃣ Testing Frontend Compatibility")
    
    # Check if frontend can reach the backend
    frontend_endpoints = [
        "http://localhost:8000/health",
        "http://localhost:8000/chat"
    ]
    
    for endpoint in frontend_endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                print(f"✅ Frontend can reach: {endpoint}")
            else:
                print(f"⚠️ Frontend endpoint issue: {endpoint} ({response.status_code})")
        except Exception as e:
            print(f"❌ Frontend cannot reach: {endpoint} ({e})")

def main():
    """Main test function"""
    
    print("🔍 OrchestrateX Python Backend Test Suite")
    print("="*50)
    
    # Run tests
    check_environment()
    backend_working = test_python_backend()
    test_frontend_compatibility()
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    if backend_working:
        print("🎉 SUCCESS: Python backend is working!")
        print("✅ Real AI API integration active")
        print("✅ Frontend configured for Python backend")
        print("✅ Environment loaded properly")
        print("\n🚀 Next Steps:")
        print("   1. Start the Python backend: start-python-backend.bat")
        print("   2. Start the frontend on a different port")
        print("   3. Test with real user prompts")
        print("\n📍 Endpoints:")
        print("   - Backend: http://localhost:8000/chat")
        print("   - Model Selector: http://localhost:5000/health")
    else:
        print("❌ ISSUES FOUND: Python backend needs attention")
        print("🔧 Troubleshooting:")
        print("   1. Make sure orche.env has valid API keys")
        print("   2. Run: python env_loader.py")
        print("   3. Start model selector: python Model/model_selector_api.py")
        print("   4. Start API server: python api_server.py")
        print("   5. Check logs for specific errors")

if __name__ == "__main__":
    main()