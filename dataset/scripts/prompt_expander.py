"""
Prompt Expansion Tool for OrchestrateX Dataset
Author: Sahil (Part 2 - Dataset Creation & Model Specialty Analysis)

This script helps expand your prompt collection by providing structured templates
and guidelines for each domain to reach the 500+ prompts target.
"""

import json
import os
from datetime import datetime

class PromptExpander:
    """Tool to help expand prompts for each domain"""
    
    def __init__(self):
        self.domains = {
            "coding": {
                "categories": [
                    "basic_syntax", "data_structures", "algorithms", "web_development",
                    "database", "debugging", "testing", "frameworks", "api_development",
                    "object_oriented", "functional_programming", "performance_optimization"
                ],
                "difficulty_levels": ["beginner", "intermediate", "advanced", "expert"],
                "languages": ["python", "javascript", "java", "c++", "react", "sql", "general"]
            },
            "creative_writing": {
                "categories": [
                    "short_stories", "poetry", "dialogues", "character_descriptions",
                    "scene_descriptions", "plot_development", "world_building", "letters",
                    "monologues", "song_lyrics", "screenplay", "flash_fiction"
                ],
                "difficulty_levels": ["simple", "moderate", "complex", "literary"],
                "genres": ["fantasy", "sci-fi", "mystery", "romance", "horror", "comedy", "drama"]
            },
            "factual_qa": {
                "categories": [
                    "geography", "history", "science", "technology", "literature", "arts",
                    "politics", "economics", "sports", "health", "environment", "culture"
                ],
                "difficulty_levels": ["basic", "intermediate", "advanced", "expert"],
                "question_types": ["definition", "explanation", "comparison", "analysis", "factual"]
            },
            "mathematical_reasoning": {
                "categories": [
                    "arithmetic", "algebra", "geometry", "calculus", "statistics", "probability",
                    "logic", "number_theory", "word_problems", "proofs", "optimization"
                ],
                "difficulty_levels": ["elementary", "high_school", "undergraduate", "graduate"],
                "topics": ["basic_math", "advanced_math", "applied_math", "theoretical_math"]
            },
            "language_translation": {
                "categories": [
                    "basic_phrases", "conversations", "formal_text", "technical_terms",
                    "literature", "business", "medical", "legal", "tourism", "education"
                ],
                "difficulty_levels": ["basic", "intermediate", "advanced", "professional"],
                "languages": ["spanish", "french", "german", "italian", "chinese", "japanese", "arabic", "portuguese"]
            },
            "sentiment_analysis": {
                "categories": [
                    "product_reviews", "movie_reviews", "social_media", "customer_feedback",
                    "news_articles", "personal_expressions", "business_communications", "literature"
                ],
                "difficulty_levels": ["clear", "neutral", "mixed", "sarcastic"],
                "sentiment_types": ["positive", "negative", "neutral", "mixed", "sarcastic"]
            }
        }
    
    def generate_prompt_templates(self, domain):
        """Generate prompt templates for a specific domain"""
        templates = []
        domain_info = self.domains.get(domain, {})
        
        if domain == "coding":
            templates = [
                f"Write a {lang} function to {task}",
                f"Implement {algorithm} in {lang}",
                f"Create a {category} solution for {problem}",
                f"How do you {action} in {lang}?",
                f"Debug this {lang} code: {code_snippet}",
                f"Optimize this {category} code for better performance",
                f"Explain the difference between {concept1} and {concept2} in {lang}",
                f"Create a {difficulty} level {category} project",
                f"Write unit tests for {functionality}",
                f"Design a {architecture} for {application_type}"
            ]
        
        elif domain == "creative_writing":
            templates = [
                f"Write a {genre} {category} about {theme}",
                f"Create a character who {characteristic}",
                f"Describe a {setting} in {tone} style",
                f"Write a dialogue between {character1} and {character2}",
                f"Compose a {poetry_type} about {subject}",
                f"Create a {length} story that starts with '{opening_line}'",
                f"Write a {genre} scene involving {conflict}",
                f"Develop a {character_type} backstory",
                f"Create a {world_type} setting for a story",
                f"Write a letter from {sender} to {receiver}"
            ]
        
        elif domain == "factual_qa":
            templates = [
                f"What is {concept} and how does it work?",
                f"Explain the {topic} in {context}",
                f"Who was {historical_figure} and why are they important?",
                f"What are the main causes of {phenomenon}?",
                f"How does {process} affect {subject}?",
                f"What is the difference between {concept1} and {concept2}?",
                f"Describe the {geographical_feature} of {location}",
                f"What happened during {historical_event}?",
                f"Explain the significance of {cultural_element}",
                f"What are the {number} most important {topic}?"
            ]
        
        elif domain == "mathematical_reasoning":
            templates = [
                f"Solve: {equation_type}",
                f"Find the {calculation} of {geometric_shape}",
                f"Calculate the probability of {event}",
                f"Prove that {mathematical_statement}",
                f"Optimize {function} subject to {constraints}",
                f"A {scenario} problem: {word_problem}",
                f"Find the derivative/integral of {function}",
                f"Solve the system: {system_of_equations}",
                f"What is the {statistic} of {dataset}?",
                f"Explain {mathematical_concept} with an example"
            ]
        
        elif domain == "language_translation":
            templates = [
                f"Translate '{phrase}' to {target_language}",
                f"How do you say '{expression}' in {target_language}?",
                f"Convert this {text_type} to {target_language}: '{text}'",
                f"Translate and explain the cultural context: '{phrase}'",
                f"What is the {formality_level} way to say '{phrase}' in {target_language}?",
                f"Translate this {domain_specific} term: '{term}'",
                f"How would you express '{concept}' in {target_language}?",
                f"Translate this {length} text to {target_language}",
                f"What are different ways to say '{phrase}' in {target_language}?",
                f"Translate and maintain the {tone} tone: '{text}'"
            ]
        
        elif domain == "sentiment_analysis":
            templates = [
                f"Analyze the sentiment: '{text_sample}'",
                f"What's the emotional tone of: '{text_sample}'?",
                f"Classify the sentiment in this {context}: '{text_sample}'",
                f"Determine if this {text_type} is positive, negative, or neutral: '{text_sample}'",
                f"What sentiment does this express: '{text_sample}'?",
                f"Rate the sentiment intensity of: '{text_sample}'",
                f"Identify the emotions in: '{text_sample}'",
                f"Is this {text_type} sarcastic or sincere: '{text_sample}'?",
                f"What's the overall sentiment of this {context}: '{text_sample}'",
                f"Analyze the sentiment and explain why: '{text_sample}'"
            ]
        
        return templates
    
    def create_expansion_guide(self, domain):
        """Create a detailed expansion guide for a specific domain"""
        domain_info = self.domains.get(domain, {})
        
        guide = {
            "domain": domain,
            "current_count": self.get_current_prompt_count(domain),
            "target_count": 500,
            "remaining_needed": 500 - self.get_current_prompt_count(domain),
            "categories": domain_info.get("categories", []),
            "difficulty_levels": domain_info.get("difficulty_levels", []),
            "templates": self.generate_prompt_templates(domain),
            "data_sources": self.get_data_sources(domain),
            "expansion_strategy": self.get_expansion_strategy(domain)
        }
        
        return guide
    
    def get_current_prompt_count(self, domain):
        """Get current number of prompts for a domain"""
        filename = f"../raw_data/{domain}_prompts.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return len(data)
        return 0
    
    def get_data_sources(self, domain):
        """Get recommended data sources for each domain"""
        sources = {
            "coding": [
                "HumanEval dataset",
                "MBPP (Mostly Basic Python Problems)",
                "CodeContests",
                "LeetCode problems",
                "GitHub repositories",
                "Stack Overflow questions",
                "Programming interview books"
            ],
            "creative_writing": [
                "WritingPrompts subreddit",
                "Story Cloze Test",
                "Creative writing textbooks",
                "Literary magazines",
                "Writing contest prompts",
                "Creative writing courses",
                "Author interviews"
            ],
            "factual_qa": [
                "MMLU (Massive Multitask Language Understanding)",
                "TriviaQA",
                "Natural Questions",
                "Wikipedia articles",
                "Educational textbooks",
                "News articles",
                "Encyclopedia entries"
            ],
            "mathematical_reasoning": [
                "GSM8K (Grade School Math 8K)",
                "MathQA",
                "MAWPS (Math Word Problems)",
                "Mathematics textbooks",
                "Online math problems",
                "Academic papers",
                "Math competition problems"
            ],
            "language_translation": [
                "WMT (Workshop on Machine Translation)",
                "Flores-101",
                "OpenSubtitles",
                "News articles in multiple languages",
                "Language learning materials",
                "UN documents",
                "Bilingual dictionaries"
            ],
            "sentiment_analysis": [
                "SST-2 (Stanford Sentiment Treebank)",
                "IMDB movie reviews",
                "Yelp reviews",
                "Amazon product reviews",
                "Twitter sentiment datasets",
                "Customer feedback",
                "Social media posts"
            ]
        }
        
        return sources.get(domain, [])
    
    def get_expansion_strategy(self, domain):
        """Get expansion strategy for each domain"""
        strategies = {
            "coding": [
                "1. Cover all major programming languages (Python, JavaScript, Java, C++, etc.)",
                "2. Include different difficulty levels from beginner to expert",
                "3. Add prompts for web development, data science, algorithms, debugging",
                "4. Include code review and optimization prompts",
                "5. Add architecture and design pattern questions"
            ],
            "creative_writing": [
                "1. Cover multiple genres (fantasy, sci-fi, mystery, romance, etc.)",
                "2. Include different formats (stories, poems, dialogues, scripts)",
                "3. Add various lengths from flash fiction to longer pieces",
                "4. Include different tones and styles",
                "5. Add prompts for character and world development"
            ],
            "factual_qa": [
                "1. Cover diverse topics (science, history, geography, culture)",
                "2. Include different question types (who, what, when, where, why, how)",
                "3. Add various difficulty levels from basic to expert",
                "4. Include current events and historical facts",
                "5. Add cross-cultural and international perspectives"
            ],
            "mathematical_reasoning": [
                "1. Cover all math levels from arithmetic to advanced calculus",
                "2. Include word problems and pure math",
                "3. Add step-by-step reasoning requirements",
                "4. Include geometric, algebraic, and statistical problems",
                "5. Add real-world application problems"
            ],
            "language_translation": [
                "1. Cover major world languages (Spanish, French, German, Chinese, etc.)",
                "2. Include different text types (formal, informal, technical, literary)",
                "3. Add various sentence lengths and complexities",
                "4. Include cultural context and idioms",
                "5. Add bidirectional translations"
            ],
            "sentiment_analysis": [
                "1. Include clear positive, negative, and neutral examples",
                "2. Add subtle sentiments and mixed emotions",
                "3. Include sarcasm and irony examples",
                "4. Cover different contexts (reviews, social media, formal text)",
                "5. Add emotion intensity variations"
            ]
        }
        
        return strategies.get(domain, [])
    
    def save_expansion_guide(self, domain):
        """Save expansion guide to file"""
        guide = self.create_expansion_guide(domain)
        
        # Ensure processed_data directory exists
        processed_data_dir = "../processed_data"
        if not os.path.exists(processed_data_dir):
            os.makedirs(processed_data_dir)
        
        filename = f"{processed_data_dir}/{domain}_expansion_guide.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Expansion guide saved for {domain}")
        return guide
    
    def generate_all_expansion_guides(self):
        """Generate expansion guides for all domains"""
        print("🚀 Generating Expansion Guides for All Domains")
        print("=" * 50)
        
        total_current = 0
        total_target = 0
        
        for domain in self.domains.keys():
            guide = self.save_expansion_guide(domain)
            current = guide["current_count"]
            target = guide["target_count"]
            remaining = guide["remaining_needed"]
            
            total_current += current
            total_target += target
            
            print(f"\n📁 {domain.upper()}:")
            print(f"   Current: {current}/{target} prompts")
            print(f"   Remaining: {remaining} prompts needed")
            print(f"   Progress: {(current/target)*100:.1f}%")
        
        print(f"\n📊 OVERALL PROGRESS:")
        print(f"Total prompts: {total_current}/{total_target}")
        print(f"Overall progress: {(total_current/total_target)*100:.1f}%")
        print(f"\n✅ All expansion guides created in: dataset/processed_data/")

def main():
    """Main execution function"""
    print("🎯 OrchestrateX Prompt Expansion Tool")
    print("=" * 50)
    
    expander = PromptExpander()
    expander.generate_all_expansion_guides()
    
    print("\n📋 Next Steps for Sahil:")
    print("1. ✅ Review expansion guides in dataset/processed_data/")
    print("2. 🔍 Research the recommended data sources")
    print("3. 📝 Use templates to create more prompts")
    print("4. 🎚️ Add difficulty levels and categories")
    print("5. 🌍 Include multilingual prompts")
    print("6. 🤖 Start collecting model responses")

if __name__ == "__main__":
    main()
