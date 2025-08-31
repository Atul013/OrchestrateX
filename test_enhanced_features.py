#!/usr/bin/env python3
"""
Test the Enhanced Ultra Context Analyzer Features
"""

from ultra_context_analyzer import UltraContextAnalyzer

def test_enhanced_features():
    """Test new intent types, domains, and valid combinations."""
    
    analyzer = UltraContextAnalyzer()
    
    test_cases = [
        # Test new intent types
        ("Compare React vs Vue for web development", "compare_something", "intent"),
        ("Troubleshoot my database connection errors", "troubleshoot_something", "intent"),
        ("Optimize my Python code for better performance", "optimize_something", "intent"),
        
        # Test new domains
        ("How to treat diabetes with medication?", "medical", "domain"),
        ("What are the legal implications of data privacy?", "legal", "domain"),
        ("Analyze cryptocurrency investment strategies", "financial", "domain"),
        ("Design a character for my RPG game", "gaming", "domain"),
        ("Create a modern UI design for mobile app", "design", "domain"),
        
        # Test valid combinations (should be coherent)
        ("Use Python for bioinformatics snake venom analysis", True, "coherence"),  # Bio + Tech valid
        ("How does music affect programming productivity?", True, "coherence"),  # Music + Productivity valid
        ("Color psychology in user interface design", True, "coherence"),  # Color + UI valid
        
        # Test context-dependent absurdity (should be absurd)
        ("How does pizza optimize database performance?", False, "coherence"),  # Food + Tech absurd
        ("Can red color increase server CPU speed?", False, "coherence"),  # Color + Performance absurd (no UI context)
    ]
    
    print("🧪 Testing Enhanced Ultra Context Analyzer Features")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        if len(test_case) == 3:
            prompt, expected, test_type = test_case
        else:
            prompt, expected = test_case
            test_type = "coherence"
            
        print(f"\n🔍 Test {i}: {prompt}")
        print("-" * 50)
        
        try:
            context = analyzer.analyze_ultra_context(prompt)
            overall = context['overall_context']
            model, confidence, reasoning = analyzer.select_ultra_model(prompt)
            
            if test_type == "intent":
                # Testing intent detection
                detected_intent = overall['primary_intent']
                result = "✅ PASS" if detected_intent == expected else "❌ FAIL"
                print(f"{result} Intent: Expected '{expected}', Got '{detected_intent}'")
            
            elif test_type == "domain":
                # Testing domain detection
                detected_domain = overall['primary_domain']
                result = "✅ PASS" if detected_domain == expected else "❌ FAIL"
                print(f"{result} Domain: Expected '{expected}', Got '{detected_domain}'")
            
            elif test_type == "coherence":
                # Testing coherence (True = should be coherent, False = should be absurd)
                is_coherent = overall['is_coherent']
                result = "✅ PASS" if is_coherent == expected else "❌ FAIL"
                absurdity = overall['absurdity_score']
                print(f"{result} Coherence: Expected {'coherent' if expected else 'absurd'}, Got {'coherent' if is_coherent else 'absurd'} (Absurdity: {absurdity:.1%})")
                
                # Show valid combinations if any
                if 'valid_combinations' in context['coherence_check'] and context['coherence_check']['valid_combinations']:
                    print(f"Valid Combinations: {', '.join(context['coherence_check']['valid_combinations'])}")
            
            print(f"🎯 Selected: {model} ({confidence:.1%})")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_enhanced_features()
