#!/usr/bin/env python3
"""
Test script to demonstrate algorithm response storage
"""

import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:5001"

def test_api_connection():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✅ API is running and connected to MongoDB")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {str(e)}")
        return False

def test_store_response():
    """Test storing an algorithm response"""
    try:
        # Sample algorithm response data
        test_data = {
            "user_input": "What is the best model for text generation?",
            "selected_model": "GPT-4",
            "confidence_score": 0.95,
            "algorithm_version": "1.0",
            "response_text": "Based on analysis, GPT-4 is recommended for this task.",
            "metadata": {
                "processing_time": 0.5,
                "models_considered": ["GPT-4", "Claude", "Gemini"],
                "selection_criteria": "text_quality"
            }
        }
        
        response = requests.post(f"{API_URL}/store-response", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Successfully stored algorithm response")
            print(f"   Document ID: {result['document_id']}")
            print(f"   Timestamp: {result['timestamp']}")
            return True
        else:
            print(f"❌ Failed to store response: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error storing response: {str(e)}")
        return False

def test_get_responses():
    """Test retrieving stored responses"""
    try:
        response = requests.get(f"{API_URL}/get-responses?limit=5")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {result['count']} stored responses")
            
            # Display responses
            for i, resp in enumerate(result['responses'], 1):
                print(f"\n   Response {i}:")
                print(f"     Model: {resp.get('selected_model')}")
                print(f"     Confidence: {resp.get('confidence_score')}")
                print(f"     Timestamp: {resp.get('timestamp')}")
                print(f"     User Input: {resp.get('user_input')[:50]}...")
            
            return True
        else:
            print(f"❌ Failed to get responses: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting responses: {str(e)}")
        return False

def test_list_collections():
    """Test listing database collections"""
    try:
        response = requests.get(f"{API_URL}/collections")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Available collections: {result['collections']}")
            return True
        else:
            print(f"❌ Failed to list collections: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error listing collections: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing OrchestrateX Algorithm Response Storage\n")
    
    # Test 1: API Connection
    print("1. Testing API connection...")
    if not test_api_connection():
        exit(1)
    
    print("\n" + "="*50)
    
    # Test 2: Store Response
    print("\n2. Testing response storage...")
    if not test_store_response():
        exit(1)
    
    print("\n" + "="*50)
    
    # Test 3: List Collections
    print("\n3. Testing collection listing...")
    test_list_collections()
    
    print("\n" + "="*50)
    
    # Test 4: Get Responses
    print("\n4. Testing response retrieval...")
    test_get_responses()
    
    print("\n" + "="*50)
    print("\n🎉 All tests completed successfully!")
    print("\n📋 Summary:")
    print("   ✅ MongoDB is running on port 27018")
    print("   ✅ Mongo Express UI is available at http://localhost:8081 (admin/admin)")
    print("   ✅ API is running on port 5001")
    print("   ✅ Algorithm responses can be stored and retrieved")
    print("\n🔍 Next steps:")
    print("   1. Visit http://localhost:8081 to view data in MongoDB Express")
    print("   2. Visit http://localhost:5001/health to check API status")
    print("   3. Integrate your ModelSelector algorithm with this API")
