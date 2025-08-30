import re
from typing import Dict, List, Tuple

def extract_prompt_features(prompt: str) -> dict:
    """
    Advanced prompt analysis with precise context-aware classification.
    Uses multi-layered analysis including semantic patterns, contextual relationships,
    and sophisticated scoring mechanisms for AI model routing.
    
    Args:
        prompt (str): The user input prompt to analyze
        
    Returns:
        dict: Contains token_count, categories, topic_domain, intent_type, confidence, and debug info
    """
    
    # Preprocessing
    prompt_original = prompt
    prompt_lower = prompt.lower().strip()
    
    # Advanced tokenization (handle punctuation better)
    tokens = re.findall(r'\b\w+\b', prompt_lower)
    token_count = len(tokens)
    
    # Create n-grams for better context understanding
    bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)]
    trigrams = [f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}" for i in range(len(tokens)-2)]
    
    # Initialize scoring system
    category_scores = {'coding': 0.0, 'reasoning': 0.0, 'general': 0.0}
    domain_scores = {'technical': 0.0, 'logical': 0.0, 'casual': 0.0}
    intent_scores = {'question': 0.0, 'instruction': 0.0, 'code_request': 0.0, 'reasoning_task': 0.0}
    
    # =================== CATEGORY ANALYSIS ===================
    
    # 1. CODING CATEGORY - Multi-tier precision
    coding_patterns = {
        # Tier 1: Unambiguous coding terms (weight: 5.0)
        'tier1': {
            'words': ['algorithm', 'debugging', 'compilation', 'syntax', 'variable', 'iteration', 
                     'recursion', 'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
                     'constructor', 'destructor', 'middleware', 'backend', 'frontend', 'fullstack',
                     'repository', 'commit', 'merge', 'branch', 'git', 'version', 'control'],
            'phrases': ['data structure', 'software engineering', 'code review', 'version control',
                       'unit test', 'integration test', 'test driven', 'object oriented',
                       'functional programming', 'design pattern', 'software architecture'],
            'weight': 5.0
        },
        # Tier 2: Strong coding indicators with context (weight: 4.0)
        'tier2': {
            'words': ['function', 'method', 'class', 'module', 'package', 'library', 'framework',
                     'api', 'database', 'query', 'schema', 'model', 'controller', 'view',
                     'import', 'export', 'namespace', 'scope', 'closure', 'callback'],
            'phrases': ['write code', 'create function', 'implement algorithm', 'build application',
                       'develop software', 'fix bug', 'handle error', 'parse data', 'rest api'],
            'weight': 4.0
        },
        # Tier 3: Technology-specific terms (weight: 3.5)
        'tier3': {
            'words': ['python', 'javascript', 'java', 'cpp', 'html', 'css', 'sql', 'react', 
                     'angular', 'vue', 'django', 'flask', 'spring', 'node', 'express',
                     'mongodb', 'postgresql', 'mysql', 'redis', 'docker', 'kubernetes',
                     'typescript', 'rust', 'golang', 'php', 'ruby', 'swift', 'kotlin'],
            'phrases': ['machine learning', 'artificial intelligence', 'deep learning',
                       'data science', 'web development', 'mobile development', 'devops'],
            'weight': 3.5
        },
        # Tier 4: Context-dependent terms (evaluated separately)
        'contextual': {
            'write': ['function', 'code', 'script', 'program', 'algorithm', 'class', 'method', 'api'],
            'create': ['application', 'website', 'api', 'database', 'function', 'class', 'component'],
            'build': ['application', 'system', 'website', 'api', 'software', 'tool', 'service'],
            'implement': ['algorithm', 'function', 'feature', 'system', 'solution', 'pattern'],
            'develop': ['software', 'application', 'system', 'website', 'api', 'service'],
            'debug': ['code', 'script', 'application', 'function', 'error', 'bug'],
            'optimize': ['code', 'algorithm', 'function', 'query', 'performance', 'system']
        }
    }
    
    # 2. REASONING CATEGORY - Cognitive analysis patterns
    reasoning_patterns = {
        'tier1': {
            'words': ['analyze', 'synthesize', 'evaluate', 'critique', 'deduce', 'infer',
                     'rationalize', 'substantiate', 'corroborate', 'extrapolate', 'hypothesize',
                     'theorem', 'proof', 'lemma', 'corollary', 'axiom', 'postulate'],
            'phrases': ['logical reasoning', 'critical thinking', 'cause and effect',
                       'pros and cons', 'compare and contrast', 'evidence based',
                       'scientific method', 'hypothesis testing'],
            'weight': 5.0
        },
        'tier2': {
            'words': ['explain', 'justify', 'demonstrate', 'prove', 'reason', 'conclude',
                     'hypothesis', 'theory', 'principle', 'methodology', 'philosophical',
                     'conceptual', 'abstract', 'logical', 'mathematical'],
            'phrases': ['explain why', 'reason about', 'think through', 'work through',
                       'step by step', 'break down', 'analyze data', 'thought process'],
            'weight': 4.0
        },
        'tier3': {
            'words': ['compare', 'contrast', 'evaluate', 'assess', 'examine', 'investigate',
                     'explore', 'research', 'study', 'review', 'calculate', 'compute',
                     'derive', 'formula', 'equation', 'statistics', 'probability'],
            'phrases': ['how does', 'why does', 'what if', 'given that', 'assuming that',
                       'in conclusion', 'therefore', 'as a result', 'consequently'],
            'weight': 3.0
        }
    }
    
    # 3. GENERAL CATEGORY - Conversational patterns
    general_patterns = {
        'conversational': {
            'words': ['hello', 'hi', 'thanks', 'please', 'help', 'chat', 'talk', 'discuss',
                     'opinion', 'feel', 'like', 'enjoy', 'prefer', 'favorite', 'best',
                     'recommendation', 'suggest', 'advice', 'tip', 'guide'],
            'phrases': ['how are you', 'nice to meet', 'good morning', 'have a nice',
                       'what do you think', 'in your opinion', 'tell me about'],
            'weight': 3.0
        },
        'informational': {
            'words': ['tell', 'show', 'describe', 'list', 'summary', 'overview', 'guide',
                     'tutorial', 'example', 'sample', 'basic', 'simple', 'beginner',
                     'introduction', 'what', 'who', 'when', 'where', 'which'],
            'phrases': ['tell me about', 'show me how', 'give me information', 'i want to know'],
            'weight': 2.5
        }
    }
    
    # =================== SCORING LOGIC ===================
    
    def score_patterns(patterns_dict: Dict, category: str) -> None:
        """Score patterns for a given category with precision weighting."""
        for tier, content in patterns_dict.items():
            if tier == 'contextual':
                # Handle contextual scoring
                for trigger_word, context_words in content.items():
                    if trigger_word in tokens:
                        context_matches = sum(1 for word in context_words if word in tokens)
                        if context_matches > 0:
                            category_scores[category] += 4.0 * context_matches
            else:
                weight = content['weight']
                
                # Score individual words
                for word in content['words']:
                    if word in tokens:
                        category_scores[category] += weight
                
                # Score phrases (higher precision)
                for phrase in content['phrases']:
                    if phrase in prompt_lower:
                        category_scores[category] += weight * 1.5  # Phrase bonus
    
    # Apply pattern scoring
    score_patterns(coding_patterns, 'coding')
    score_patterns(reasoning_patterns, 'reasoning')
    score_patterns(general_patterns, 'general')
    
    # =================== ADVANCED CONTEXTUAL ADJUSTMENTS ===================
    
    # Mathematical/Scientific context boosts reasoning
    math_science_terms = ['calculate', 'formula', 'equation', 'theorem', 'proof', 'statistics',
                         'probability', 'mathematical', 'scientific', 'research', 'experiment',
                         'hypothesis', 'analysis', 'methodology', 'data', 'metrics']
    math_score = sum(2.0 for term in math_science_terms if term in tokens)
    category_scores['reasoning'] += math_score
    
    # Question patterns boost reasoning for analytical questions
    analytical_question_patterns = [
        r'\bwhy\s+(?:does|do|is|are|would|should)',
        r'\bhow\s+(?:does|do|can|would|should)',
        r'\bwhat\s+(?:causes|makes|determines|influences)',
        r'\bwhich\s+(?:factors|elements|aspects)',
        r'\bexplain\s+(?:why|how|the)',
        r'\banalyze\s+(?:the|this|how|why)'
    ]
    
    for pattern in analytical_question_patterns:
        if re.search(pattern, prompt_lower):
            category_scores['reasoning'] += 3.0
    
    # Code-specific patterns with high precision
    code_request_patterns = [
        r'\b(?:write|create|build|implement|develop|generate)\s+(?:a|an|some)?\s*(?:function|method|class|script|program|code|algorithm)',
        r'\b(?:how\s+to\s+)?(?:code|program|script|implement)\s+(?:a|an|the)',
        r'\b(?:debug|fix|optimize|refactor)\s+(?:this|the|my)\s+(?:code|script|function|program)',
        r'\b(?:rest|api|database|sql|web)\s+(?:application|development|programming)',
        r'\b(?:python|javascript|java|react|django|node)\s+(?:code|function|application|development)'
    ]
    
    for pattern in code_request_patterns:
        if re.search(pattern, prompt_lower):
            category_scores['coding'] += 4.5
    
    # Technology stack detection
    tech_stacks = {
        'web': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'frontend', 'backend'],
        'backend': ['api', 'server', 'database', 'django', 'flask', 'spring', 'express'],
        'data': ['sql', 'mongodb', 'postgresql', 'mysql', 'data', 'analytics', 'ml'],
        'devops': ['docker', 'kubernetes', 'ci/cd', 'deployment', 'cloud', 'aws', 'azure']
    }
    
    for stack_type, keywords in tech_stacks.items():
        stack_matches = sum(1 for keyword in keywords if keyword in tokens)
        if stack_matches >= 2:  # Multiple keywords from same stack
            category_scores['coding'] += 2.0
    
    # =================== DOMAIN CLASSIFICATION ===================
    
    # Technical domain - infrastructure and systems
    technical_indicators = {
        'architecture': ['system', 'architecture', 'design', 'infrastructure', 'scalability'],
        'devops': ['deployment', 'ci/cd', 'docker', 'kubernetes', 'cloud', 'aws', 'azure'],
        'performance': ['optimization', 'performance', 'scalability', 'efficiency', 'monitoring'],
        'security': ['security', 'authentication', 'authorization', 'encryption', 'vulnerability'],
        'database': ['database', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis']
    }
    
    # Logical domain - analytical and mathematical
    logical_indicators = {
        'mathematical': ['algorithm', 'mathematical', 'calculation', 'formula', 'equation'],
        'analytical': ['analysis', 'reasoning', 'logic', 'proof', 'methodology'],
        'problem_solving': ['solve', 'problem', 'solution', 'approach', 'strategy'],
        'scientific': ['research', 'experiment', 'hypothesis', 'theory', 'evidence']
    }
    
    # Score domains with category influence
    for domain_type, keywords in technical_indicators.items():
        technical_matches = sum(1 for keyword in keywords if keyword in tokens)
        domain_scores['technical'] += technical_matches * 2.0
    
    for domain_type, keywords in logical_indicators.items():
        logical_matches = sum(1 for keyword in keywords if keyword in tokens)
        domain_scores['logical'] += logical_matches * 2.0
    
    # Category influence on domain
    if category_scores['coding'] > 6:
        domain_scores['technical'] += 3.0
    if category_scores['reasoning'] > 6:
        domain_scores['logical'] += 3.0
    
    # Default to casual for conversational prompts
    casual_indicators = ['chat', 'talk', 'discuss', 'opinion', 'think', 'feel', 'like', 'enjoy',
                        'personal', 'story', 'experience', 'recommendation', 'advice']
    casual_matches = sum(1 for indicator in casual_indicators if indicator in tokens)
    domain_scores['casual'] += casual_matches * 2.0 + 1.0  # Base casual score
    
    # =================== INTENT CLASSIFICATION ===================
    
    # Question intent - enhanced detection
    if '?' in prompt:
        intent_scores['question'] += 5.0
    
    question_starters = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should']
    for starter in question_starters:
        if prompt_lower.startswith(starter):
            intent_scores['question'] += 3.0
        elif starter in tokens[:3]:  # First three words
            intent_scores['question'] += 2.0
    
    # Instruction intent
    instruction_markers = ['please', 'could you', 'would you', 'can you', 'help me', 'show me', 'tell me']
    for marker in instruction_markers:
        if marker in prompt_lower:
            intent_scores['instruction'] += 4.0
    
    # Code request intent - precise patterns
    if re.search(r'\b(?:write|create|build|implement|develop|generate)\s+(?:a|an|some)?\s*(?:function|method|class|script|program|code|algorithm)', prompt_lower):
        intent_scores['code_request'] += 6.0
    elif category_scores['coding'] > 8 and any(word in tokens for word in ['write', 'create', 'build', 'implement']):
        intent_scores['code_request'] += 4.0
    
    # Reasoning task intent
    reasoning_tasks = ['explain', 'analyze', 'compare', 'evaluate', 'reason', 'prove', 'demonstrate', 'justify']
    for task in reasoning_tasks:
        if task in tokens and category_scores['reasoning'] > 3:
            intent_scores['reasoning_task'] += 4.0
    
    # =================== FINAL CLASSIFICATION ===================
    
    # Normalize scores and apply thresholds
    total_category_score = sum(category_scores.values())
    if total_category_score > 0:
        normalized_categories = {k: v/total_category_score for k, v in category_scores.items()}
    else:
        normalized_categories = category_scores
    
    # Select categories (precision threshold)
    threshold = 0.15  # 15% of total score minimum
    raw_threshold = 2.0  # Raw score minimum
    
    categories = []
    for category, score in category_scores.items():
        if score >= raw_threshold and normalized_categories[category] >= threshold:
            categories.append(category)
    
    # Ensure at least one category
    if not categories:
        categories = [max(category_scores.keys(), key=lambda k: category_scores[k])]
        if category_scores[categories[0]] == 0:
            categories = ['general']
    
    # Final classifications
    topic_domain = max(domain_scores.keys(), key=lambda k: domain_scores[k]) if max(domain_scores.values()) > 0 else 'casual'
    intent_type = max(intent_scores.keys(), key=lambda k: intent_scores[k]) if max(intent_scores.values()) > 0 else 'question'
    
    # Confidence scoring
    max_category_score = max(category_scores.values())
    max_domain_score = max(domain_scores.values())
    max_intent_score = max(intent_scores.values())
    
    confidence = {
        'category': min(max_category_score / 10.0, 1.0),  # Scale to 0-1
        'domain': min(max_domain_score / 8.0, 1.0),
        'intent': min(max_intent_score / 6.0, 1.0),
        'overall': min((max_category_score + max_domain_score + max_intent_score) / 24.0, 1.0)
    }
    
    return {
        'token_count': token_count,
        'categories': categories,
        'topic_domain': topic_domain,
        'intent_type': intent_type,
        'confidence': confidence,
        '_debug': {
            'category_scores': category_scores,
            'domain_scores': domain_scores,
            'intent_scores': intent_scores,
            'normalized_categories': normalized_categories,
            'tokens': tokens,
            'bigrams': bigrams[:5],  # First 5 bigrams for debugging
        }
    }


# Comprehensive precision test suite
if __name__ == "__main__":
    
    test_prompts = [
        # === CODING TESTS - Should clearly identify as coding ===
        "Write a Python function to sort an array using quicksort algorithm",
        "How do I implement a REST API using Django and PostgreSQL?",
        "Debug this JavaScript code that's throwing a TypeError",
        "Create a React component with TypeScript for user authentication",
        "Optimize this SQL query for better performance on large datasets",
        "Build a microservices architecture using Docker and Kubernetes",
        
        # === REASONING TESTS - Should clearly identify as reasoning ===
        "Explain why renewable energy is more sustainable than fossil fuels",
        "Analyze the economic implications of remote work on urban development",
        "Compare the effectiveness of different machine learning algorithms",
        "What are the logical fallacies in this argument about climate change?",
        "Prove that the square root of 2 is irrational using mathematical reasoning",
        "Evaluate the pros and cons of cryptocurrency adoption",
        
        # === CONTEXT-DEPENDENT TESTS - Should differentiate based on context ===
        "Write an essay about artificial intelligence ethics",      # reasoning/logical
        "Write a function to calculate compound interest",          # coding/technical
        "Build a compelling argument for space exploration",       # reasoning/logical
        "Build a web application with user login system",         # coding/technical
        "Create a presentation about data privacy concerns",      # reasoning/logical
        "Create a database schema for an e-commerce platform",    # coding/technical
        
        # === GENERAL/CONVERSATIONAL TESTS ===
        "Hello, how are you doing today?",
        "Can you help me understand what you can do?",
        "What's the weather like in New York?",
        "Tell me a fun fact about dolphins",
        "I'm feeling stressed about work, any advice?",
        
        # === MIXED/COMPLEX TESTS - Should show sophisticated classification ===
        "How do I write better code comments for my Python functions?",           # coding + reasoning
        "Explain the time complexity of this sorting algorithm and optimize it",  # reasoning + coding
        "What are the best practices for designing RESTful APIs?",               # coding + reasoning
        "Compare Python and JavaScript for backend development",                 # reasoning + coding
        
        # === EDGE CASES - Testing precision boundaries ===
        "write",  # Should be general (ambiguous)
        "build",  # Should be general (ambiguous)
        "explain recursion in programming",  # Should be reasoning with coding context
        "calculate 2+2",  # Should be reasoning (mathematical)
        "fix",  # Should be general (too vague)
    ]
    
    print("=== PRECISION PROMPT ANALYSIS RESULTS ===\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        result = extract_prompt_features(prompt)
        
        print(f"{i:2d}. \"{prompt}\"")
        print(f"    → Categories: {result['categories']}")
        print(f"    → Domain: {result['topic_domain']} | Intent: {result['intent_type']}")
        print(f"    → Tokens: {result['token_count']} | Confidence: {result['confidence']['overall']:.3f}")
        
        # Show detailed scoring for interesting cases
        if result['confidence']['overall'] > 0.5 or len(result['categories']) > 1:
            debug = result['_debug']
            scores = debug['category_scores']
            print(f"    → Scores: C:{scores['coding']:.1f} R:{scores['reasoning']:.1f} G:{scores['general']:.1f}")
            
        print()
    
    print("\n=== PRECISION METRICS ===")
    print("Legend: C=Coding, R=Reasoning, G=General")
    print("High confidence (>0.5) indicates clear classification")
    print("Multiple categories show sophisticated context detection")
