#!/usr/bin/env python3
"""
Interactive Universal Context Analyzer Tester
Test the context understanding with your own prompts!
"""

from universal_context_analyzer import UniversalContextAnalyzer

def interactive_test():
    """Interactive testing interface for the Universal Context Analyzer."""
    
    print("🧠 Universal Context Analyzer - Interactive Tester")
    print("=" * 60)
    print("Enter your prompts to see how the AI understands context!")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 60)
    
    analyzer = UniversalContextAnalyzer()
    
    while True:
        print("\n🔍 Enter your prompt:")
        prompt = input("➤ ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for testing! Goodbye!")
            break
        
        if not prompt:
            print("❌ Please enter a prompt!")
            continue
        
        print(f"\n🎯 Analyzing: '{prompt}'")
        print("-" * 50)
        
        try:
            # Get full context analysis
            context = analyzer.analyze_universal_context(prompt)
            overall = context['overall_context']
            
            # Get model selection
            model, confidence, reasoning = analyzer.select_best_model(prompt)
            
            # Display key results
            print(f"📊 Primary Intent: {overall['primary_intent'].replace('_', ' ').title()}")
            print(f"🏷️  Primary Domain: {overall['primary_domain'].title()}")
            print(f"📤 Expected Output: {overall['expected_output'].replace('_', ' ').title()}")
            print(f"📈 Complexity: {overall['complexity_level'].title()}")
            print(f"🧠 Coherent: {'✅ Yes' if overall['is_coherent'] else '❌ No'}")
            print(f"📊 Context Confidence: {overall['context_confidence']:.1%}")
            print(f"🎯 Selected Model: {model} ({confidence:.1%})")
            print(f"💭 Reasoning: {reasoning}")
            
            # Show detailed analysis if user wants
            print(f"\n🔍 Want detailed analysis? (y/n): ", end="")
            detail = input().strip().lower()
            
            if detail in ['y', 'yes']:
                print("\n📋 DETAILED ANALYSIS:")
                print("-" * 30)
                
                # Intent details
                intent = context['intent_analysis']
                print(f"🎯 Intent Scores:")
                for intent_type, score in intent['intent_scores'].items():
                    if score > 0:
                        print(f"   • {intent_type.replace('_', ' ').title()}: {score:.1f}")
                
                # Domain details
                domain = context['domain_reasoning']
                print(f"\n🏷️  Domain Evidence:")
                for domain_type, evidence in domain['domain_evidence'].items():
                    if evidence['score'] > 0:
                        print(f"   • {domain_type.title()}: {evidence['score']:.1f}")
                        for item in evidence['evidence']:
                            print(f"     - {item}")
                
                # Coherence details
                coherence = context['coherence_check']
                if not coherence['is_coherent']:
                    print(f"\n🚨 Coherence Issues:")
                    for issue in coherence['issues']:
                        print(f"   • {issue}")
                
        except Exception as e:
            print(f"❌ Error analyzing prompt: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    interactive_test()
