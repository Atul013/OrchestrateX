#!/usr/bin/env python3
"""
Ultra-Fine-Tuned Universal Context Analyzer v2.0
Advanced semantic understanding with enhanced precision
"""

import re
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter

class UltraContextAnalyzer:
    """
    Ultra-fine-tuned context analyzer with advanced semantic reasoning
    Enhanced intent detection, domain classification, and coherence analysis
    """
    
    def __init__(self):
        print("🧠 Initializing Ultra-Fine-Tuned Context Analyzer v2.0...")
        
        # Enhanced model profiles with detailed capabilities
        self.models = {
            'TNG DeepSeek': {
                'strengths': ['code_creation', 'technical_implementation', 'structured_building', 'debugging', 'system_design'],
                'confidence_base': 0.92,
                'specialty_domains': ['technical', 'analytical'],
                'output_preferences': ['code', 'technical_solution', 'structured_content']
            },
            'GLM4.5': {
                'strengths': ['complex_analysis', 'reasoning', 'comparison', 'evaluation', 'research', 'critical_thinking'],
                'confidence_base': 0.88,
                'specialty_domains': ['analytical', 'scientific', 'business'],
                'output_preferences': ['analysis', 'detailed_explanation', 'research_summary']
            },
            'GPT-OSS': {
                'strengths': ['general_knowledge', 'explanation', 'creative_writing', 'broad_topics', 'conversational'],
                'confidence_base': 0.78,
                'specialty_domains': ['general', 'cultural', 'educational'],
                'output_preferences': ['explanation', 'general_response', 'creative_content']
            },
            'Llama 4 Maverick': {
                'strengths': ['teaching', 'step_by_step', 'educational', 'simplification', 'tutoring', 'guidance'],
                'confidence_base': 0.83,
                'specialty_domains': ['educational', 'cultural', 'biological'],
                'output_preferences': ['explanation', 'tutorial', 'educational_content']
            },
            'Qwen3': {
                'strengths': ['logical_reasoning', 'problem_solving', 'precise_thinking', 'mathematical', 'systematic'],
                'confidence_base': 0.85,
                'specialty_domains': ['analytical', 'scientific', 'technical'],
                'output_preferences': ['solution', 'logical_explanation', 'systematic_analysis']
            },
            'MoonshotAI Kimi': {
                'strengths': ['personal_help', 'conversational', 'practical_advice', 'user_friendly', 'supportive'],
                'confidence_base': 0.75,
                'specialty_domains': ['general', 'personal', 'practical'],
                'output_preferences': ['practical_advice', 'friendly_response', 'helpful_guidance']
            }
        }
        
        # Enhanced intent patterns with confidence weighting
        self.intent_patterns = {
            'create_something': {
                'strong_indicators': ['create', 'make', 'build', 'develop', 'implement', 'design', 'generate', 'write', 'code', 'program'],
                'context_boosters': ['new', 'fresh', 'from scratch', 'custom', 'original'],
                'confidence_multiplier': 1.2
            },
            'learn_something': {
                'strong_indicators': ['explain', 'tell me', 'what is', 'how does', 'why does', 'learn about', 'understand'],
                'context_boosters': ['meaning', 'definition', 'concept', 'principle', 'fundamentals'],
                'confidence_multiplier': 1.1
            },
            'analyze_something': {
                'strong_indicators': ['analyze', 'examine', 'evaluate', 'assess', 'review', 'study', 'compare', 'contrast'],
                'context_boosters': ['pros and cons', 'advantages', 'disadvantages', 'trade-offs', 'comparison'],
                'confidence_multiplier': 1.3
            },
            'solve_problem': {
                'strong_indicators': ['solve', 'fix', 'debug', 'troubleshoot', 'resolve', 'help with'],
                'context_boosters': ['problem', 'issue', 'error', 'bug', 'challenge', 'difficulty'],
                'confidence_multiplier': 1.2
            },
            'get_help': {
                'strong_indicators': ['how to', 'can you', 'could you', 'would you', 'please help'],
                'context_boosters': ['guidance', 'assistance', 'support', 'advice'],
                'confidence_multiplier': 1.0
            }
        }
        
        # Enhanced domain detection with semantic relationships
        self.domain_semantics = {
            'technical': {
                'core_terms': ['python', 'javascript', 'java', 'code', 'programming', 'software', 'API', 'database'],
                'context_terms': ['function', 'algorithm', 'data structure', 'framework', 'library', 'development'],
                'exclusion_patterns': ['snake', 'animal', 'biology', 'nature']  # For disambiguation
            },
            'biological': {
                'core_terms': ['animal', 'snake', 'hunt', 'prey', 'species', 'behavior', 'wildlife', 'nature'],
                'context_terms': ['ecosystem', 'habitat', 'evolution', 'genetics', 'biology', 'zoology'],
                'exclusion_patterns': ['code', 'programming', 'software']
            },
            'cultural': {
                'core_terms': ['festival', 'tradition', 'culture', 'celebration', 'heritage', 'custom'],
                'context_terms': ['community', 'society', 'beliefs', 'practices', 'rituals', 'history'],
                'exclusion_patterns': []
            }
        }
    
    def analyze_ultra_context(self, prompt: str) -> Dict[str, Any]:
        """Ultra-fine-tuned context analysis with enhanced precision."""
        
        # Multi-layered semantic analysis
        semantic_profile = self._extract_enhanced_semantic_profile(prompt)
        
        # Advanced intent understanding with confidence scoring
        intent_analysis = self._understand_enhanced_intent(prompt)
        
        # Smart domain reasoning with disambiguation
        domain_reasoning = self._reason_enhanced_domains(prompt)
        
        # Sophisticated task complexity assessment
        task_complexity = self._assess_enhanced_complexity(prompt)
        
        # Advanced output expectation analysis
        output_analysis = self._analyze_enhanced_output(prompt)
        
        # Ultra-smart coherence and absurdity detection
        coherence_check = self._check_enhanced_coherence(prompt)
        
        # Contextual relationship mapping
        relationship_analysis = self._analyze_contextual_relationships(prompt)
        
        return {
            'semantic_profile': semantic_profile,
            'intent_analysis': intent_analysis,
            'domain_reasoning': domain_reasoning,
            'task_complexity': task_complexity,
            'output_analysis': output_analysis,
            'coherence_check': coherence_check,
            'relationship_analysis': relationship_analysis,
            'overall_context': self._synthesize_enhanced_context(prompt, {
                'semantic': semantic_profile,
                'intent': intent_analysis,
                'domain': domain_reasoning,
                'complexity': task_complexity,
                'output': output_analysis,
                'coherence': coherence_check,
                'relationships': relationship_analysis
            })
        }
    
    def _extract_enhanced_semantic_profile(self, prompt: str) -> Dict[str, Any]:
        """Enhanced semantic profiling with weighted scoring."""
        
        # Linguistic structure analysis
        structure = self._analyze_linguistic_structure(prompt)
        
        # Semantic intent scoring with pattern matching
        intent_scores = {}
        for intent_type, patterns in self.intent_patterns.items():
            score = self._calculate_intent_score(prompt, patterns)
            intent_scores[intent_type] = score
        
        # Semantic density and complexity
        semantic_density = self._calculate_semantic_density(prompt)
        
        # Specificity and abstraction levels
        specificity_analysis = self._analyze_specificity_levels(prompt)
        
        return {
            'linguistic_structure': structure,
            'intent_scores': intent_scores,
            'semantic_density': semantic_density,
            'specificity_analysis': specificity_analysis,
            'dominant_intent': max(intent_scores.items(), key=lambda x: x[1])[0] if intent_scores else 'general_request'
        }
    
    def _calculate_intent_score(self, prompt: str, patterns: Dict) -> float:
        """Calculate weighted intent score based on patterns."""
        score = 0.0
        prompt_lower = prompt.lower()
        
        # Strong indicators
        for indicator in patterns['strong_indicators']:
            if indicator in prompt_lower:
                score += 1.0
        
        # Context boosters
        for booster in patterns['context_boosters']:
            if booster in prompt_lower:
                score += 0.5
        
        # Apply confidence multiplier
        score *= patterns['confidence_multiplier']
        
        return score
    
    def _analyze_linguistic_structure(self, prompt: str) -> Dict[str, Any]:
        """Analyze the linguistic structure of the prompt."""
        
        words = prompt.split()
        sentences = prompt.split('.')
        
        # Sentence structure analysis
        sentence_types = {
            'declarative': len([s for s in sentences if not s.strip().endswith('?') and s.strip()]),
            'interrogative': len([s for s in sentences if s.strip().endswith('?')]),
            'imperative': self._count_imperative_sentences(prompt)
        }
        
        # Complexity indicators
        complexity_indicators = {
            'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
            'sentence_count': len([s for s in sentences if s.strip()]),
            'clause_complexity': self._measure_clause_complexity(prompt),
            'technical_density': self._measure_technical_density(prompt)
        }
        
        return {
            'word_count': len(words),
            'sentence_types': sentence_types,
            'complexity_indicators': complexity_indicators
        }
    
    def _calculate_semantic_density(self, prompt: str) -> Dict[str, float]:
        """Calculate the semantic density of different concept types."""
        
        densities = {
            'action_density': len(re.findall(r'\b(create|make|build|analyze|solve|implement)\b', prompt.lower())) / len(prompt.split()),
            'knowledge_density': len(re.findall(r'\b(what|how|why|explain|tell|describe)\b', prompt.lower())) / len(prompt.split()),
            'technical_density': len(re.findall(r'\b(code|API|database|algorithm|function|system)\b', prompt.lower())) / len(prompt.split()),
            'domain_density': len(re.findall(r'\b(cultural|scientific|business|educational)\b', prompt.lower())) / len(prompt.split())
        }
        
        return densities
    
    def _analyze_specificity_levels(self, prompt: str) -> Dict[str, float]:
        """Analyze different levels of specificity in the prompt."""
        
        # Technical specificity
        technical_terms = len(re.findall(r'\b[A-Z][a-z]*[A-Z][a-z]*\b', prompt))  # CamelCase
        version_numbers = len(re.findall(r'\b\d+\.\d+\b', prompt))
        specific_technologies = len(re.findall(r'\b(React|Angular|Vue|Django|Flask|MongoDB|PostgreSQL)\b', prompt))
        
        # Domain specificity
        domain_specific_terms = len(re.findall(r'\b(quantum|neural|blockchain|microservices|containerization)\b', prompt.lower()))
        
        # Temporal specificity
        time_references = len(re.findall(r'\b(today|tomorrow|next week|2024|recent|current)\b', prompt.lower()))
        
        return {
            'technical_specificity': (technical_terms + version_numbers + specific_technologies) / 3,
            'domain_specificity': domain_specific_terms,
            'temporal_specificity': time_references,
            'overall_specificity': np.mean([technical_terms, domain_specific_terms, time_references])
        }
    
    def _understand_enhanced_intent(self, prompt: str) -> Dict[str, Any]:
        """Enhanced intent understanding with confidence weighting."""
        
        semantic_profile = self._extract_enhanced_semantic_profile(prompt)
        intent_scores = semantic_profile['intent_scores']
        
        # Calculate intent confidence
        total_score = sum(intent_scores.values())
        intent_confidence = {}
        
        if total_score > 0:
            for intent, score in intent_scores.items():
                intent_confidence[intent] = score / total_score
        
        # Determine primary and secondary intents
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        primary_intent = sorted_intents[0][0] if sorted_intents else 'general_request'
        secondary_intent = sorted_intents[1][0] if len(sorted_intents) > 1 and sorted_intents[1][1] > 0 else None
        
        return {
            'primary_intent': primary_intent,
            'secondary_intent': secondary_intent,
            'intent_scores': intent_scores,
            'intent_confidence': intent_confidence,
            'intent_clarity': max(intent_confidence.values()) if intent_confidence else 0.5
        }
    
    def _reason_enhanced_domains(self, prompt: str) -> Dict[str, Any]:
        """Enhanced domain reasoning with smart disambiguation."""
        
        domain_scores = {}
        domain_evidence = {}
        
        # Technical domain with disambiguation
        tech_score, tech_evidence = self._analyze_technical_domain(prompt)
        domain_scores['technical'] = tech_score
        domain_evidence['technical'] = tech_evidence
        
        # Biological domain
        bio_score, bio_evidence = self._analyze_biological_domain(prompt)
        domain_scores['biological'] = bio_score
        domain_evidence['biological'] = bio_evidence
        
        # Cultural domain
        cultural_score, cultural_evidence = self._analyze_cultural_domain(prompt)
        domain_scores['cultural'] = cultural_score
        domain_evidence['cultural'] = cultural_evidence
        
        # Scientific domain
        scientific_score, scientific_evidence = self._analyze_scientific_domain(prompt)
        domain_scores['scientific'] = scientific_score
        domain_evidence['scientific'] = scientific_evidence
        
        # Business domain
        business_score, business_evidence = self._analyze_business_domain(prompt)
        domain_scores['business'] = business_score
        domain_evidence['business'] = business_evidence
        
        # Educational domain
        educational_score, educational_evidence = self._analyze_educational_domain(prompt)
        domain_scores['educational'] = educational_score
        domain_evidence['educational'] = educational_evidence
        
        # Creative domain
        creative_score, creative_evidence = self._analyze_creative_domain(prompt)
        domain_scores['creative'] = creative_score
        domain_evidence['creative'] = creative_evidence
        
        # Filter and rank domains
        active_domains = {k: v for k, v in domain_scores.items() if v > 0.1}
        primary_domain = max(active_domains.items(), key=lambda x: x[1])[0] if active_domains else 'general'
        
        return {
            'primary_domain': primary_domain,
            'domain_scores': domain_scores,
            'domain_evidence': domain_evidence,
            'active_domains': list(active_domains.keys()),
            'domain_confidence': active_domains[primary_domain] / sum(active_domains.values()) if active_domains else 0.5
        }
    
    def _analyze_technical_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze technical domain with smart disambiguation."""
        score = 0.0
        evidence = []
        
        # Python disambiguation
        if 'python' in prompt.lower():
            programming_context = any(term in prompt.lower() for term in 
                ['function', 'code', 'script', 'programming', 'implement', 'develop', 'write', 'create', 'build'])
            biological_context = any(term in prompt.lower() for term in 
                ['snake', 'animal', 'hunt', 'prey', 'species', 'behavior', 'wildlife'])
            
            if programming_context and not biological_context:
                score += 0.8
                evidence.append("Python programming language (contextually confirmed)")
            elif biological_context and not programming_context:
                score += 0.0  # Not technical
            else:
                score += 0.3  # Ambiguous context
                evidence.append("Python mentioned but context unclear")
        
        # Other technical terms
        tech_terms = re.findall(r'\b(javascript|java|html|css|sql|api|database|server|algorithm|function|class|method|code|programming)\b', prompt.lower())
        if tech_terms:
            score += len(set(tech_terms)) * 0.3
            evidence.append(f"Technical terms: {', '.join(set(tech_terms))}")
        
        # Implementation patterns
        if re.search(r'\b(implement|develop|build|create|write)\b.*\b(function|application|system|software)\b', prompt.lower()):
            score += 0.5
            evidence.append("Implementation request with technical context")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _analyze_biological_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze biological domain."""
        score = 0.0
        evidence = []
        
        # Biological terms
        bio_terms = re.findall(r'\b(animal|animals|snake|snakes|hunt|prey|predator|species|behavior|behaviour|wildlife|nature|biology|reptile|mammal|ecosystem)\b', prompt.lower())
        if bio_terms:
            score += len(set(bio_terms)) * 0.4
            evidence.append(f"Biological terms: {', '.join(set(bio_terms))}")
        
        # Animal behavior patterns
        if re.search(r'\b(how do|how does).*\b(hunt|eat|live|behave|survive|reproduce)\b', prompt.lower()):
            score += 0.6
            evidence.append("Animal behavior inquiry")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _analyze_cultural_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze cultural domain."""
        score = 0.0
        evidence = []
        
        # Cultural terms
        cultural_terms = re.findall(r'\b(culture|tradition|festival|celebration|heritage|custom|ceremony|ritual)\b', prompt.lower())
        if cultural_terms:
            score += len(set(cultural_terms)) * 0.5
            evidence.append(f"Cultural terms: {', '.join(set(cultural_terms))}")
        
        # Specific festivals/events
        festivals = re.findall(r'\b(diwali|christmas|ramadan|eid|onam|pongal|holi|easter)\b', prompt.lower())
        if festivals:
            score += len(set(festivals)) * 0.6
            evidence.append(f"Cultural events: {', '.join(set(festivals))}")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _analyze_scientific_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze scientific domain."""
        score = 0.0
        evidence = []
        
        scientific_terms = re.findall(r'\b(quantum|physics|chemistry|research|experiment|hypothesis|theory|scientific|study)\b', prompt.lower())
        if scientific_terms:
            score += len(set(scientific_terms)) * 0.5
            evidence.append(f"Scientific terms: {', '.join(set(scientific_terms))}")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _analyze_business_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze business domain."""
        score = 0.0
        evidence = []
        
        business_terms = re.findall(r'\b(business|company|market|strategy|profit|revenue|investment|economic|financial|corporate)\b', prompt.lower())
        if business_terms:
            score += len(set(business_terms)) * 0.4
            evidence.append(f"Business terms: {', '.join(set(business_terms))}")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _analyze_educational_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze educational domain."""
        score = 0.0
        evidence = []
        
        # Learning language
        learning_terms = re.findall(r'\b(explain|teach|learn|understand|know|study|educate|tutorial)\b', prompt.lower())
        if learning_terms:
            score += len(set(learning_terms)) * 0.3
            evidence.append(f"Learning language: {', '.join(set(learning_terms))}")
        
        # Question format
        if prompt.strip().endswith('?'):
            score += 0.3
            evidence.append("Question format")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _analyze_creative_domain(self, prompt: str) -> Tuple[float, Dict]:
        """Analyze creative domain."""
        score = 0.0
        evidence = []
        
        creative_terms = re.findall(r'\b(story|creative|design|art|artistic|beautiful|innovative|original|imaginative|write|compose)\b', prompt.lower())
        if creative_terms:
            score += len(set(creative_terms)) * 0.4
            evidence.append(f"Creative language: {', '.join(set(creative_terms))}")
        
        return score, {'score': score, 'evidence': evidence}
    
    def _check_enhanced_coherence(self, prompt: str) -> Dict[str, Any]:
        """Enhanced coherence checking with detailed absurdity detection."""
        
        domain_analysis = self._reason_enhanced_domains(prompt)
        active_domains = domain_analysis['active_domains']
        
        coherence_issues = []
        absurdity_score = 0.0
        coherence_score = 1.0
        
        # Temporal impossibilities (anachronisms)
        temporal_issues = self._detect_temporal_impossibilities(prompt)
        if temporal_issues:
            coherence_issues.extend(temporal_issues)
            absurdity_score += 0.8  # High absurdity for anachronisms
            coherence_score -= 0.8
        
        # Cultural + Technical impossibilities
        if 'cultural' in active_domains and 'technical' in active_domains:
            if re.search(r'\b(festival|celebration|tradition|diwali|christmas|ramadan)\b.*\b(improve|enhance|optimize|boost|affect|influence)\b.*\b(database|performance|server|algorithm|api|sorting)\b', prompt.lower()):
                coherence_issues.append("Impossible causal relationship: cultural events cannot affect technical systems")
                absurdity_score += 0.7
                coherence_score -= 0.7
        
        # Scientific + Political impossibilities  
        if 'scientific' in active_domains:
            if re.search(r'\b(quantum|physics|chemistry|entanglement)\b.*\b(affect|influence|impact)\b.*\b(election|political|parliament|government|voting)\b', prompt.lower()):
                coherence_issues.append("Impossible scientific influence on political processes")
                absurdity_score += 0.8
                coherence_score -= 0.8
        
        # Biological + Technical mixing
        if 'biological' in active_domains and 'technical' in active_domains:
            if not any(term in prompt.lower() for term in ['bio', 'bioinformatics', 'computational', 'simulation']):
                coherence_issues.append("Unusual mixing of biological and technical domains")
                absurdity_score += 0.3
                coherence_score -= 0.3
        
        # Economic + Literary impossibilities
        if re.search(r'\b(GDP|economic|financial|market)\b.*\b(predict|forecast)\b.*\b(shakespeare|sonnet|literature|poetry)\b', prompt.lower()):
            coherence_issues.append("Impossible prediction of economics using literature")
            absurdity_score += 0.7
            coherence_score -= 0.7
        
        # Weather + Programming impossibilities
        if re.search(r'\b(weather|rain|snow|storm|hurricane)\b.*\b(affect|influence|impact|improve)\b.*\b(code|programming|algorithm|function|performance)\b', prompt.lower()):
            coherence_issues.append("Weather cannot directly affect code performance")
            absurdity_score += 0.6
            coherence_score -= 0.6
        
        # Food + Technology impossibilities
        if re.search(r'\b(pizza|burger|chocolate|coffee|food)\b.*\b(optimize|improve|enhance)\b.*\b(database|server|network|api)\b', prompt.lower()):
            coherence_issues.append("Food cannot optimize technical systems")
            absurdity_score += 0.6
            coherence_score -= 0.6
        
        # Color + Performance impossibilities
        if re.search(r'\b(red|blue|green|yellow|purple|color)\b.*\b(increase|boost|improve)\b.*\b(speed|performance|efficiency|processing)\b', prompt.lower()):
            coherence_issues.append("Colors cannot improve system performance")
            absurdity_score += 0.6
            coherence_score -= 0.6
        
        # Music + Mathematical impossibilities
        if re.search(r'\b(music|song|melody|rhythm)\b.*\b(solve|calculate|compute)\b.*\b(equation|mathematics|algebra|calculus)\b', prompt.lower()):
            coherence_issues.append("Music cannot solve mathematical equations")
            absurdity_score += 0.6
            coherence_score -= 0.6
        
        # Sports + Academic impossibilities
        if re.search(r'\b(football|basketball|soccer|tennis|sports)\b.*\b(improve|enhance|boost)\b.*\b(grades|academic|study|learning)\b', prompt.lower()):
            coherence_issues.append("Sports cannot directly improve academic performance")
            absurdity_score += 0.4
            coherence_score -= 0.4
        
        # Astrology + Science impossibilities
        if re.search(r'\b(horoscope|astrology|zodiac|stars)\b.*\b(predict|forecast|determine)\b.*\b(physics|chemistry|biology|science)\b', prompt.lower()):
            coherence_issues.append("Astrology cannot predict scientific phenomena")
            absurdity_score += 0.7
            coherence_score -= 0.7
        
        # Multiple unrelated concepts
        if len(active_domains) > 3:
            coherence_issues.append("Too many unrelated domains in single request")
            absurdity_score += 0.4
            coherence_score -= 0.4
        
        return {
            'score': max(0.1, coherence_score),
            'absurdity_score': min(1.0, absurdity_score),
            'issues': coherence_issues,
            'is_coherent': len(coherence_issues) == 0,
            'absurdity_level': 'high' if absurdity_score > 0.6 else 'medium' if absurdity_score > 0.3 else 'low'
        }
    
    def _detect_temporal_impossibilities(self, prompt: str) -> List[str]:
        """Detect anachronisms and temporal impossibilities."""
        issues = []
        prompt_lower = prompt.lower()
        
        # Modern tech terms (expanded)
        modern_tech = ['html', 'css', 'javascript', 'wifi', 'internet', 'computer', 'smartphone', 'api', 'database', 'server', 
                      'blockchain', 'ai', 'machine learning', 'neural network', 'cloud computing', 'social media', 'email', 
                      'bluetooth', '5g', '4g', 'gps', 'satellite', 'laser', 'nuclear', 'electricity', 'television', 'radio']
        
        # Historical periods (expanded)
        historical_periods = ['medieval', 'ancient', 'renaissance', 'victorian', 'classical', 'prehistoric', 'stone age',
                             'bronze age', 'iron age', 'roman', 'greek', 'egyptian', 'babylonian', 'paleolithic', 
                             'neolithic', 'dark ages', 'middle ages', 'byzantine', 'feudal']
        
        found_modern = [tech for tech in modern_tech if tech in prompt_lower]
        found_historical = [period for period in historical_periods if period in prompt_lower]
        
        if found_modern and found_historical:
            issues.append(f"Temporal impossibility: {', '.join(found_modern)} did not exist during {', '.join(found_historical)} times")
        
        # Specific impossible combinations (expanded)
        impossible_combinations = [
            (r'\bhtml\b.*\bmedieval\b', "HTML did not exist in medieval times (HTML: 1990s, Medieval: 500-1500 AD)"),
            (r'\bwifi\b.*\bancient\b', "WiFi did not exist in ancient times"),
            (r'\bsmartphone\b.*\bvictorian\b', "Smartphones did not exist in Victorian era"),
            (r'\binternet\b.*\b(ancient|medieval|renaissance)\b', "Internet did not exist in pre-modern times"),
            (r'\b(css|javascript)\b.*\b(medieval|ancient)\b', "Web technologies did not exist in historical periods"),
            (r'\bblockchain\b.*\b(ancient|medieval|renaissance|victorian)\b', "Blockchain technology is from 2008+"),
            (r'\bai\b.*\b(ancient|medieval|stone age)\b', "Artificial Intelligence is a modern concept"),
            (r'\bsocial media\b.*\b(ancient|medieval|victorian)\b', "Social media is a 21st century phenomenon"),
            (r'\bemail\b.*\b(ancient|medieval|renaissance)\b', "Email was invented in the 1970s"),
            (r'\belectricity\b.*\b(ancient|medieval|stone age)\b', "Electricity was not understood/harnessed in ancient times"),
            (r'\bnuclear\b.*\b(ancient|medieval|renaissance)\b', "Nuclear technology is 20th century")
        ]
        
        for pattern, message in impossible_combinations:
            if re.search(pattern, prompt_lower):
                issues.append(message)
        
        return issues
    
    def _analyze_contextual_relationships(self, prompt: str) -> Dict[str, Any]:
        """Analyze relationships between different concepts in the prompt."""
        
        # Extract entities and concepts
        entities = self._extract_entities(prompt)
        concepts = self._extract_concepts(prompt)
        
        # Analyze relationships
        relationships = self._map_entity_relationships(prompt, entities, concepts)
        
        # Determine relationship coherence
        relationship_coherence = self._assess_relationship_coherence(relationships)
        
        return {
            'entities': entities,
            'concepts': concepts,
            'relationships': relationships,
            'relationship_coherence': relationship_coherence
        }
    
    def _extract_entities(self, prompt: str) -> List[str]:
        """Extract named entities from the prompt."""
        # Simple entity extraction - could be enhanced with NLP libraries
        entities = []
        
        # Proper nouns (potential entities)
        proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', prompt)
        entities.extend(proper_nouns)
        
        # Technical entities
        tech_entities = re.findall(r'\b(Python|JavaScript|Java|SQL|API|REST|HTTP)\b', prompt)
        entities.extend(tech_entities)
        
        return list(set(entities))
    
    def _extract_concepts(self, prompt: str) -> List[str]:
        """Extract conceptual terms from the prompt."""
        concepts = []
        
        # Abstract concepts
        abstract_concepts = re.findall(r'\b(performance|optimization|efficiency|algorithm|analysis|theory|concept)\b', prompt.lower())
        concepts.extend(abstract_concepts)
        
        return list(set(concepts))
    
    def _map_entity_relationships(self, prompt: str, entities: List[str], concepts: List[str]) -> List[Dict]:
        """Map relationships between entities and concepts."""
        relationships = []
        
        # Look for relationship indicators
        if re.search(r'\b(affect|influence|impact|improve|enhance|relate|connect)\b', prompt.lower()):
            # Extract what affects what
            for entity in entities:
                for concept in concepts:
                    if entity.lower() in prompt.lower() and concept in prompt.lower():
                        relationships.append({
                            'entity': entity,
                            'concept': concept,
                            'relationship': 'influences',
                            'context': prompt
                        })
        
        return relationships
    
    def _assess_relationship_coherence(self, relationships: List[Dict]) -> Dict[str, Any]:
        """Assess the coherence of entity-concept relationships."""
        coherent_relationships = 0
        incoherent_relationships = 0
        
        for rel in relationships:
            entity = rel['entity'].lower()
            concept = rel['concept'].lower()
            
            # Check for known incoherent relationships
            if any(cultural in entity for cultural in ['diwali', 'christmas', 'ramadan']) and \
               any(tech in concept for tech in ['performance', 'algorithm', 'optimization']):
                incoherent_relationships += 1
            else:
                coherent_relationships += 1
        
        total_relationships = len(relationships)
        coherence_ratio = coherent_relationships / total_relationships if total_relationships > 0 else 1.0
        
        return {
            'total_relationships': total_relationships,
            'coherent_count': coherent_relationships,
            'incoherent_count': incoherent_relationships,
            'coherence_ratio': coherence_ratio
        }
    
    def _assess_enhanced_complexity(self, prompt: str) -> Dict[str, Any]:
        """Enhanced complexity assessment with multiple factors."""
        
        # Linguistic complexity
        word_count = len(prompt.split())
        sentence_count = len([s for s in prompt.split('.') if s.strip()])
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else word_count
        
        # Conceptual complexity
        unique_domains = len(self._reason_enhanced_domains(prompt)['active_domains'])
        technical_terms = len(re.findall(r'\b[A-Z][a-z]*[A-Z][a-z]*\b', prompt))
        
        # Structural complexity
        conjunctions = len(re.findall(r'\b(and|but|however|moreover|furthermore|additionally)\b', prompt.lower()))
        clauses = len(re.findall(r'[,;]', prompt))
        
        # Calculate overall complexity
        complexity_factors = {
            'linguistic': min(word_count / 20, 3.0),  # Normalize to 0-3 scale
            'conceptual': min(unique_domains + (technical_terms * 0.5), 3.0),
            'structural': min((conjunctions + clauses) * 0.5, 3.0)
        }
        
        overall_complexity = np.mean(list(complexity_factors.values()))
        
        if overall_complexity < 0.8:
            level = 'simple'
        elif overall_complexity < 1.5:
            level = 'moderate'
        elif overall_complexity < 2.5:
            level = 'complex'
        else:
            level = 'very_complex'
        
        return {
            'level': level,
            'score': overall_complexity,
            'factors': complexity_factors,
            'details': {
                'word_count': word_count,
                'unique_domains': unique_domains,
                'technical_terms': technical_terms,
                'structural_elements': conjunctions + clauses
            }
        }
    
    def _analyze_enhanced_output(self, prompt: str) -> Dict[str, Any]:
        """Enhanced output expectation analysis."""
        
        intent_analysis = self._understand_enhanced_intent(prompt)
        domain_analysis = self._reason_enhanced_domains(prompt)
        
        primary_intent = intent_analysis['primary_intent']
        primary_domain = domain_analysis['primary_domain']
        
        # Determine expected output type with higher precision
        output_mapping = {
            ('create_something', 'technical'): 'code',
            ('create_something', 'creative'): 'creative_content',
            ('create_something', 'business'): 'business_document',
            ('learn_something', 'any'): 'explanation',
            ('analyze_something', 'any'): 'analysis',
            ('solve_problem', 'technical'): 'technical_solution',
            ('solve_problem', 'any'): 'solution',
            ('get_help', 'any'): 'guidance'
        }
        
        # Find matching output type
        output_type = 'general_response'
        for (intent, domain), output in output_mapping.items():
            if (intent == primary_intent and (domain == primary_domain or domain == 'any')):
                output_type = output
                break
        
        # Calculate output confidence
        output_confidence = intent_analysis['intent_clarity'] * domain_analysis['domain_confidence']
        
        return {
            'type': output_type,
            'confidence': output_confidence,
            'specificity': self._calculate_output_specificity(prompt, output_type)
        }
    
    def _calculate_output_specificity(self, prompt: str, output_type: str) -> float:
        """Calculate how specific the expected output should be."""
        specificity = 0.5  # Default
        
        # Look for specificity indicators
        if 'detailed' in prompt.lower():
            specificity += 0.2
        if 'step by step' in prompt.lower():
            specificity += 0.3
        if 'comprehensive' in prompt.lower():
            specificity += 0.2
        if 'brief' in prompt.lower() or 'summary' in prompt.lower():
            specificity -= 0.2
        
        return min(1.0, max(0.1, specificity))
    
    def _synthesize_enhanced_context(self, prompt: str, analysis: Dict) -> Dict[str, Any]:
        """Synthesize all analysis into enhanced context understanding."""
        
        intent = analysis['intent']['primary_intent']
        domain = analysis['domain']['primary_domain']
        output = analysis['output']['type']
        complexity = analysis['complexity']['level']
        coherence = analysis['coherence']['is_coherent']
        absurdity = analysis['coherence']['absurdity_score']
        
        # Enhanced context confidence calculation
        context_confidence = (
            analysis['intent']['intent_clarity'] * 0.25 +
            analysis['domain']['domain_confidence'] * 0.25 +
            analysis['output']['confidence'] * 0.2 +
            analysis['coherence']['score'] * 0.2 +
            analysis['relationships']['relationship_coherence']['coherence_ratio'] * 0.1
        )
        
        # Context quality assessment
        quality_factors = {
            'clarity': analysis['intent']['intent_clarity'],
            'domain_certainty': analysis['domain']['domain_confidence'],
            'coherence': analysis['coherence']['score'],
            'complexity_appropriateness': 1.0 - (absurdity * 0.5)
        }
        
        context_quality = np.mean(list(quality_factors.values()))
        
        return {
            'primary_intent': intent,
            'primary_domain': domain,
            'expected_output': output,
            'complexity_level': complexity,
            'is_coherent': coherence,
            'absurdity_score': absurdity,
            'context_confidence': context_confidence,
            'context_quality': context_quality,
            'quality_factors': quality_factors,
            'context_summary': f"{intent.replace('_', ' ')} in {domain} domain, expecting {output.replace('_', ' ')} ({complexity} complexity)"
        }
    
    def select_ultra_model(self, prompt: str) -> Tuple[str, float, str]:
        """Ultra-fine-tuned model selection with enhanced precision."""
        
        # Get comprehensive context analysis
        context = self.analyze_ultra_context(prompt)
        overall = context['overall_context']
        
        # Calculate model fitness scores
        model_scores = {}
        model_reasons = {}
        
        for model_name, model_info in self.models.items():
            score, reasoning = self._calculate_enhanced_model_fit(overall, model_info, context)
            model_scores[model_name] = score
            model_reasons[model_name] = reasoning
        
        # Select best model
        best_model = max(model_scores.items(), key=lambda x: x[1])
        model_name = best_model[0]
        confidence = min(best_model[1], 0.99)
        
        # Generate comprehensive reasoning
        reasoning = self._generate_enhanced_reasoning(overall, model_name, context, model_reasons[model_name])
        
        return model_name, confidence, reasoning
    
    def _calculate_enhanced_model_fit(self, overall_context: Dict, model_info: Dict, full_context: Dict) -> Tuple[float, List[str]]:
        """Calculate enhanced model fitness with detailed reasoning."""
        
        base_score = model_info['confidence_base']
        reasoning_points = []
        
        # Intent matching with weighted scoring
        intent = overall_context['primary_intent']
        for strength in model_info['strengths']:
            if self._intent_matches_strength(intent, strength):
                boost = 0.15
                base_score += boost
                reasoning_points.append(f"{strength.replace('_', ' ')} specialist (+{boost:.2f})")
        
        # Domain specialty matching
        domain = overall_context['primary_domain']
        if domain in model_info['specialty_domains']:
            boost = 0.12
            base_score += boost
            reasoning_points.append(f"{domain} domain specialist (+{boost:.2f})")
        
        # Output type preference matching
        output_type = overall_context['expected_output']
        if output_type in model_info['output_preferences']:
            boost = 0.1
            base_score += boost
            reasoning_points.append(f"{output_type.replace('_', ' ')} preference (+{boost:.2f})")
        
        # Complexity handling
        complexity = overall_context['complexity_level']
        if complexity in ['complex', 'very_complex'] and 'complex_analysis' in model_info['strengths']:
            boost = 0.08
            base_score += boost
            reasoning_points.append(f"complex analysis capability (+{boost:.2f})")
        
        # Coherence penalty
        if not overall_context['is_coherent']:
            penalty = 0.2 + (overall_context['absurdity_score'] * 0.1)
            base_score -= penalty
            reasoning_points.append(f"incoherent request penalty (-{penalty:.2f})")
        
        # Context quality multiplier
        quality_multiplier = overall_context['context_quality']
        base_score *= quality_multiplier
        if quality_multiplier != 1.0:
            reasoning_points.append(f"context quality factor (×{quality_multiplier:.2f})")
        
        return max(0.1, min(base_score, 1.0)), reasoning_points
    
    def _intent_matches_strength(self, intent: str, strength: str) -> bool:
        """Check if intent matches model strength."""
        intent_strength_map = {
            'create_something': ['code_creation', 'technical_implementation', 'structured_building', 'creative_writing'],
            'learn_something': ['teaching', 'explanation', 'general_knowledge', 'educational'],
            'analyze_something': ['complex_analysis', 'reasoning', 'critical_thinking', 'evaluation'],
            'solve_problem': ['problem_solving', 'debugging', 'technical_implementation'],
            'get_help': ['personal_help', 'conversational', 'practical_advice', 'supportive']
        }
        
        return strength in intent_strength_map.get(intent, [])
    
    def _generate_enhanced_reasoning(self, overall_context: Dict, model_name: str, full_context: Dict, reasoning_points: List[str]) -> str:
        """Generate comprehensive reasoning for model selection."""
        
        base_reason = f"Context: {overall_context['context_summary']}"
        
        if reasoning_points:
            detailed_reason = f"{base_reason}. Selection factors: {', '.join(reasoning_points[:3])}"
        else:
            detailed_reason = f"{base_reason}. Default selection based on general capabilities"
        
        # Add quality indicators
        quality = overall_context['context_quality']
        if quality > 0.8:
            detailed_reason += " (high quality context)"
        elif quality < 0.5:
            detailed_reason += " (low quality context)"
        
        return detailed_reason
    
    # Helper methods for linguistic analysis
    def _count_imperative_sentences(self, prompt: str) -> int:
        """Count imperative sentences in the prompt."""
        sentences = [s.strip() for s in prompt.split('.') if s.strip()]
        imperative_count = 0
        
        for sentence in sentences:
            words = sentence.split()
            if words and words[0].lower() in ['create', 'make', 'build', 'write', 'implement', 'design', 'develop']:
                imperative_count += 1
        
        return imperative_count
    
    def _measure_clause_complexity(self, prompt: str) -> float:
        """Measure the complexity of clauses in the prompt."""
        # Count subordinating conjunctions and relative pronouns
        complex_markers = len(re.findall(r'\b(because|since|although|while|whereas|if|unless|that|which|who|whom)\b', prompt.lower()))
        return complex_markers * 0.5
    
    def _measure_technical_density(self, prompt: str) -> float:
        """Measure the density of technical terminology."""
        words = prompt.split()
        if not words:
            return 0.0
        
        technical_terms = len(re.findall(r'\b(API|SQL|HTTP|JSON|XML|algorithm|database|server|framework|library)\b', prompt))
        return technical_terms / len(words)

def test_ultra_analyzer():
    """Test the ultra-fine-tuned analyzer."""
    
    analyzer = UltraContextAnalyzer()
    
    test_prompts = [
        "Create a Python machine learning algorithm for stock prediction",
        "How does quantum entanglement affect parliamentary elections?", 
        "Explain the cultural significance of Diwali and its impact on database performance",
        "Write a detailed story about AI consciousness",
        "Debug this complex JavaScript authentication system",
        "What hunting strategies do python snakes use in the wild?",
        "Analyze market trends for renewable energy investments",
        "How do I learn React.js step by step?"
    ]
    
    print("🚀 Ultra-Fine-Tuned Context Analyzer Test Results")
    print("=" * 70)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔍 Test {i}: {prompt}")
        print("-" * 65)
        
        try:
            # Get analysis
            context = analyzer.analyze_ultra_context(prompt)
            overall = context['overall_context']
            
            # Get model selection
            model, confidence, reasoning = analyzer.select_ultra_model(prompt)
            
            # Display results
            print(f"🎯 Intent: {overall['primary_intent'].replace('_', ' ').title()}")
            print(f"🏷️  Domain: {overall['primary_domain'].title()}")
            print(f"📤 Output: {overall['expected_output'].replace('_', ' ').title()}")
            print(f"📊 Complexity: {overall['complexity_level'].title()}")
            print(f"🧠 Coherent: {'✅' if overall['is_coherent'] else '❌'} (Absurdity: {overall['absurdity_score']:.1%})")
            print(f"⭐ Quality: {overall['context_quality']:.1%}")
            print(f"🎯 Model: {model} ({confidence:.1%})")
            print(f"💭 Reasoning: {reasoning}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ultra_analyzer()
