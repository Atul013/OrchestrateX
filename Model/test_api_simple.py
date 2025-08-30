#!/usr/bin/env python3
"""
Simple API Test Script

Tests the Flask API with basic requests.
"""

import requests
import json

def test_api():
    """Test the Flask API with simple requests."""
    
    # Test single prediction
    print("Testing API prediction...")
    
    try:
        response = requests.post(
            "http://localhost:5000/predict",
            json={"prompt": "Write a Python function for sorting"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print(f"Best Model: {result['best_model']}")
            print(f"Confidence: {result['prediction_confidence']:.3f}")
            return True
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_api()
