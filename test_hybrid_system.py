#!/usr/bin/env python3
"""
Test the hybrid model selector directly without API
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Model'))

from Model.hybrid_model_selector import HybridModelSelector

def test_hybrid_system():
    """Test the hybrid model selector with various prompts."""
    
    print("🚀 Testing Hybrid Model Selector System")
    print("=" * 60)
    
    # Initialize selector
    selector = HybridModelSelector()
    
    # Test prompts with expected models
    test_cases = [
        ("Write a Python function to implement machine learning", "TNG DeepSeek"),
        ("Analyze the economic impact of remote work policies", "GLM4.5"),
        ("Create a creative story about time travel", "GPT-OSS"),
        ("Design a secure authentication system", "Qwen3"),
        ("Explain quantum computing in simple terms", "Llama 4 Maverick"),
        ("Build a React component for user profiles", "TNG DeepSeek"),
        ("Compare different investment strategies", "GLM4.5"),
        ("Write a marketing campaign for eco-friendly products", "GPT-OSS"),
        ("How do I improve my productivity at work?", "MoonshotAI Kimi"),
        ("Debug this JavaScript React component", "TNG DeepSeek")
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} prompts...\n")
    
    results = []
    high_confidence_count = 0
    
    for i, (prompt, expected) in enumerate(test_cases, 1):
        result = selector.select_model(prompt, confidence_threshold=0.75)
        
        is_high_confidence = result['confidence'] >= 0.90
        if is_high_confidence:
            high_confidence_count += 1
        
        confidence_emoji = "🎯" if is_high_confidence else "📊"
        method_emoji = "⚡" if result['method'] == 'rule_based' else "🤖"
        
        print(f"{confidence_emoji} Test {i:2d}: {result['confidence']:5.1%} | {result['model']:18s} | {method_emoji} {result['method']}")
        print(f"           Prompt: {prompt[:80]}...")
        print(f"           Reason: {result['reasoning']}")
        print()
        
        results.append(result)
    
    # Summary statistics
    avg_confidence = sum(r['confidence'] for r in results) / len(results)
    rule_based_count = sum(1 for r in results if r['method'] == 'rule_based')
    
    print("=" * 60)
    print("📈 PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"Average Confidence:     {avg_confidence:5.1%}")
    print(f"High Confidence (≥90%): {high_confidence_count:2d}/{len(results)} ({high_confidence_count/len(results):5.1%})")
    print(f"Rule-Based Selections:  {rule_based_count:2d}/{len(results)} ({rule_based_count/len(results):5.1%})")
    print(f"ML Fallback Available:  {'Yes' if selector.has_ml_fallback else 'No'}")
    
    # Model distribution
    model_counts = {}
    for result in results:
        model = result['model']
        model_counts[model] = model_counts.get(model, 0) + 1
    
    print(f"\n📊 MODEL DISTRIBUTION:")
    for model, count in sorted(model_counts.items()):
        print(f"  {model:18s}: {count:2d} selections ({count/len(results):5.1%})")
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print(f"🏆 System achieved {avg_confidence:.1%} average confidence")
    print(f"⚡ Rule-based approach handled {rule_based_count/len(results):.1%} of cases")
    
    return results

if __name__ == "__main__":
    test_hybrid_system()
