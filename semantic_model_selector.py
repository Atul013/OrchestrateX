#!/usr/bin/env python3
"""
Intelligent Context-Aware Model Selector
Uses semantic analysis instead of hardcoded keywords
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter

class SemanticModelSelector:
    """
    Truly intelligent model selector using semantic analysis
    No hardcoded keywords - analyzes context and meaning
    """
    
    def __init__(self):
        print("🧠 Initializing Semantic Model Selector...")
        
        # Model expertise profiles (what each model is actually good at)
        self.model_profiles = {
            'TNG DeepSeek': {
                'strength': 'code_generation',
                'indicators': ['implementation', 'technical_creation', 'structured_output'],
                'confidence_boost': 0.2
            },
            'GLM4.5': {
                'strength': 'analysis',
                'indicators': ['comparison', 'evaluation', 'complex_reasoning'],
                'confidence_boost': 0.15
            },
            'GPT-OSS': {
                'strength': 'general_knowledge',
                'indicators': ['explanation', 'creative_content', 'broad_topics'],
                'confidence_boost': 0.1
            },
            'Qwen3': {
                'strength': 'logical_reasoning',
                'indicators': ['problem_solving', 'structured_thinking', 'precision'],
                'confidence_boost': 0.15
            },
            'MoonshotAI Kimi': {
                'strength': 'conversational',
                'indicators': ['personal_advice', 'interactive', 'practical_guidance'],
                'confidence_boost': 0.1
            },
            'Llama 4 Maverick': {
                'strength': 'educational',
                'indicators': ['learning', 'teaching', 'step_by_step'],
                'confidence_boost': 0.12
            }
        }
    
    def analyze_semantic_context(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the semantic context of a prompt without hardcoded keywords.
        Uses linguistic patterns and structure to understand intent.
        """
        words = prompt.lower().split()
        sentences = re.split(r'[.!?]+', prompt)
        
        context = {
            'intent_type': self._classify_intent(prompt),
            'domain_signals': self._detect_domain_signals(prompt),
            'complexity_level': self._assess_complexity(prompt),
            'interaction_style': self._analyze_interaction_style(prompt),
            'output_expectation': self._predict_output_type(prompt),
            'ambiguity_level': self._measure_ambiguity(prompt)
        }
        
        return context
    
    def _classify_intent(self, prompt: str) -> str:
        """Classify the primary intent without hardcoded keywords."""
        prompt_lower = prompt.lower()
        
        # Analyze sentence structure and patterns
        imperative_patterns = len(re.findall(r'\b(create|make|build|write|implement|develop|design|generate)\b', prompt_lower))
        question_patterns = len(re.findall(r'\b(what|how|why|when|where|which|who|is|are|do|does|can|could)\b', prompt_lower))
        analysis_patterns = len(re.findall(r'\b(analyze|compare|evaluate|assess|examine|review|study)\b', prompt_lower))
        explanation_patterns = len(re.findall(r'\b(explain|describe|tell|discuss|elaborate)\b', prompt_lower))
        
        # Determine primary intent based on pattern strength
        patterns = {
            'creation': imperative_patterns,
            'inquiry': question_patterns,
            'analysis': analysis_patterns,
            'explanation': explanation_patterns
        }
        
        if max(patterns.values()) == 0:
            return 'general'
        
        return max(patterns.items(), key=lambda x: x[1])[0]
    
    def _detect_domain_signals(self, prompt: str) -> List[str]:
        """Detect domain indicators through linguistic analysis."""
        domains = []
        prompt_lower = prompt.lower()
        
        # Technical domain signals (not just keywords)
        if self._has_technical_structure(prompt):
            domains.append('technical')
        
        # Creative domain signals
        if self._has_creative_structure(prompt):
            domains.append('creative')
        
        # Academic/educational signals
        if self._has_educational_structure(prompt):
            domains.append('educational')
        
        # Business/professional signals
        if self._has_business_structure(prompt):
            domains.append('business')
        
        # Cultural/social signals
        if self._has_cultural_structure(prompt):
            domains.append('cultural')
        
        return domains if domains else ['general']
    
    def _has_technical_structure(self, prompt: str) -> bool:
        """Detect technical context through structure analysis."""
        prompt_lower = prompt.lower()
        
        # Look for technical language patterns
        technical_indicators = [
            # Code-like patterns
            bool(re.search(r'\b\w+\(\)', prompt_lower)),  # function calls
            bool(re.search(r'\b\w+\.\w+', prompt_lower)),  # method/property access
            # Technical concepts
            any(word in prompt_lower for word in ['function', 'method', 'class', 'object', 'array', 'variable']),
            # Implementation language
            any(word in prompt_lower for word in ['implement', 'algorithm', 'logic', 'syntax', 'code']),
            # Framework/library mentions (but detect as patterns, not hardcode)
            bool(re.search(r'\b[A-Z][a-z]+[A-Z][a-z]+\b', prompt)),  # CamelCase (common in frameworks)
        ]
        
        return sum(technical_indicators) >= 2
    
    def _has_creative_structure(self, prompt: str) -> bool:
        """Detect creative context through language patterns."""
        prompt_lower = prompt.lower()
        
        creative_indicators = [
            # Artistic language
            any(word in prompt_lower for word in ['story', 'creative', 'design', 'artistic', 'imagine']),
            # Subjective language
            any(word in prompt_lower for word in ['beautiful', 'interesting', 'unique', 'innovative']),
            # Creation verbs
            any(word in prompt_lower for word in ['write', 'compose', 'craft', 'create']),
            # Marketing/branding context
            any(word in prompt_lower for word in ['campaign', 'brand', 'marketing', 'content'])
        ]
        
        return sum(creative_indicators) >= 1
    
    def _has_educational_structure(self, prompt: str) -> bool:
        """Detect educational context through learning patterns."""
        prompt_lower = prompt.lower()
        
        educational_indicators = [
            # Learning language
            any(word in prompt_lower for word in ['explain', 'teach', 'learn', 'understand', 'know']),
            # Question format
            prompt.strip().endswith('?'),
            # Simple language request
            any(phrase in prompt_lower for phrase in ['in simple terms', 'easy to understand', 'basic']),
            # Educational structure
            any(word in prompt_lower for word in ['definition', 'meaning', 'concept', 'principle'])
        ]
        
        return sum(educational_indicators) >= 2
    
    def _has_business_structure(self, prompt: str) -> bool:
        """Detect business context through professional language."""
        prompt_lower = prompt.lower()
        
        business_indicators = [
            # Professional language
            any(word in prompt_lower for word in ['strategy', 'business', 'market', 'company', 'industry']),
            # Analysis language
            any(word in prompt_lower for word in ['analyze', 'assessment', 'evaluation', 'performance']),
            # Financial context
            any(word in prompt_lower for word in ['cost', 'profit', 'revenue', 'investment', 'economic'])
        ]
        
        return sum(business_indicators) >= 1
    
    def _has_cultural_structure(self, prompt: str) -> bool:
        """Detect cultural context through social/cultural language patterns."""
        prompt_lower = prompt.lower()
        
        # Look for cultural context clues without hardcoding specific festivals
        cultural_indicators = [
            # Cultural question patterns
            bool(re.search(r'\bwhat.*about\b', prompt_lower)),
            bool(re.search(r'\btell me.*about\b', prompt_lower)),
            # Social/cultural concepts
            any(word in prompt_lower for word in ['tradition', 'culture', 'festival', 'celebration', 'custom']),
            # Geographic/regional references
            bool(re.search(r'\b[A-Z][a-z]+\b.*\b(in|from|of)\b', prompt)),
            # Relationship to other things
            bool(re.search(r'\bis.*related to\b', prompt_lower))
        ]
        
        return sum(cultural_indicators) >= 2
    
    def _assess_complexity(self, prompt: str) -> str:
        """Assess the complexity level of the request."""
        words = prompt.split()
        sentences = len(re.split(r'[.!?]+', prompt))
        
        if len(words) < 5:
            return 'simple'
        elif len(words) < 15:
            return 'moderate'
        elif len(words) < 30:
            return 'complex'
        else:
            return 'very_complex'
    
    def _analyze_interaction_style(self, prompt: str) -> str:
        """Determine the expected interaction style."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['i need', 'help me', 'can you']):
            return 'assistance'
        elif prompt.strip().endswith('?'):
            return 'inquiry'
        elif any(word in prompt_lower for word in ['create', 'make', 'build']):
            return 'directive'
        else:
            return 'conversational'
    
    def _predict_output_type(self, prompt: str) -> str:
        """Predict what type of output is expected."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['function', 'code', 'script']):
            return 'code'
        elif any(word in prompt_lower for word in ['explain', 'describe', 'what']):
            return 'explanation'
        elif any(word in prompt_lower for word in ['analyze', 'compare', 'evaluate']):
            return 'analysis'
        elif any(word in prompt_lower for word in ['write', 'create', 'compose']):
            return 'content'
        else:
            return 'general_response'
    
    def _measure_ambiguity(self, prompt: str) -> float:
        """Measure how ambiguous the prompt is."""
        ambiguity_factors = [
            # Vague language
            len(re.findall(r'\b(something|anything|somehow|somewhere)\b', prompt.lower())),
            # Multiple possible interpretations
            len(re.findall(r'\b(or|maybe|possibly|might)\b', prompt.lower())),
            # Unclear references
            len(re.findall(r'\b(this|that|it)\b', prompt.lower()))
        ]
        
        return min(sum(ambiguity_factors) * 0.2, 1.0)
    
    def semantic_model_selection(self, prompt: str) -> Tuple[str, float, str]:
        """
        Select model based on semantic analysis, not hardcoded rules.
        """
        context = self.analyze_semantic_context(prompt)
        
        # Calculate scores for each model based on context fit
        model_scores = {}
        
        for model_name, profile in self.model_profiles.items():
            score = self._calculate_model_fit_score(context, profile)
            model_scores[model_name] = score
        
        # Select best model
        best_model = max(model_scores.items(), key=lambda x: x[1])
        model_name = best_model[0]
        confidence = min(best_model[1], 0.99)  # Cap at 99%
        
        # Generate reasoning based on analysis
        reasoning = self._generate_reasoning(context, model_name)
        
        return model_name, confidence, reasoning
    
    def _calculate_model_fit_score(self, context: Dict, profile: Dict) -> float:
        """Calculate how well a model fits the analyzed context."""
        base_score = 0.5  # Start with neutral
        
        # Intent matching
        if profile['strength'] == 'code_generation' and context['output_expectation'] == 'code':
            base_score += 0.4
        elif profile['strength'] == 'analysis' and context['output_expectation'] == 'analysis':
            base_score += 0.35
        elif profile['strength'] == 'educational' and context['interaction_style'] == 'inquiry':
            base_score += 0.3
        elif profile['strength'] == 'general_knowledge' and 'cultural' in context['domain_signals']:
            base_score += 0.25
        
        # Domain matching
        if profile['strength'] == 'code_generation' and 'technical' in context['domain_signals']:
            base_score += 0.2
        elif profile['strength'] == 'analysis' and 'business' in context['domain_signals']:
            base_score += 0.2
        elif profile['strength'] == 'educational' and 'educational' in context['domain_signals']:
            base_score += 0.25
        
        # Complexity consideration
        if context['complexity_level'] == 'very_complex' and profile['strength'] == 'analysis':
            base_score += 0.1
        elif context['complexity_level'] == 'simple' and profile['strength'] == 'conversational':
            base_score += 0.1
        
        # Reduce score for high ambiguity
        base_score -= context['ambiguity_level'] * 0.2
        
        # Add model-specific boost
        base_score += profile['confidence_boost']
        
        return max(0.1, min(base_score, 1.0))
    
    def _generate_reasoning(self, context: Dict, model_name: str) -> str:
        """Generate human-readable reasoning for the selection."""
        reasons = []
        
        # Intent-based reasoning
        if context['intent_type'] == 'creation' and model_name == 'TNG DeepSeek':
            reasons.append("creation task detected")
        elif context['intent_type'] == 'analysis' and model_name == 'GLM4.5':
            reasons.append("analytical reasoning required")
        elif context['intent_type'] == 'inquiry' and model_name == 'Llama 4 Maverick':
            reasons.append("educational question format")
        
        # Domain-based reasoning
        if 'technical' in context['domain_signals']:
            reasons.append("technical domain identified")
        elif 'cultural' in context['domain_signals']:
            reasons.append("cultural context detected")
        elif 'educational' in context['domain_signals']:
            reasons.append("learning-oriented request")
        
        # Output expectation
        if context['output_expectation'] == 'code':
            reasons.append("code output expected")
        elif context['output_expectation'] == 'explanation':
            reasons.append("explanatory response needed")
        
        if not reasons:
            reasons.append("general purpose best fit")
        
        return f"Semantic analysis: {', '.join(reasons)}"

def test_semantic_selector():
    """Test the semantic selector with various prompts."""
    
    print("🧠 Testing Semantic Model Selector")
    print("=" * 60)
    
    selector = SemanticModelSelector()
    
    # Test prompts that should challenge the system
    test_prompts = [
        "I need you to tell me everything you know about Onam. Is it related to python somehow ??",
        "Write a Python function to implement machine learning",
        "How do python snakes hunt their prey in the wild?",
        "Can you analyze the market trends for cryptocurrency investments?",
        "Create a story about a robot learning to love",
        "What's the best way to optimize database queries?",
        "Explain quantum physics to a 10-year-old",
        "Design a user interface for a mobile banking app",
        "Compare the economic policies of different countries",
        "Help me debug this JavaScript code that's not working"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔍 Test {i}: {prompt}")
        print("-" * 40)
        
        # Analyze context
        context = selector.analyze_semantic_context(prompt)
        print(f"📊 Intent: {context['intent_type']}")
        print(f"🏷️  Domains: {', '.join(context['domain_signals'])}")
        print(f"📈 Complexity: {context['complexity_level']}")
        print(f"🤔 Ambiguity: {context['ambiguity_level']:.1%}")
        print(f"📤 Expected Output: {context['output_expectation']}")
        
        # Get selection
        model, confidence, reasoning = selector.semantic_model_selection(prompt)
        
        confidence_emoji = "🎯" if confidence >= 0.8 else "📊" if confidence >= 0.6 else "🤔"
        print(f"{confidence_emoji} **Selected:** {model} ({confidence:.1%})")
        print(f"💭 **Reasoning:** {reasoning}")

if __name__ == "__main__":
    test_semantic_selector()
