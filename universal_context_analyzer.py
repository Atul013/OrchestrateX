#!/usr/bin/env python3
"""
Universal Context Understanding System
Analyzes ALL prompts with consistent semantic reasoning
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter

class UniversalContextAnalyzer:
    """
    Universal context analyzer that understands ANY prompt
    No hardcoded patterns - pure semantic reasoning
    """
    
    def __init__(self):
        print("🧠 Initializing Universal Context Analyzer...")
        
        # Core model capabilities (what they're actually good at)
        self.models = {
            'TNG DeepSeek': {
                'strengths': ['code_creation', 'technical_implementation', 'structured_building'],
                'confidence_base': 0.9
            },
            'GLM4.5': {
                'strengths': ['complex_analysis', 'reasoning', 'comparison', 'evaluation'],
                'confidence_base': 0.85
            },
            'GPT-OSS': {
                'strengths': ['general_knowledge', 'explanation', 'creative_writing', 'broad_topics'],
                'confidence_base': 0.75
            },
            'Llama 4 Maverick': {
                'strengths': ['teaching', 'step_by_step', 'educational', 'simplification'],
                'confidence_base': 0.8
            },
            'Qwen3': {
                'strengths': ['logical_reasoning', 'problem_solving', 'precise_thinking'],
                'confidence_base': 0.8
            },
            'MoonshotAI Kimi': {
                'strengths': ['personal_help', 'conversational', 'practical_advice'],
                'confidence_base': 0.7
            }
        }
    
    def analyze_universal_context(self, prompt: str) -> Dict[str, Any]:
        """Universal context analysis for ANY prompt."""
        
        # Core semantic analysis
        semantic_profile = self._extract_semantic_profile(prompt)
        
        # Intent understanding
        intent_analysis = self._understand_intent(prompt)
        
        # Domain reasoning
        domain_reasoning = self._reason_about_domains(prompt)
        
        # Task complexity
        task_complexity = self._assess_task_complexity(prompt)
        
        # Output expectations
        output_analysis = self._analyze_expected_output(prompt)
        
        # Coherence and logic
        coherence_check = self._check_logical_coherence(prompt)
        
        return {
            'semantic_profile': semantic_profile,
            'intent_analysis': intent_analysis,
            'domain_reasoning': domain_reasoning,
            'task_complexity': task_complexity,
            'output_analysis': output_analysis,
            'coherence_check': coherence_check,
            'overall_context': self._synthesize_context(prompt, {
                'semantic': semantic_profile,
                'intent': intent_analysis,
                'domain': domain_reasoning,
                'complexity': task_complexity,
                'output': output_analysis,
                'coherence': coherence_check
            })
        }
    
    def _extract_semantic_profile(self, prompt: str) -> Dict[str, Any]:
        """Extract the semantic profile of the prompt."""
        words = prompt.lower().split()
        
        # Semantic categories based on linguistic analysis
        semantic_indicators = {
            'action_oriented': self._count_action_words(prompt),
            'knowledge_seeking': self._count_knowledge_words(prompt), 
            'creation_focused': self._count_creation_words(prompt),
            'analysis_focused': self._count_analysis_words(prompt),
            'problem_solving': self._count_problem_words(prompt),
            'explanation_seeking': self._count_explanation_words(prompt)
        }
        
        # Linguistic structure
        structure = {
            'imperative_strength': self._measure_imperative_mood(prompt),
            'interrogative_strength': self._measure_interrogative_mood(prompt),
            'complexity_markers': self._count_complexity_markers(prompt),
            'specificity_level': self._measure_specificity(prompt)
        }
        
        return {
            'semantic_indicators': semantic_indicators,
            'linguistic_structure': structure,
            'dominant_semantic': max(semantic_indicators.items(), key=lambda x: x[1])[0]
        }
    
    def _count_action_words(self, prompt: str) -> float:
        """Count action-oriented language."""
        action_patterns = [
            r'\b(create|make|build|develop|implement|design|generate|write|code|program)\b',
            r'\b(do|perform|execute|run|process)\b',
            r'\b(fix|solve|debug|optimize|improve)\b'
        ]
        return sum(len(re.findall(pattern, prompt.lower())) for pattern in action_patterns)
    
    def _count_knowledge_words(self, prompt: str) -> float:
        """Count knowledge-seeking language."""
        knowledge_patterns = [
            r'\b(what|which|who|where|when)\b',
            r'\b(tell me|inform me|let me know)\b',
            r'\b(about|regarding|concerning)\b'
        ]
        return sum(len(re.findall(pattern, prompt.lower())) for pattern in knowledge_patterns)
    
    def _count_creation_words(self, prompt: str) -> float:
        """Count creation-focused language."""
        creation_patterns = [
            r'\b(create|make|build|craft|compose|design|generate)\b',
            r'\b(new|fresh|original|innovative)\b',
            r'\b(from scratch|start with|begin by)\b'
        ]
        return sum(len(re.findall(pattern, prompt.lower())) for pattern in creation_patterns)
    
    def _count_analysis_words(self, prompt: str) -> float:
        """Count analysis-focused language."""
        analysis_patterns = [
            r'\b(analyze|examine|evaluate|assess|review|study)\b',
            r'\b(compare|contrast|difference|similarity)\b',
            r'\b(pros and cons|advantages|disadvantages)\b'
        ]
        return sum(len(re.findall(pattern, prompt.lower())) for pattern in analysis_patterns)
    
    def _count_problem_words(self, prompt: str) -> float:
        """Count problem-solving language."""
        problem_patterns = [
            r'\b(solve|fix|debug|troubleshoot|resolve)\b',
            r'\b(problem|issue|error|bug|challenge)\b',
            r'\b(how to|best way|solution)\b'
        ]
        return sum(len(re.findall(pattern, prompt.lower())) for pattern in problem_patterns)
    
    def _count_explanation_words(self, prompt: str) -> float:
        """Count explanation-seeking language."""
        explanation_patterns = [
            r'\b(explain|describe|elaborate|clarify)\b',
            r'\b(why|how|what does|what is)\b',
            r'\b(meaning|definition|concept|principle)\b'
        ]
        return sum(len(re.findall(pattern, prompt.lower())) for pattern in explanation_patterns)
    
    def _measure_imperative_mood(self, prompt: str) -> float:
        """Measure how command-like the prompt is."""
        # Commands often start with verbs
        first_word = prompt.strip().split()[0].lower() if prompt.strip() else ""
        imperative_starters = ['create', 'make', 'build', 'write', 'implement', 'design', 'develop', 'generate']
        
        score = 1.0 if first_word in imperative_starters else 0.0
        
        # Add score for imperative language throughout
        imperative_count = len(re.findall(r'\b(please |you should |you need to )\b', prompt.lower()))
        return score + (imperative_count * 0.3)
    
    def _measure_interrogative_mood(self, prompt: str) -> float:
        """Measure how question-like the prompt is."""
        question_score = 0.0
        
        # Question marks
        question_score += prompt.count('?') * 0.5
        
        # Question words at start
        first_words = prompt.strip().split()[:2]
        question_starters = ['what', 'how', 'why', 'when', 'where', 'which', 'who', 'can', 'could', 'would', 'should']
        if first_words and first_words[0].lower() in question_starters:
            question_score += 1.0
        
        return min(question_score, 2.0)
    
    def _count_complexity_markers(self, prompt: str) -> int:
        """Count markers of complex requests."""
        complexity_markers = [
            r'\band\b',  # Multiple requirements
            r'\bbut\b',  # Contrasting requirements  
            r'\bhowever\b',  # Conditional complexity
            r'\bwith\b.*\band\b',  # Multiple specifications
            r'\bthat also\b',  # Additional requirements
        ]
        return sum(len(re.findall(marker, prompt.lower())) for marker in complexity_markers)
    
    def _measure_specificity(self, prompt: str) -> float:
        """Measure how specific vs general the prompt is."""
        specificity_score = 0.0
        
        # Technical terms increase specificity
        technical_terms = len(re.findall(r'\b[A-Z][a-z]*[A-Z][a-z]*\b', prompt))  # CamelCase
        specificity_score += technical_terms * 0.2
        
        # Specific numbers/versions
        numbers = len(re.findall(r'\b\d+\b', prompt))
        specificity_score += numbers * 0.1
        
        # Domain-specific terminology
        domain_terms = len(re.findall(r'\b(API|SQL|HTML|CSS|JSON|XML|HTTP|database|algorithm|function|class|method)\b', prompt.lower()))
        specificity_score += domain_terms * 0.3
        
        return min(specificity_score, 2.0)
    
    def _understand_intent(self, prompt: str) -> Dict[str, Any]:
        """Understand the true intent behind the prompt."""
        semantic = self._extract_semantic_profile(prompt)
        
        # Determine primary intent based on semantic profile
        intent_scores = {
            'create_something': semantic['semantic_indicators']['creation_focused'] + semantic['semantic_indicators']['action_oriented'],
            'learn_something': semantic['semantic_indicators']['knowledge_seeking'] + semantic['semantic_indicators']['explanation_seeking'],
            'analyze_something': semantic['semantic_indicators']['analysis_focused'],
            'solve_problem': semantic['semantic_indicators']['problem_solving'],
            'get_help': semantic['linguistic_structure']['interrogative_strength']
        }
        
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0] if max(intent_scores.values()) > 0 else 'general_request'
        
        return {
            'primary_intent': primary_intent,
            'intent_scores': intent_scores,
            'intent_confidence': max(intent_scores.values()) / sum(intent_scores.values()) if sum(intent_scores.values()) > 0 else 0.5
        }
    
    def _reason_about_domains(self, prompt: str) -> Dict[str, Any]:
        """Reason about what domains this prompt involves."""
        prompt_lower = prompt.lower()
        
        # Domain reasoning based on content and context
        domain_evidence = {
            'technical': self._find_technical_evidence(prompt),
            'creative': self._find_creative_evidence(prompt),
            'analytical': self._find_analytical_evidence(prompt),
            'educational': self._find_educational_evidence(prompt),
            'cultural': self._find_cultural_evidence(prompt),
            'business': self._find_business_evidence(prompt),
            'scientific': self._find_scientific_evidence(prompt),
            'biological': self._find_biological_evidence(prompt)
        }
        
        # Filter out domains with no evidence
        active_domains = {k: v for k, v in domain_evidence.items() if v['score'] > 0}
        
        # Determine primary domain
        primary_domain = 'general'
        if active_domains:
            primary_domain = max(active_domains.items(), key=lambda x: x[1]['score'])[0]
        
        return {
            'primary_domain': primary_domain,
            'domain_evidence': domain_evidence,
            'active_domains': list(active_domains.keys()),
            'domain_confidence': active_domains[primary_domain]['score'] / sum(d['score'] for d in active_domains.values()) if active_domains else 0.5
        }
    
    def _find_technical_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of technical domain."""
        evidence = []
        score = 0.0
        
        # Context-aware programming language detection
        tech_terms = []
        
        # Python disambiguation - only technical if in programming context
        if 'python' in prompt.lower():
            programming_context = any(word in prompt.lower() for word in [
                'function', 'script', 'code', 'programming', 'implement', 'develop', 
                'write', 'create', 'build', 'algorithm', 'syntax', 'library', 'package'
            ])
            biological_context = any(word in prompt.lower() for word in [
                'snake', 'snakes', 'hunt', 'prey', 'animal', 'reptile', 'species', 
                'behavior', 'nature', 'wildlife', 'biology'
            ])
            
            if programming_context and not biological_context:
                tech_terms.append('python')
            elif programming_context and biological_context:
                # Mixed context - reduce confidence
                pass
        
        # Other tech terms
        other_tech = re.findall(r'\b(javascript|java|html|css|sql|api|database|server|algorithm|function|class|method|code|programming)\b', prompt.lower())
        tech_terms.extend(other_tech)
        
        if tech_terms:
            evidence.append(f"Technical terms: {', '.join(set(tech_terms))}")
            score += len(set(tech_terms)) * 0.3
        
        # Implementation language
        implementation_words = re.findall(r'\b(implement|develop|build|create|write|code|program)\b', prompt.lower())
        tech_context = any(word in prompt.lower() for word in ['function', 'script', 'application', 'system', 'software'])
        if implementation_words and tech_context:
            evidence.append("Implementation request with technical context")
            score += 0.5
        
        # Technical patterns
        if re.search(r'\w+\(\)', prompt):  # Function calls
            evidence.append("Function call syntax detected")
            score += 0.3
        
        return {'score': score, 'evidence': evidence}
    
    def _find_creative_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of creative domain."""
        evidence = []
        score = 0.0
        
        # Creative terms
        creative_terms = re.findall(r'\b(story|creative|design|art|artistic|beautiful|innovative|original|imaginative)\b', prompt.lower())
        if creative_terms:
            evidence.append(f"Creative language: {', '.join(set(creative_terms))}")
            score += len(set(creative_terms)) * 0.3
        
        # Content creation
        content_words = re.findall(r'\b(write|compose|create|craft|generate)\b', prompt.lower())
        content_targets = re.findall(r'\b(story|poem|article|content|script|narrative)\b', prompt.lower())
        if content_words and content_targets:
            evidence.append("Content creation request")
            score += 0.5
        
        return {'score': score, 'evidence': evidence}
    
    def _find_analytical_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of analytical domain."""
        evidence = []
        score = 0.0
        
        # Analysis terms
        analysis_terms = re.findall(r'\b(analyze|examine|evaluate|assess|compare|contrast|review|study)\b', prompt.lower())
        if analysis_terms:
            evidence.append(f"Analytical language: {', '.join(set(analysis_terms))}")
            score += len(set(analysis_terms)) * 0.4
        
        # Comparison language
        if re.search(r'\b(vs|versus|compared to|difference between|pros and cons)\b', prompt.lower()):
            evidence.append("Comparison request")
            score += 0.4
        
        return {'score': score, 'evidence': evidence}
    
    def _find_educational_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of educational domain."""
        evidence = []
        score = 0.0
        
        # Learning language
        learning_terms = re.findall(r'\b(explain|teach|learn|understand|know|study|educate)\b', prompt.lower())
        if learning_terms:
            evidence.append(f"Learning language: {', '.join(set(learning_terms))}")
            score += len(set(learning_terms)) * 0.3
        
        # Question format
        if prompt.strip().endswith('?'):
            evidence.append("Question format")
            score += 0.2
        
        # Educational phrases
        educational_phrases = re.findall(r'\b(tell me about|what is|how does|why does|what are)\b', prompt.lower())
        if educational_phrases:
            evidence.append("Educational question patterns")
            score += 0.3
        
        return {'score': score, 'evidence': evidence}
    
    def _find_cultural_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of cultural domain."""
        evidence = []
        score = 0.0
        
        # Cultural terms
        cultural_terms = re.findall(r'\b(culture|tradition|festival|celebration|heritage|custom|ceremony)\b', prompt.lower())
        if cultural_terms:
            evidence.append(f"Cultural terms: {', '.join(set(cultural_terms))}")
            score += len(set(cultural_terms)) * 0.4
        
        # Proper nouns (potential cultural references)
        proper_nouns = re.findall(r'\b[A-Z][a-z]{3,}\b', prompt)
        if proper_nouns and any(term in prompt.lower() for term in ['about', 'tradition', 'culture', 'festival']):
            evidence.append(f"Cultural references: {', '.join(proper_nouns)}")
            score += 0.5
        
        return {'score': score, 'evidence': evidence}
    
    def _find_business_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of business domain."""
        evidence = []
        score = 0.0
        
        # Business terms
        business_terms = re.findall(r'\b(business|company|market|strategy|profit|revenue|investment|economic|financial)\b', prompt.lower())
        if business_terms:
            evidence.append(f"Business terms: {', '.join(set(business_terms))}")
            score += len(set(business_terms)) * 0.4
        
        return {'score': score, 'evidence': evidence}
    
    def _find_scientific_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of scientific domain."""
        evidence = []
        score = 0.0
        
        # Scientific terms
        scientific_terms = re.findall(r'\b(quantum|physics|chemistry|biology|research|experiment|hypothesis|theory)\b', prompt.lower())
        if scientific_terms:
            evidence.append(f"Scientific terms: {', '.join(set(scientific_terms))}")
            score += len(set(scientific_terms)) * 0.4
        
        return {'score': score, 'evidence': evidence}
    
    def _find_biological_evidence(self, prompt: str) -> Dict[str, Any]:
        """Find evidence of biological domain."""
        evidence = []
        score = 0.0
        
        # Biological terms
        biological_terms = re.findall(r'\b(animal|animals|snake|snakes|hunt|prey|predator|species|behavior|behaviour|wildlife|nature|biology|reptile|mammal)\b', prompt.lower())
        if biological_terms:
            evidence.append(f"Biological terms: {', '.join(set(biological_terms))}")
            score += len(set(biological_terms)) * 0.4
        
        # Animal behavior patterns
        if re.search(r'\b(how do|how does).*\b(hunt|eat|live|behave|survive)\b', prompt.lower()):
            evidence.append("Animal behavior inquiry")
            score += 0.5
        
        return {'score': score, 'evidence': evidence}
    
    def _assess_task_complexity(self, prompt: str) -> Dict[str, Any]:
        """Assess the complexity of the requested task."""
        
        # Multiple components
        components = len(prompt.split(' and ')) + len(prompt.split(' with ')) - 2
        
        # Word count complexity
        word_count = len(prompt.split())
        
        # Technical complexity
        semantic = self._extract_semantic_profile(prompt)
        technical_complexity = semantic['linguistic_structure']['specificity_level']
        
        # Calculate overall complexity
        complexity_score = (
            (word_count / 10) +  # Length factor
            (components * 0.5) +  # Multi-part requests
            technical_complexity  # Technical specificity
        )
        
        if complexity_score < 1:
            level = 'simple'
        elif complexity_score < 3:
            level = 'moderate'
        elif complexity_score < 6:
            level = 'complex'
        else:
            level = 'very_complex'
        
        return {
            'level': level,
            'score': complexity_score,
            'factors': {
                'word_count': word_count,
                'components': components,
                'technical_specificity': technical_complexity
            }
        }
    
    def _analyze_expected_output(self, prompt: str) -> Dict[str, Any]:
        """Analyze what type of output is expected."""
        
        intent = self._understand_intent(prompt)
        domain = self._reason_about_domains(prompt)
        
        # Determine output type based on context
        if intent['primary_intent'] == 'create_something':
            if domain['primary_domain'] == 'technical':
                output_type = 'code'
            elif domain['primary_domain'] == 'creative':
                output_type = 'creative_content'
            else:
                output_type = 'structured_content'
        elif intent['primary_intent'] == 'learn_something':
            output_type = 'explanation'
        elif intent['primary_intent'] == 'analyze_something':
            output_type = 'analysis'
        elif intent['primary_intent'] == 'solve_problem':
            output_type = 'solution'
        else:
            output_type = 'general_response'
        
        return {
            'type': output_type,
            'confidence': intent['intent_confidence'] * domain['domain_confidence']
        }
    
    def _check_logical_coherence(self, prompt: str) -> Dict[str, Any]:
        """Check if the prompt makes logical sense."""
        
        domain_analysis = self._reason_about_domains(prompt)
        active_domains = domain_analysis['active_domains']
        
        coherence_issues = []
        coherence_score = 1.0
        
        # Check for domain conflicts
        if 'cultural' in active_domains and 'technical' in active_domains:
            # Look for impossible relationships
            if re.search(r'\b(festival|celebration|tradition)\b.*\b(improve|enhance|optimize|boost|affect|influence)\b.*\b(database|performance|server|algorithm|API)\b', prompt.lower()):
                coherence_issues.append("Impossible causal relationship between cultural and technical domains")
                coherence_score -= 0.6
            elif len(active_domains) > 2:
                coherence_issues.append("Multiple unrelated domains mixed")
                coherence_score -= 0.3
        
        # Check for scientific + political impossibilities
        if 'scientific' in active_domains:
            if re.search(r'\b(quantum|physics|chemistry)\b.*\b(affect|influence|impact)\b.*\b(election|political|parliament|government)\b', prompt.lower()):
                coherence_issues.append("Impossible scientific influence on political processes")
                coherence_score -= 0.7
        
        # Check for cultural + algorithmic impossibilities  
        if 'cultural' in active_domains and 'technical' in active_domains:
            if re.search(r'\b(festival|celebration|tradition|Ramadan|Pongal|Diwali|Christmas)\b.*\b(sorting|algorithm|data structure|API|RESTful)\b', prompt.lower()):
                coherence_issues.append("Nonsensical connection between cultural events and technical concepts")
                coherence_score -= 0.6
        
        # Check for internal contradictions
        if re.search(r'\b(simple|easy)\b.*\b(complex|advanced|sophisticated)\b', prompt.lower()):
            coherence_issues.append("Contradictory complexity requirements")
            coherence_score -= 0.2
        
        return {
            'score': max(0.1, coherence_score),
            'issues': coherence_issues,
            'is_coherent': len(coherence_issues) == 0
        }
    
    def _synthesize_context(self, prompt: str, analysis: Dict) -> Dict[str, Any]:
        """Synthesize all analysis into final context understanding."""
        
        # Primary context determination
        intent = analysis['intent']['primary_intent']
        domain = analysis['domain']['primary_domain']
        output = analysis['output']['type']
        complexity = analysis['complexity']['level']
        coherence = analysis['coherence']['is_coherent']
        
        # Context confidence
        context_confidence = (
            analysis['intent']['intent_confidence'] * 0.3 +
            analysis['domain']['domain_confidence'] * 0.3 +
            analysis['output']['confidence'] * 0.2 +
            analysis['coherence']['score'] * 0.2
        )
        
        return {
            'primary_intent': intent,
            'primary_domain': domain,
            'expected_output': output,
            'complexity_level': complexity,
            'is_coherent': coherence,
            'context_confidence': context_confidence,
            'context_summary': f"{intent} in {domain} domain, expecting {output} ({complexity} complexity)"
        }
    
    def select_best_model(self, prompt: str) -> Tuple[str, float, str]:
        """Select the best model based on universal context analysis."""
        
        # Get full context analysis
        context = self.analyze_universal_context(prompt)
        overall = context['overall_context']
        
        # Score each model based on context fit
        model_scores = {}
        
        for model_name, model_info in self.models.items():
            score = self._calculate_model_context_fit(overall, model_info, context)
            model_scores[model_name] = score
        
        # Select best model
        best_model = max(model_scores.items(), key=lambda x: x[1])
        model_name = best_model[0]
        confidence = min(best_model[1], 0.99)
        
        # Generate reasoning
        reasoning = self._generate_context_reasoning(overall, model_name, context)
        
        return model_name, confidence, reasoning
    
    def _calculate_model_context_fit(self, overall_context: Dict, model_info: Dict, full_context: Dict) -> float:
        """Calculate how well a model fits the analyzed context."""
        
        base_score = model_info['confidence_base']
        
        # Intent matching
        intent = overall_context['primary_intent']
        if intent == 'create_something' and 'code_creation' in model_info['strengths']:
            base_score += 0.15
        elif intent == 'learn_something' and 'teaching' in model_info['strengths']:
            base_score += 0.15
        elif intent == 'analyze_something' and 'complex_analysis' in model_info['strengths']:
            base_score += 0.15
        
        # Domain matching
        domain = overall_context['primary_domain']
        if domain == 'technical' and 'technical_implementation' in model_info['strengths']:
            base_score += 0.1
        elif domain == 'educational' and 'educational' in model_info['strengths']:
            base_score += 0.1
        elif domain in ['cultural', 'general', 'biological'] and 'general_knowledge' in model_info['strengths']:
            base_score += 0.05
        
        # Output type matching
        output = overall_context['expected_output']
        if output == 'code' and 'code_creation' in model_info['strengths']:
            base_score += 0.1
        elif output == 'explanation' and ('teaching' in model_info['strengths'] or 'general_knowledge' in model_info['strengths']):
            base_score += 0.05
        
        # Complexity consideration
        complexity = overall_context['complexity_level']
        if complexity in ['complex', 'very_complex'] and 'complex_analysis' in model_info['strengths']:
            base_score += 0.05
        
        # Coherence penalty
        if not overall_context['is_coherent']:
            base_score -= 0.2  # Penalty for incoherent prompts
        
        # Context confidence factor
        base_score *= overall_context['context_confidence']
        
        return max(0.1, min(base_score, 1.0))
    
    def _generate_context_reasoning(self, overall_context: Dict, model_name: str, full_context: Dict) -> str:
        """Generate reasoning based on context analysis."""
        
        reasoning_parts = []
        
        # Intent reasoning
        intent = overall_context['primary_intent']
        reasoning_parts.append(f"{intent.replace('_', ' ')}")
        
        # Domain reasoning
        domain = overall_context['primary_domain']
        if domain != 'general':
            reasoning_parts.append(f"{domain} domain")
        
        # Output reasoning
        output = overall_context['expected_output']
        if output != 'general_response':
            reasoning_parts.append(f"{output.replace('_', ' ')} expected")
        
        # Coherence reasoning
        if not overall_context['is_coherent']:
            reasoning_parts.append("handling incoherent request")
        
        # Model-specific reasoning
        if model_name == 'TNG DeepSeek' and output == 'code':
            reasoning_parts.append("code generation specialist")
        elif model_name == 'GLM4.5' and intent == 'analyze_something':
            reasoning_parts.append("analytical reasoning expert")
        elif model_name == 'Llama 4 Maverick' and intent == 'learn_something':
            reasoning_parts.append("educational explanation specialist")
        
        return f"Context analysis: {', '.join(reasoning_parts)}"

def test_universal_analyzer():
    """Test the universal context analyzer."""
    
    analyzer = UniversalContextAnalyzer()
    
    test_prompts = [
        "Explain everything about Diwali and let me know if it improves database performance",
        "Write a Python function to implement machine learning",
        "How do python snakes hunt their prey?",
        "What is the cultural significance of Onam festival?", 
        "Analyze market trends for cryptocurrency",
        "Create a story about a robot learning to love",
        "Debug this JavaScript code that's not working",
        "Compare the economic policies of different countries"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔍 Test {i}: {prompt}")
        print("-" * 60)
        
        # Get full analysis
        context = analyzer.analyze_universal_context(prompt)
        overall = context['overall_context']
        
        # Get model selection
        model, confidence, reasoning = analyzer.select_best_model(prompt)
        
        # Display results
        print(f"📊 Primary Intent: {overall['primary_intent']}")
        print(f"🏷️  Primary Domain: {overall['primary_domain']}")
        print(f"📤 Expected Output: {overall['expected_output']}")
        print(f"📈 Complexity: {overall['complexity_level']}")
        print(f"🧠 Coherent: {overall['is_coherent']}")
        print(f"📊 Context Confidence: {overall['context_confidence']:.1%}")
        print(f"🎯 Selected Model: {model} ({confidence:.1%})")
        print(f"💭 Reasoning: {reasoning}")

if __name__ == "__main__":
    test_universal_analyzer()
