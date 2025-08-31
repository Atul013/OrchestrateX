#!/usr/bin/env python3
"""
Test script to demonstrate OrchestrateX storage workflow
"""

import requests
import json
import time
from datetime import datetime

API_BASE = "http://localhost:5001"

def test_storage_workflow():
    """Test the complete storage workflow"""
    
    print("🧪 Testing OrchestrateX Storage Workflow")
    print("=" * 50)
    
    # Step 1: Store user input
    print("\n1️⃣ Storing user input...")
    user_data = {
        "user_id": "test_user_123",
        "session_id": f"session_{int(time.time())}",
        "prompt": "Write a Python function to calculate fibonacci numbers",
        "category": "programming"
    }
    
    response = requests.post(f"{API_BASE}/store-user-input", json=user_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    session_id = response.json().get("session_id")
    
    # Step 2: Store algorithm decision
    print("\n2️⃣ Storing algorithm decision...")
    decision_data = {
        "session_id": session_id,
        "user_prompt": user_data["prompt"],
        "selected_model": "gpt-4",
        "confidence_score": 0.95,
        "reasoning": "Selected GPT-4 for complex programming task requiring detailed explanation",
        "available_models": ["gpt-4", "claude-3", "gemini-pro"],
        "criteria": "Programming complexity, code quality, explanation detail"
    }
    
    response = requests.post(f"{API_BASE}/store-algorithm-decision", json=decision_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    decision_id = response.json().get("decision_id")
    
    # Step 3: Store model response
    print("\n3️⃣ Storing model response...")
    response_data = {
        "session_id": session_id,
        "decision_id": decision_id,
        "model_name": "gpt-4",
        "response": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        "response_time": 1250,
        "token_count": 85,
        "cost": 0.002,
        "quality_score": 0.92
    }
    
    response = requests.post(f"{API_BASE}/store-model-response", json=response_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Step 4: Retrieve session data
    print("\n4️⃣ Retrieving complete session data...")
    response = requests.get(f"{API_BASE}/get-session-data/{session_id}")
    print(f"   Status: {response.status_code}")
    session_data = response.json()
    print(f"   Complete workflow stored successfully!")
    
    # Step 5: Get analytics
    print("\n5️⃣ Getting analytics summary...")
    response = requests.get(f"{API_BASE}/analytics/summary")
    print(f"   Status: {response.status_code}")
    analytics = response.json()
    print(f"   Analytics: {json.dumps(analytics, indent=2)}")
    
    print("\n✅ Storage workflow test completed successfully!")
    print(f"🎯 Session ID: {session_id}")
    print(f"📊 Check MongoDB Express at http://localhost:8081 to view stored data")

if __name__ == "__main__":
    try:
        # Check if API is running
        health_response = requests.get(f"{API_BASE}/health", timeout=5)
        if health_response.status_code == 200:
            test_storage_workflow()
        else:
            print("❌ Storage API is not responding. Please start it first with: python storage_api.py")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Storage API.")
        print("Please start the API first with: python storage_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")
