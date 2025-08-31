#!/usr/bin/env python3
"""
Interactive Ultra Context Analyzer Tester
Ultra-fine-tuned with enhanced precision!
"""

from ultra_context_analyzer import UltraContextAnalyzer

def interactive_ultra_test():
    """Interactive testing interface for the Ultra Context Analyzer."""
    
    print("🚀 Ultra-Fine-Tuned Context Analyzer v2.0 - Interactive Tester")
    print("=" * 75)
    print("✨ Enhanced with: Smart disambiguation, absurdity detection, quality scoring")
    print("🎯 Test with any prompt to see ultra-precise context understanding!")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 75)
    
    analyzer = UltraContextAnalyzer()
    
    while True:
        print("\n🔍 Enter your prompt:")
        prompt = input("➤ ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for testing the Ultra Analyzer! Goodbye!")
            break
        
        if not prompt:
            print("❌ Please enter a prompt!")
            continue
        
        print(f"\n🎯 Ultra-Analyzing: '{prompt}'")
        print("-" * 60)
        
        try:
            # Get comprehensive ultra analysis
            context = analyzer.analyze_ultra_context(prompt)
            overall = context['overall_context']
            
            # Get ultra model selection
            model, confidence, reasoning = analyzer.select_ultra_model(prompt)
            
            # Display enhanced results
            print(f"🎯 Primary Intent: {overall['primary_intent'].replace('_', ' ').title()}")
            if context['intent_analysis']['secondary_intent']:
                print(f"🔄 Secondary Intent: {context['intent_analysis']['secondary_intent'].replace('_', ' ').title()}")
            
            print(f"🏷️  Primary Domain: {overall['primary_domain'].title()}")
            active_domains = context['domain_reasoning']['active_domains']
            if len(active_domains) > 1:
                print(f"🏷️  Other Domains: {', '.join([d.title() for d in active_domains if d != overall['primary_domain']])}")
            
            print(f"📤 Expected Output: {overall['expected_output'].replace('_', ' ').title()}")
            print(f"📊 Complexity: {overall['complexity_level'].title()}")
            
            # Enhanced coherence display
            coherence_icon = "✅" if overall['is_coherent'] else "❌"
            absurdity = overall['absurdity_score']
            print(f"🧠 Coherent: {coherence_icon} (Absurdity: {absurdity:.1%})")
            
            if not overall['is_coherent']:
                print(f"🚨 Issues: {', '.join(context['coherence_check']['issues'])}")
            
            # Quality indicators
            quality = overall['context_quality']
            quality_emoji = "⭐⭐⭐" if quality > 0.8 else "⭐⭐" if quality > 0.6 else "⭐"
            print(f"{quality_emoji} Context Quality: {quality:.1%}")
            
            print(f"🎯 Selected Model: {model} ({confidence:.1%})")
            print(f"💭 Reasoning: {reasoning}")
            
            # Offer detailed analysis
            print(f"\n🔍 Want ultra-detailed analysis? (y/n): ", end="")
            detail = input().strip().lower()
            
            if detail in ['y', 'yes']:
                print("\n📋 ULTRA-DETAILED ANALYSIS:")
                print("-" * 40)
                
                # Intent breakdown
                intent_scores = context['intent_analysis']['intent_scores']
                print(f"🎯 Intent Confidence Breakdown:")
                for intent_type, score in sorted(intent_scores.items(), key=lambda x: x[1], reverse=True):
                    if score > 0:
                        print(f"   • {intent_type.replace('_', ' ').title()}: {score:.2f}")
                
                # Domain evidence
                domain_evidence = context['domain_reasoning']['domain_evidence']
                print(f"\n🏷️  Domain Evidence Analysis:")
                for domain_type, evidence in domain_evidence.items():
                    if evidence['score'] > 0.1:
                        print(f"   • {domain_type.title()}: {evidence['score']:.2f}")
                        for item in evidence['evidence'][:2]:  # Show top 2 evidence items
                            print(f"     - {item}")
                
                # Complexity factors
                complexity_factors = context['task_complexity']['factors']
                print(f"\n📊 Complexity Factor Breakdown:")
                for factor, score in complexity_factors.items():
                    print(f"   • {factor.replace('_', ' ').title()}: {score:.2f}")
                
                # Quality factors
                quality_factors = overall['quality_factors']
                print(f"\n⭐ Quality Factor Analysis:")
                for factor, score in quality_factors.items():
                    print(f"   • {factor.replace('_', ' ').title()}: {score:.1%}")
                
                # Relationship analysis
                relationships = context['relationship_analysis']
                if relationships['relationships']:
                    print(f"\n🔗 Detected Relationships:")
                    for rel in relationships['relationships'][:3]:  # Show top 3
                        print(f"   • {rel['entity']} {rel['relationship']} {rel['concept']}")
                
        except Exception as e:
            print(f"❌ Error in ultra analysis: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    interactive_ultra_test()
