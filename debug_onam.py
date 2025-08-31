#!/usr/bin/env python3
"""
Debug the Onam prompt selection issue
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Model'))

from Model.hybrid_model_selector import HybridModelSelector

def debug_onam_prompt():
    """Debug why the Onam prompt was misclassified."""
    
    prompt = "I need you to tell me everything you know about Onam. Is it related to python somehow ??"
    
    print("🔍 DEBUGGING ONAM PROMPT SELECTION")
    print("=" * 60)
    print(f"📝 PROMPT: {prompt}")
    print()
    
    selector = HybridModelSelector()
    
    # Get features
    features = selector.extract_features(prompt)
    
    print("🤔 WHAT THE SYSTEM DETECTED:")
    print(f"  • Has code keywords: {features['has_code_keywords']}")
    print(f"  • Has question words: {features['has_question_words']}")
    print(f"  • Has create keywords: {features['has_create_keywords']}")
    print(f"  • Has analyze keywords: {features['has_analyze_keywords']}")
    print(f"  • Word count: {features['word_count']}")
    print(f"  • Character count: {features['char_count']}")
    print()
    
    # Check specific keyword detection
    prompt_lower = prompt.lower()
    print("🔍 KEYWORD ANALYSIS:")
    print(f"  • Contains 'python': {'python' in prompt_lower}")
    print(f"  • Contains 'onam': {'onam' in prompt_lower}")
    print(f"  • Contains coding words: {any(word in prompt_lower for word in ['code', 'programming', 'script', 'function'])}")
    print(f"  • Contains question words: {any(word in prompt_lower for word in ['what', 'how', 'why', 'is', 'related'])}")
    print()
    
    # Get the actual selection
    result = selector.select_model(prompt)
    
    print("🎯 ACTUAL SELECTION:")
    print(f"  • Selected Model: {result['model']}")
    print(f"  • Confidence: {result['confidence']:.1%}")
    print(f"  • Method: {result['method']}")
    print(f"  • Reasoning: {result['reasoning']}")
    print()
    
    print("❌ PROBLEM IDENTIFIED:")
    print("  The system detected 'python' keyword and immediately")
    print("  classified it as a coding task, ignoring the context")
    print("  about Onam festival and the snake reference.")
    print()
    
    print("✅ WHAT IT SHOULD HAVE DONE:")
    print("  • Recognized this as a cultural/educational question")
    print("  • Noted the question format ('Is it related to...')")
    print("  • Selected a general knowledge model like GPT-OSS or Llama 4 Maverick")
    print("  • Confidence should be lower since context is ambiguous")

if __name__ == "__main__":
    debug_onam_prompt()
