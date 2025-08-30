#!/usr/bin/env python3
"""
Simple test of the API - run this after starting the server.
"""

import requests
import json
import sys

def test_single_request():
    """Test a single API request."""
    try:
        print("🧪 Testing API Request...")
        
        # Test data
        test_prompt = "Write a Python function to sort arrays"
        
        # Make request
        response = requests.post(
            "http://localhost:5000/predict",
            json={"prompt": test_prompt},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📝 Prompt: '{test_prompt}'")
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"🎯 Best Model: {result['best_model']}")
            print(f"📊 Confidence: {result['prediction_confidence']:.3f}")
            print("🔢 All Confidence Scores:")
            for model, score in result['confidence_scores'].items():
                print(f"   {model}: {score:.3f}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the API server is running.")
        print("   Start server: python simple_api.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_single_request()
