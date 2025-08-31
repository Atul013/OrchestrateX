#!/usr/bin/env python3
"""
Interactive test for hybrid model selector
Enter your own prompts to see model selection in action
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Model'))

from Model.hybrid_model_selector import HybridModelSelector

def test_custom_prompt():
    """Test the hybrid model selector with a custom prompt."""
    
    print("🚀 Custom Prompt Testing - Hybrid Model Selector")
    print("=" * 60)
    
    # Initialize selector
    selector = HybridModelSelector()
    print()
    
    while True:
        # Get user input
        print("💬 Enter your prompt (or 'quit' to exit):")
        prompt = input(">>> ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not prompt:
            print("❌ Please enter a prompt!")
            continue
        
        print("\n🔍 Analyzing prompt...")
        print("-" * 40)
        
        # Get prediction
        result = selector.select_model(prompt, confidence_threshold=0.75)
        
        # Display results
        confidence_emoji = "🎯" if result['confidence'] >= 0.90 else "📊" if result['confidence'] >= 0.75 else "🤔"
        method_emoji = "⚡" if result['method'] == 'rule_based' else "🤖" if result['method'] == 'ml_fallback' else "🔄"
        
        print(f"{confidence_emoji} **SELECTED MODEL:** {result['model']}")
        print(f"📊 **CONFIDENCE:** {result['confidence']:.1%}")
        print(f"{method_emoji} **METHOD:** {result['method']}")
        print(f"💭 **REASONING:** {result['reasoning']}")
        print(f"📝 **PROMPT:** {result['prompt_preview']}")
        
        # Confidence analysis
        if result['confidence'] >= 0.95:
            print("🔥 **ANALYSIS:** Extremely high confidence - perfect match!")
        elif result['confidence'] >= 0.90:
            print("✅ **ANALYSIS:** High confidence - strong pattern match")
        elif result['confidence'] >= 0.75:
            print("👍 **ANALYSIS:** Good confidence - decent pattern match")
        elif result['confidence'] >= 0.60:
            print("🤷 **ANALYSIS:** Medium confidence - weak pattern match")
        else:
            print("⚠️ **ANALYSIS:** Low confidence - fallback selection")
        
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    test_custom_prompt()
