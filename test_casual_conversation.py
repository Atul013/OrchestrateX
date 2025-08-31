#!/usr/bin/env python3
"""    for prompt in casual_prompts:
        # Analyze context
        context = analyzer.analyze_ultra_context(prompt)
        # Select model
        model, confidence, reasoning = analyzer.select_ultra_model(prompt)
        
        print(f'📝 Prompt: "{prompt}"')
        print(f'   🤖 Model: {model} ({confidence:.1f}%)')
        print(f'   🎯 Intent: {context["intent"]}')
        print(f'   🏷️  Domain: {context["primary_domain"]}')
        print(f'   📤 Output: {context["expected_output"]}')
        print(f'   ⭐ Quality: {context["quality_score"]:.1f}%')
        print(f'   💭 Why: {reasoning[:80]}...')
        print()est for casual conversation handling
"""

from ultra_context_analyzer import UltraContextAnalyzer

def test_casual_prompts():
    analyzer = UltraContextAnalyzer()
    
    # Test casual conversation prompts
    casual_prompts = [
        'hey how are ya',
        'hello',
        'hi there', 
        'sup',
        'good morning',
        'thanks',
        'bye',
        'see you later',
        'whats up',
        'how ya doing'
    ]
    
    print('🧪 Testing Casual Conversation Handling:')
    print('=' * 60)
    
    for prompt in casual_prompts:
        # Analyze context
        context = analyzer.analyze_ultra_context(prompt)
        # Select model
        model, confidence, reasoning = analyzer.select_ultra_model(prompt)
        
        print(f'📝 Prompt: "{prompt}"')
        print(f'   🤖 Model: {model} ({confidence:.1f}%)')
        print(f'   🎯 Intent: {context["overall_context"]["primary_intent"]}')
        print(f'   🏷️  Domain: {context["overall_context"]["primary_domain"]}')
        print(f'   📤 Output: {context["overall_context"]["expected_output"]}')
        print(f'   ⭐ Quality: {context["overall_context"]["context_quality"]:.1f}%')
        print(f'   💭 Why: {reasoning[:80]}...')
        print()

if __name__ == "__main__":
    test_casual_prompts()
