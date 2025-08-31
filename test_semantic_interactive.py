#!/usr/bin/env python3
"""
Interactive Semantic Model Selector Tester
Test the intelligent context-aware system with your own prompts
"""

import sys
import os
from semantic_model_selector import SemanticModelSelector

def interactive_semantic_test():
    """Interactive tester for the semantic model selector."""
    
    print("🧠 Interactive Semantic Model Selector")
    print("=" * 60)
    print("🎯 This system uses semantic analysis (no hardcoded keywords)")
    print("💡 It understands context, intent, and meaning")
    print("🔍 Watch how it analyzes your prompts...")
    print()
    
    # Initialize the semantic selector
    selector = SemanticModelSelector()
    print()
    
    while True:
        # Get user input
        print("💬 Enter your prompt (or 'quit' to exit):")
        prompt = input(">>> ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for testing! Goodbye!")
            break
            
        if not prompt:
            print("❌ Please enter a prompt!")
            continue
        
        print(f"\n🔍 Analyzing: '{prompt}'")
        print("=" * 60)
        
        try:
            # Get semantic analysis
            context = selector.analyze_semantic_context(prompt)
            
            print("🧠 **SEMANTIC ANALYSIS:**")
            print(f"  📊 Intent Type: {context['intent_type']}")
            print(f"  🏷️  Domain Signals: {', '.join(context['domain_signals'])}")
            print(f"  📈 Complexity Level: {context['complexity_level']}")
            print(f"  🎭 Interaction Style: {context['interaction_style']}")
            print(f"  📤 Expected Output: {context['output_expectation']}")
            print(f"  🤔 Ambiguity Level: {context['ambiguity_level']:.1%}")
            print()
            
            # Get model selection
            model, confidence, reasoning = selector.semantic_model_selection(prompt)
            
            # Display results with emojis
            if confidence >= 0.9:
                confidence_emoji = "🎯"
                confidence_desc = "VERY HIGH"
            elif confidence >= 0.8:
                confidence_emoji = "✅"
                confidence_desc = "HIGH"
            elif confidence >= 0.7:
                confidence_emoji = "📊"
                confidence_desc = "GOOD"
            elif confidence >= 0.6:
                confidence_emoji = "🤷"
                confidence_desc = "MEDIUM"
            else:
                confidence_emoji = "⚠️"
                confidence_desc = "LOW"
            
            print("🎯 **MODEL SELECTION:**")
            print(f"{confidence_emoji} **Selected Model:** {model}")
            print(f"📊 **Confidence:** {confidence:.1%} ({confidence_desc})")
            print(f"💭 **Reasoning:** {reasoning}")
            print()
            
            # Show why this model was chosen
            print("🔬 **WHY THIS MODEL?**")
            if model == 'TNG DeepSeek':
                if 'technical' in context['domain_signals']:
                    print("  • Technical implementation detected")
                if context['output_expectation'] == 'code':
                    print("  • Code output expected")
                if context['intent_type'] == 'creation':
                    print("  • Creation/building task identified")
            
            elif model == 'GLM4.5':
                if context['intent_type'] == 'analysis':
                    print("  • Analytical reasoning required")
                if 'business' in context['domain_signals']:
                    print("  • Business/professional context")
                if context['complexity_level'] in ['complex', 'very_complex']:
                    print("  • Complex reasoning needed")
            
            elif model == 'Llama 4 Maverick':
                if context['intent_type'] == 'inquiry':
                    print("  • Educational question format")
                if 'educational' in context['domain_signals']:
                    print("  • Learning-oriented request")
                if context['output_expectation'] == 'explanation':
                    print("  • Explanatory response needed")
            
            elif model == 'GPT-OSS':
                if 'cultural' in context['domain_signals']:
                    print("  • Cultural/general knowledge")
                if 'creative' in context['domain_signals']:
                    print("  • Creative content creation")
                if context['intent_type'] == 'general':
                    print("  • General purpose best fit")
            
            elif model == 'Qwen3':
                if context['intent_type'] == 'analysis':
                    print("  • Logical reasoning required")
                print("  • Precision and structured thinking")
            
            elif model == 'MoonshotAI Kimi':
                if context['interaction_style'] == 'assistance':
                    print("  • Personal assistance request")
                print("  • Conversational and practical guidance")
            
        except Exception as e:
            print(f"❌ Error analyzing prompt: {e}")
            continue
        
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    interactive_semantic_test()
