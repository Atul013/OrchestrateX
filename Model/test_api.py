#!/usr/bin/env python3
"""
Test the Flask API endpoints with sample requests.
"""

import requests
import json
import time

def test_api():
    """Test the Flask API with various requests."""
    
    base_url = "http://localhost:5000"
    
    print("🧪 TESTING FLASK API")
    print("=" * 50)
    
    # Test data
    test_prompts = [
        "Write a Python function to sort arrays",
        "Explain quantum physics concepts",
        "Hello, how are you today?",
        "Debug this JavaScript error",
        "Analyze climate change effects"
    ]
    
    print("1. Testing /predict endpoint...")
    
    for i, prompt in enumerate(test_prompts, 1):
        try:
            print(f"\n{i}. Testing prompt: '{prompt}'")
            
            response = requests.post(
                f"{base_url}/predict",
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   📝 Best Model: {result['best_model']}")
                print(f"   🎯 Confidence: {result['prediction_confidence']:.3f}")
                
                # Show top 3 models
                top_models = sorted(result['confidence_scores'].items(), 
                                  key=lambda x: x[1], reverse=True)[:3]
                print(f"   📊 Top 3: {', '.join([f'{m}:{s:.3f}' for m, s in top_models])}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {str(e)}")
        
        time.sleep(0.5)  # Small delay between requests
    
    # Test error handling
    print(f"\n6. Testing error handling...")
    
    # Test missing prompt
    try:
        response = requests.post(
            f"{base_url}/predict",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 400:
            print("   ✅ Missing prompt error handled correctly")
            print(f"   📝 Response: {response.json()}")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {str(e)}")
    
    # Test invalid JSON
    try:
        response = requests.post(
            f"{base_url}/predict",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"   📝 Invalid JSON response: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {str(e)}")
    
    print(f"\n✅ API testing complete!")
    print(f"🌐 API is running at: {base_url}")

if __name__ == "__main__":
    # Wait a moment for the server to fully start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    test_api()
