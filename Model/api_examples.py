#!/usr/bin/env python3
"""
Flask API Usage Examples

This file shows how to use the ModelSelector Flask API in different scenarios.
"""

import requests
import json

# API Configuration
API_BASE_URL = "http://localhost:5000"

def example_single_prediction():
    """Example: Single prediction request."""
    print("📝 Example 1: Single Prediction")
    print("-" * 40)
    
    # Request data
    prompt = "Write a Python function to implement binary search"
    
    # Make API call
    response = requests.post(
        f"{API_BASE_URL}/predict",
        json={"prompt": prompt},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Prompt: {prompt}")
        print(f"Best Model: {result['best_model']}")
        print(f"Confidence: {result['prediction_confidence']:.3f}")
        print("All Models:")
        for model, score in result['confidence_scores'].items():
            print(f"  {model}: {score:.3f}")
    else:
        print(f"Error {response.status_code}: {response.text}")
    
    print()

def example_error_handling():
    """Example: Error handling."""
    print("📝 Example 2: Error Handling")
    print("-" * 40)
    
    # Test missing prompt
    response = requests.post(
        f"{API_BASE_URL}/predict",
        json={},  # Missing prompt
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Missing prompt - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def example_different_prompts():
    """Example: Different types of prompts."""
    print("📝 Example 3: Different Prompt Types")
    print("-" * 40)
    
    test_prompts = [
        ("Coding", "Debug this JavaScript error in React"),
        ("Reasoning", "Explain the economic impact of renewable energy"),
        ("General", "What's a good recipe for chocolate cake?"),
        ("Mixed", "Analyze this sorting algorithm and optimize it")
    ]
    
    for category, prompt in test_prompts:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"{category:10} | {result['best_model']:15} | {result['prediction_confidence']:.3f} | {prompt[:40]}...")
        else:
            print(f"Error for prompt: {prompt}")
    
    print()

def example_curl_commands():
    """Show equivalent curl commands."""
    print("📝 Example 4: Equivalent cURL Commands")
    print("-" * 40)
    
    curl_examples = [
        {
            "description": "Single prediction",
            "command": '''curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"prompt": "Write a Python function to sort arrays"}'
'''
        },
        {
            "description": "Error handling test",
            "command": '''curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{}'
'''
        }
    ]
    
    for example in curl_examples:
        print(f"{example['description']}:")
        print(example['command'])

def example_integration():
    """Example: Integration into existing application."""
    print("📝 Example 5: Application Integration")
    print("-" * 40)
    
    integration_code = '''
# Integration Example
import requests

class AIModelRouter:
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url
    
    def get_best_model(self, user_prompt):
        """Get the best AI model for a user prompt."""
        try:
            response = requests.post(
                f"{self.api_url}/predict",
                json={"prompt": user_prompt},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "model": result["best_model"],
                    "confidence": result["prediction_confidence"],
                    "success": True
                }
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Usage
router = AIModelRouter()
result = router.get_best_model("Write a sorting algorithm")

if result["success"]:
    print(f"Use model: {result['model']} (confidence: {result['confidence']:.3f})")
    # Route to the recommended model...
else:
    print(f"Error: {result['error']}")
    # Use fallback model...
'''
    
    print(integration_code)

if __name__ == "__main__":
    print("🚀 Flask API Usage Examples")
    print("=" * 50)
    print("Make sure the API server is running: python simple_api.py")
    print()
    
    try:
        # Test if server is running
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
    except:
        print("❌ API server not running. Start it with: python simple_api.py")
        print("   Then run this script again.")
        exit(1)
    
    # Run examples
    example_single_prediction()
    example_error_handling()
    example_different_prompts()
    example_curl_commands()
    example_integration()
