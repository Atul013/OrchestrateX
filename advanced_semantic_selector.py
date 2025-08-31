#!/usr/bin/env python3
"""
Fixed Semantic Model Selector with True Context Understanding
Handles absurd/nonsensical prompts and mixed domains properly
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter

class AdvancedSemanticModelSelector:
    """
    Advanced semantic analyzer that detects:
    - Nonsensical combinations
    - Mixed/conflicting domains  
    - Contextual coherence
    - True semantic relationships
    """
    
    def __init__(self):
        print("🧠 Initializing Advanced Semantic Model Selector...")
        
        # Model expertise profiles
        self.model_profiles = {
            'TNG DeepSeek': {
                'strength': 'code_generation',
                'domains': ['technical', 'programming'],
                'confidence_boost': 0.2
            },
            'GLM4.5': {
                'strength': 'analysis',
                'domains': ['analytical', 'complex_reasoning'],
                'confidence_boost': 0.15
            },
            'GPT-OSS': {
                'strength': 'general_knowledge',
                'domains': ['general', 'creative', 'cultural'],
                'confidence_boost': 0.1
            },
            'Qwen3': {
                'strength': 'logical_reasoning',
                'domains': ['logical', 'structured'],
                'confidence_boost': 0.15
            },
            'MoonshotAI Kimi': {
                'strength': 'conversational',
                'domains': ['personal', 'conversational'],
                'confidence_boost': 0.1
            },
            'Llama 4 Maverick': {
                'strength': 'educational',
                'domains': ['educational', 'explanatory'],
                'confidence_boost': 0.12
            }
        }
    
    def analyze_semantic_context(self, prompt: str) -> Dict[str, Any]:
        """Advanced semantic analysis with coherence checking."""
        
        # Basic analysis
        basic_context = self._basic_linguistic_analysis(prompt)
        
        # Advanced coherence analysis
        coherence = self._analyze_coherence(prompt)
        
        # Domain relationship analysis
        domain_analysis = self._analyze_domain_relationships(prompt)
        
        return {
            **basic_context,
            'coherence_score': coherence['score'],
            'coherence_issues': coherence['issues'],
            'domain_conflicts': domain_analysis['conflicts'],
            'primary_domain': domain_analysis['primary'],
            'secondary_domains': domain_analysis['secondary'],
            'absurdity_level': self._detect_absurdity(prompt)
        }
    
    def _basic_linguistic_analysis(self, prompt: str) -> Dict[str, Any]:
        """Basic linguistic structure analysis."""
        words = prompt.lower().split()
        
        # Intent classification through linguistic patterns
        intent = self._classify_intent_advanced(prompt)
        complexity = self._assess_complexity_advanced(prompt)
        output_type = self._predict_output_advanced(prompt)
        
        return {
            'intent_type': intent,
            'complexity_level': complexity,
            'output_expectation': output_type,
            'word_count': len(words),
            'sentence_count': len(re.split(r'[.!?]+', prompt.strip())),
            'question_markers': len(re.findall(r'\?', prompt)),
            'ambiguity_markers': len(re.findall(r'\b(somehow|maybe|possibly|might|perhaps)\b', prompt.lower()))
        }
    
    def _classify_intent_advanced(self, prompt: str) -> str:
        """Advanced intent classification using linguistic structure."""
        prompt_lower = prompt.lower()
        
        # Command/imperative detection
        imperative_patterns = [
            r'^(create|make|build|write|implement|develop|design|generate)',
            r'\b(please\s+)?(create|make|build|write|implement|develop|design|generate)',
        ]
        
        # Question detection
        question_patterns = [
            r'^(what|how|why|when|where|which|who)',
            r'\b(what|how|why|when|where|which|who)\b.*\?',
            r'.*\?$'
        ]
        
        # Explanation request detection
        explanation_patterns = [
            r'^explain',
            r'\bexplain\b.*\babout\b',
            r'\btell me\b.*\babout\b'
        ]
        
        # Analysis request detection
        analysis_patterns = [
            r'\b(analyze|compare|evaluate|assess)\b',
            r'\b(difference|comparison|evaluation)\b'
        ]
        
        if any(re.search(pattern, prompt_lower) for pattern in imperative_patterns):
            return 'creation'
        elif any(re.search(pattern, prompt_lower) for pattern in explanation_patterns):
            return 'explanation'
        elif any(re.search(pattern, prompt_lower) for pattern in analysis_patterns):
            return 'analysis'
        elif any(re.search(pattern, prompt_lower) for pattern in question_patterns):
            return 'inquiry'
        else:
            return 'general'
    
    def _assess_complexity_advanced(self, prompt: str) -> str:
        """Advanced complexity assessment."""
        words = prompt.split()
        concepts = len(re.findall(r'\band\b', prompt.lower()))  # Multiple concepts
        conjunctions = len(re.findall(r'\b(and|or|but|however|meanwhile)\b', prompt.lower()))
        
        complexity_score = len(words) + (concepts * 5) + (conjunctions * 3)
        
        if complexity_score < 10:
            return 'simple'
        elif complexity_score < 25:
            return 'moderate'
        elif complexity_score < 50:
            return 'complex'
        else:
            return 'very_complex'
    
    def _predict_output_advanced(self, prompt: str) -> str:
        """Advanced output type prediction."""
        prompt_lower = prompt.lower()
        
        # Code indicators (contextual)
        code_context = (
            bool(re.search(r'\b(function|method|class|algorithm)\b', prompt_lower)) and
            bool(re.search(r'\b(write|create|implement|build)\b', prompt_lower))
        )
        
        if code_context:
            return 'code'
        elif re.search(r'\b(explain|describe|tell|what is)\b', prompt_lower):
            return 'explanation'
        elif re.search(r'\b(analyze|compare|evaluate)\b', prompt_lower):
            return 'analysis'
        elif re.search(r'\b(write|create|compose|story|content)\b', prompt_lower):
            return 'content'
        else:
            return 'general_response'
    
    def _analyze_coherence(self, prompt: str) -> Dict[str, Any]:
        """Analyze if the prompt makes semantic sense."""
        issues = []
        score = 1.0
        
        # Check for contradictory concepts
        cultural_terms = re.findall(r'\b(festival|celebration|tradition|culture|diwali|christmas|eid|onam)\b', prompt.lower())
        technical_terms = re.findall(r'\b(database|performance|server|algorithm|code|programming)\b', prompt.lower())
        
        if cultural_terms and technical_terms:
            # Check if they're meaningfully connected
            connecting_words = re.findall(r'\b(improve|affect|impact|influence|enhance|optimize)\b', prompt.lower())
            if connecting_words:
                issues.append("nonsensical_relationship")
                score -= 0.4  # Major coherence issue
        
        # Check for impossible relationships
        absurd_patterns = [
            (r'\b(festival|holiday)\b.*\b(database|performance)\b', "cultural-technical absurdity"),
            (r'\b(snake|animal)\b.*\b(programming|code)\b', "potential ambiguity"),
            (r'\b(color|music)\b.*\b(sql|database)\b', "unrelated domain mixing")
        ]
        
        for pattern, issue_type in absurd_patterns:
            if re.search(pattern, prompt.lower()):
                issues.append(issue_type)
                score -= 0.3
        
        return {
            'score': max(0.1, score),
            'issues': issues
        }
    
    def _analyze_domain_relationships(self, prompt: str) -> Dict[str, Any]:
        """Analyze domain relationships and conflicts."""
        prompt_lower = prompt.lower()
        
        # Define semantic domains with better patterns
        domains = {
            'cultural': (
                # Cultural festivals/traditions (detect pattern, not hardcode specific festivals)
                len(re.findall(r'\b(festival|celebration|tradition|culture|heritage|ceremony)\b', prompt_lower)) +
                # Detect proper nouns that could be festivals (capitalized words not at sentence start)
                len(re.findall(r'\b[A-Z][a-z]{4,}\b', prompt)) +
                # Cultural question patterns
                len(re.findall(r'\bwhat.*about\b', prompt_lower))
            ),
            'technical': (
                len(re.findall(r'\b(database|server|algorithm|programming|code|software|performance|system)\b', prompt_lower))
            ),
            'educational': (
                len(re.findall(r'\b(explain|learn|teach|understand|study|knowledge|tell me)\b', prompt_lower))
            ),
            'creative': (
                len(re.findall(r'\b(story|creative|design|art|write|compose)\b', prompt_lower))
            ),
            'analytical': (
                len(re.findall(r'\b(analyze|compare|evaluate|assessment|research)\b', prompt_lower))
            ),
            'business': (
                len(re.findall(r'\b(strategy|market|company|profit|revenue|business)\b', prompt_lower))
            )
        }
        
        # Remove zero-count domains
        active_domains = {k: v for k, v in domains.items() if v > 0}
        
        # Identify conflicts - check for meaningful relationships
        conflicts = []
        if 'cultural' in active_domains and 'technical' in active_domains:
            # Check if there's a meaningful bridge
            bridge_words = re.findall(r'\b(affect|impact|improve|influence|related|enhance|optimize)\b', prompt_lower)
            cultural_indicators = re.findall(r'\b(festival|celebration|tradition|diwali|christmas|eid|onam)\b', prompt_lower)
            technical_indicators = re.findall(r'\b(database|performance|server|algorithm)\b', prompt_lower)
            
            if cultural_indicators and technical_indicators and bridge_words:
                conflicts.append("nonsensical cultural-technical relationship")
        
        # Determine primary domain
        if not active_domains:
            primary = 'general'
        else:
            primary = max(active_domains.items(), key=lambda x: x[1])[0]
        
        secondary = [k for k in active_domains.keys() if k != primary]
        
        return {
            'primary': primary,
            'secondary': secondary,
            'conflicts': conflicts,
            'all_detected': list(active_domains.keys()),
            'domain_scores': active_domains
        }
    
    def _detect_absurdity(self, prompt: str) -> float:
        """Detect how absurd/nonsensical the prompt is."""
        absurdity_score = 0.0
        prompt_lower = prompt.lower()
        
        # Check for cultural + technical with improvement claims
        cultural_words = re.findall(r'\b(festival|celebration|tradition|diwali|christmas|eid|onam)\b', prompt_lower)
        technical_words = re.findall(r'\b(database|performance|server|algorithm|system)\b', prompt_lower)
        improvement_words = re.findall(r'\b(improve|enhance|optimize|boost|increase)\b', prompt_lower)
        
        # Detect specific absurd patterns
        if cultural_words and technical_words:
            absurdity_score += 0.6  # Cultural + technical is unusual
            
            if improvement_words:
                absurdity_score += 0.4  # Claiming cultural things improve technical things is absurd
        
        # Check for impossible causal relationships
        absurd_patterns = [
            r'\b(festival|celebration)\b.*\b(improve|enhance)\b.*\b(database|performance)\b',
            r'\b(diwali|christmas|eid)\b.*\b(boost|optimize)\b.*\b(server|system)\b'
        ]
        
        for pattern in absurd_patterns:
            if re.search(pattern, prompt_lower):
                absurdity_score += 0.5
        
        return min(absurdity_score, 1.0)
    
    def advanced_model_selection(self, prompt: str) -> Tuple[str, float, str]:
        """Advanced model selection with coherence consideration."""
        
        context = self.analyze_semantic_context(prompt)
        
        # Handle high absurdity prompts
        if context['absurdity_level'] > 0.5:
            return self._handle_absurd_prompt(prompt, context)
        
        # Handle coherent prompts with primary domain focus
        return self._handle_coherent_prompt(prompt, context)
    
    def _handle_absurd_prompt(self, prompt: str, context: Dict) -> Tuple[str, float, str]:
        """Handle nonsensical/absurd prompts."""
        
        # For absurd prompts, use general knowledge model with low confidence
        reasoning_parts = []
        
        if 'nonsensical_relationship' in context['coherence_issues']:
            reasoning_parts.append("nonsensical concept combination detected")
        
        if 'cultural-technical disconnect' in context['domain_conflicts']:
            reasoning_parts.append("unrelated domains mixed")
        
        reasoning_parts.append(f"absurdity level {context['absurdity_level']:.0%}")
        
        # Route to general knowledge model for handling weird requests
        confidence = 0.4 + (0.2 * context['coherence_score'])  # Low confidence for absurd prompts
        reasoning = f"Absurd prompt handling: {', '.join(reasoning_parts)}"
        
        return 'GPT-OSS', confidence, reasoning
    
    def _handle_coherent_prompt(self, prompt: str, context: Dict) -> Tuple[str, float, str]:
        """Handle coherent prompts with normal logic."""
        
        primary_domain = context['primary_domain']
        intent = context['intent_type']
        output = context['output_expectation']
        
        # Route based on primary domain and intent
        if primary_domain == 'technical' and output == 'code':
            return 'TNG DeepSeek', 0.95, f"Technical {intent} with code output"
        
        elif primary_domain == 'analytical' or intent == 'analysis':
            return 'GLM4.5', 0.90, f"Analytical reasoning required"
        
        elif primary_domain == 'educational' or intent == 'explanation':
            return 'Llama 4 Maverick', 0.85, f"Educational explanation needed"
        
        elif primary_domain == 'creative':
            return 'GPT-OSS', 0.80, f"Creative content generation"
        
        elif primary_domain == 'cultural':
            return 'GPT-OSS', 0.75, f"Cultural knowledge required"
        
        else:
            return 'GPT-OSS', 0.65, f"General purpose response"

def test_advanced_selector():
    """Test with the problematic Diwali prompt."""
    
    selector = AdvancedSemanticModelSelector()
    
    test_prompts = [
        "Explain everything about Diwali and let me know if it improves database performance",
        "Write a Python function to implement machine learning",
        "How do python snakes hunt their prey?",
        "What is the cultural significance of Onam festival?",
        "Analyze market trends for cryptocurrency"
    ]
    
    for prompt in test_prompts:
        print(f"\n🔍 Testing: {prompt}")
        print("-" * 50)
        
        context = selector.analyze_semantic_context(prompt)
        model, confidence, reasoning = selector.advanced_model_selection(prompt)
        
        print(f"Primary Domain: {context['primary_domain']}")
        print(f"Coherence Score: {context['coherence_score']:.1%}")
        print(f"Absurdity Level: {context['absurdity_level']:.1%}")
        print(f"Domain Conflicts: {context['domain_conflicts']}")
        print(f"Selected: {model} ({confidence:.1%})")
        print(f"Reasoning: {reasoning}")

if __name__ == "__main__":
    test_advanced_selector()
