#!/usr/bin/env python3
"""
Quick test of README examples to ensure they work as documented.
"""

from model_selector import ModelSelector

def test_readme_examples():
    """Test the examples provided in the README."""
    
    print("🧪 Testing README Examples")
    print("=" * 40)
    
    # Test 1: Quick model prediction
    print("\n1. Testing Quick Model Prediction:")
    selector = ModelSelector()
    selector.load_model('model_selector.pkl')
    
    result = selector.select_best_model("Write a Python function to sort arrays")
    print(f"   ✅ Best model: {result['predicted_model']}")
    print(f"   ✅ Confidence: {result['prediction_confidence']:.3f}")
    
    # Test 2: Multiple prompts
    print("\n2. Testing Multiple Prompts:")
    test_prompts = [
        "Write a REST API in Python",
        "Explain quantum physics", 
        "Help me cook dinner"
    ]
    
    for prompt in test_prompts:
        result = selector.select_best_model(prompt)
        print(f"   📝 '{prompt}' → {result['predicted_model']}")
    
    # Test 3: Feature analysis
    print("\n3. Testing Feature Analysis:")
    result = selector.select_best_model("Debug this JavaScript error")
    features = result['prompt_features']
    print(f"   📊 Categories: {features['categories']}")
    print(f"   🎯 Domain: {features['topic_domain']}")
    print(f"   💡 Intent: {features['intent_type']}")
    
    print("\n✅ All README examples working correctly!")

if __name__ == "__main__":
    test_readme_examples()
