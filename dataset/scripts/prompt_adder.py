"""
Prompt Adding Tool for OrchestrateX Dataset
Author: Sahil (Part 2 - Dataset Creation & Model Specialty Analysis)

This tool helps you easily add new prompts to your dataset.
Use this to gradually expand each domain to 500+ prompts.
"""

import json
import os
from datetime import datetime

class PromptAdder:
    """Tool to help add new prompts to existing dataset"""
    
    def __init__(self):
        self.domains = [
            "coding", "creative_writing", "factual_qa", 
            "mathematical_reasoning", "language_translation", "sentiment_analysis"
        ]
    
    def create_prompt_template(self, prompt, domain, difficulty="medium", category="general"):
        """Create a standardized prompt template"""
        return {
            "id": f"{domain}_{len(prompt)}_{hash(prompt) % 10000}",
            "prompt": prompt,
            "domain": domain,
            "difficulty": difficulty,
            "category": category,
            "language": "english",
            "created_at": datetime.now().isoformat(),
            "chatbot_responses": {},
            "ratings": {},
            "metadata": {}
        }
    
    def load_existing_prompts(self, domain):
        """Load existing prompts for a domain"""
        filename = f"../raw_data/{domain}_prompts.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_prompts(self, domain, prompts):
        """Save prompts to file"""
        filename = f"../raw_data/{domain}_prompts.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(prompts)} prompts for {domain}")
    
    def add_prompts_to_domain(self, domain, new_prompts_data):
        """Add new prompts to a domain"""
        existing_prompts = self.load_existing_prompts(domain)
        
        added_count = 0
        for prompt_data in new_prompts_data:
            prompt_text = prompt_data.get("prompt", "")
            difficulty = prompt_data.get("difficulty", "medium")
            category = prompt_data.get("category", "general")
            
            if prompt_text:
                new_prompt = self.create_prompt_template(prompt_text, domain, difficulty, category)
                existing_prompts.append(new_prompt)
                added_count += 1
        
        self.save_prompts(domain, existing_prompts)
        print(f"➕ Added {added_count} new prompts to {domain}")
        return len(existing_prompts)
    
    def show_domain_status(self, domain):
        """Show current status of a domain"""
        prompts = self.load_existing_prompts(domain)
        count = len(prompts)
        target = 500
        progress = (count / target) * 100
        
        print(f"\n📊 {domain.upper().replace('_', ' ')} STATUS:")
        print(f"   Current: {count}/{target} prompts")
        print(f"   Progress: {progress:.1f}%")
        print(f"   Remaining: {target - count} prompts needed")
        
        if count > 0:
            # Show categories
            categories = {}
            difficulties = {}
            for prompt in prompts:
                cat = prompt.get("category", "general")
                diff = prompt.get("difficulty", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
                difficulties[diff] = difficulties.get(diff, 0) + 1
            
            print(f"   Categories: {len(categories)} ({', '.join(categories.keys())})")
            print(f"   Difficulties: {len(difficulties)} ({', '.join(difficulties.keys())})")
    
    def bulk_add_coding_prompts(self):
        """Add more coding prompts"""
        coding_prompts = [
            {"prompt": "Write a Python function to check if a number is prime", "difficulty": "easy", "category": "algorithms"},
            {"prompt": "Create a React component for a todo list", "difficulty": "medium", "category": "web_development"},
            {"prompt": "Implement a stack data structure in Java", "difficulty": "medium", "category": "data_structures"},
            {"prompt": "Write a SQL query to find duplicate records", "difficulty": "medium", "category": "database"},
            {"prompt": "Create a RESTful API for user authentication", "difficulty": "hard", "category": "api_development"},
            {"prompt": "Debug this infinite loop in JavaScript", "difficulty": "easy", "category": "debugging"},
            {"prompt": "Write unit tests for a shopping cart class", "difficulty": "medium", "category": "testing"},
            {"prompt": "Optimize this O(n²) algorithm to O(n log n)", "difficulty": "hard", "category": "optimization"},
            {"prompt": "Explain inheritance in object-oriented programming", "difficulty": "easy", "category": "oop"},
            {"prompt": "Create a binary search tree in C++", "difficulty": "hard", "category": "data_structures"},
            {"prompt": "Write a function to reverse a string without using built-in methods", "difficulty": "easy", "category": "algorithms"},
            {"prompt": "How do you handle asynchronous operations in JavaScript?", "difficulty": "medium", "category": "javascript"},
            {"prompt": "Create a database connection pool in Node.js", "difficulty": "hard", "category": "backend"},
            {"prompt": "Write a function to find the nth Fibonacci number", "difficulty": "easy", "category": "algorithms"},
            {"prompt": "Implement error handling in a Python web application", "difficulty": "medium", "category": "error_handling"}
        ]
        
        return self.add_prompts_to_domain("coding", coding_prompts)
    
    def bulk_add_creative_writing_prompts(self):
        """Add more creative writing prompts"""
        creative_prompts = [
            {"prompt": "Write a story about a library where books come to life at night", "difficulty": "medium", "category": "fantasy"},
            {"prompt": "Create a character who can taste colors", "difficulty": "easy", "category": "character_development"},
            {"prompt": "Describe a world where gravity works differently", "difficulty": "hard", "category": "world_building"},
            {"prompt": "Write a dialogue between the sun and the moon", "difficulty": "easy", "category": "dialogue"},
            {"prompt": "Create a mystery story set in a space station", "difficulty": "hard", "category": "mystery"},
            {"prompt": "Write a poem about memories fading away", "difficulty": "medium", "category": "poetry"},
            {"prompt": "Describe a day in the life of a superhero's pet", "difficulty": "easy", "category": "humor"},
            {"prompt": "Write a love story between two AIs", "difficulty": "medium", "category": "sci_fi"},
            {"prompt": "Create a horror story about a friendly monster", "difficulty": "medium", "category": "horror"},
            {"prompt": "Write a letter from Earth to Mars in the year 2150", "difficulty": "medium", "category": "sci_fi"},
            {"prompt": "Describe a magical school for unusual talents", "difficulty": "medium", "category": "fantasy"},
            {"prompt": "Write a story that takes place entirely in an elevator", "difficulty": "hard", "category": "constraint_writing"},
            {"prompt": "Create a character description using only dialogue", "difficulty": "hard", "category": "technique"},
            {"prompt": "Write a story where the ending changes the meaning of the beginning", "difficulty": "hard", "category": "plot_twist"},
            {"prompt": "Describe a meal that transports someone to their childhood", "difficulty": "medium", "category": "sensory_writing"}
        ]
        
        return self.add_prompts_to_domain("creative_writing", creative_prompts)
    
    def bulk_add_factual_qa_prompts(self):
        """Add more factual Q&A prompts"""
        factual_prompts = [
            {"prompt": "What is the difference between weather and climate?", "difficulty": "easy", "category": "science"},
            {"prompt": "Explain how the internet works", "difficulty": "medium", "category": "technology"},
            {"prompt": "What caused the fall of the Roman Empire?", "difficulty": "medium", "category": "history"},
            {"prompt": "How do electric cars work?", "difficulty": "medium", "category": "technology"},
            {"prompt": "What is the significance of the Rosetta Stone?", "difficulty": "medium", "category": "history"},
            {"prompt": "Explain the concept of inflation in economics", "difficulty": "medium", "category": "economics"},
            {"prompt": "What is CRISPR and how is it used?", "difficulty": "hard", "category": "science"},
            {"prompt": "How do satellites stay in orbit?", "difficulty": "medium", "category": "physics"},
            {"prompt": "What is the largest ocean on Earth?", "difficulty": "easy", "category": "geography"},
            {"prompt": "Explain the process of DNA replication", "difficulty": "hard", "category": "biology"},
            {"prompt": "What is the greenhouse effect?", "difficulty": "easy", "category": "environment"},
            {"prompt": "How do vaccines prevent diseases?", "difficulty": "medium", "category": "health"},
            {"prompt": "What is quantum computing?", "difficulty": "hard", "category": "technology"},
            {"prompt": "Explain the water cycle", "difficulty": "easy", "category": "science"},
            {"prompt": "What is blockchain technology?", "difficulty": "medium", "category": "technology"}
        ]
        
        return self.add_prompts_to_domain("factual_qa", factual_prompts)
    
    def bulk_add_math_prompts(self):
        """Add math prompts - PRIORITY for this week"""
        math_prompts = [
            # Basic Arithmetic
            {"prompt": "Calculate 847 + 293", "difficulty": "easy", "category": "arithmetic"},
            {"prompt": "What is 25% of 160?", "difficulty": "easy", "category": "arithmetic"},
            {"prompt": "If you buy 3 items for $12.50 each, what's the total cost?", "difficulty": "easy", "category": "arithmetic"},
            
            # Algebra
            {"prompt": "Solve for x: 4x - 9 = 23", "difficulty": "medium", "category": "algebra"},
            {"prompt": "If y = 2x + 5 and x = 3, what is y?", "difficulty": "easy", "category": "algebra"},
            {"prompt": "Solve the system: 2x + y = 8, x - y = 1", "difficulty": "medium", "category": "algebra"},
            
            # Geometry
            {"prompt": "Find the perimeter of a rectangle with length 15 and width 8", "difficulty": "easy", "category": "geometry"},
            {"prompt": "What is the volume of a cube with side length 6?", "difficulty": "easy", "category": "geometry"},
            {"prompt": "Calculate the area of a triangle with base 10 and height 7", "difficulty": "easy", "category": "geometry"},
            
            # Word Problems
            {"prompt": "A car travels 240 miles in 4 hours. What is its average speed?", "difficulty": "easy", "category": "word_problems"},
            {"prompt": "If a pizza is cut into 8 slices and you eat 3, what fraction is left?", "difficulty": "easy", "category": "word_problems"},
            {"prompt": "Sarah has $50. She spends $18 on lunch and $12 on a book. How much does she have left?", "difficulty": "easy", "category": "word_problems"},
            
            # Probability
            {"prompt": "What's the probability of rolling a 6 on a standard die?", "difficulty": "easy", "category": "probability"},
            {"prompt": "If you flip two coins, what's the probability both are heads?", "difficulty": "medium", "category": "probability"},
            {"prompt": "In a bag of 20 marbles (12 red, 8 blue), what's the probability of drawing a red marble?", "difficulty": "medium", "category": "probability"},
            
            # Statistics
            {"prompt": "Find the mean of: 5, 8, 12, 15, 20", "difficulty": "easy", "category": "statistics"},
            {"prompt": "What is the median of: 3, 7, 9, 12, 18, 21?", "difficulty": "easy", "category": "statistics"},
            {"prompt": "Calculate the range of: 45, 67, 23, 89, 34, 56", "difficulty": "easy", "category": "statistics"},
            
            # Advanced
            {"prompt": "Find the derivative of f(x) = 3x² + 2x - 1", "difficulty": "hard", "category": "calculus"},
            {"prompt": "Calculate the compound interest on $1000 at 5% annually for 3 years", "difficulty": "medium", "category": "financial_math"},
            {"prompt": "If log₂(x) = 5, what is x?", "difficulty": "hard", "category": "logarithms"}
        ]
        
        return self.add_prompts_to_domain("mathematical_reasoning", math_prompts)
    
    def bulk_add_translation_prompts(self):
        """Add translation prompts - PRIORITY for this week"""
        translation_prompts = [
            # Spanish
            {"prompt": "Translate 'Where is the bathroom?' to Spanish", "difficulty": "easy", "category": "basic_phrases"},
            {"prompt": "How do you say 'I would like to order food' in Spanish?", "difficulty": "medium", "category": "restaurant"},
            {"prompt": "Translate 'The meeting is at 3 PM tomorrow' to Spanish", "difficulty": "medium", "category": "business"},
            {"prompt": "Convert 'Happy birthday to you!' to Spanish", "difficulty": "easy", "category": "celebrations"},
            
            # French
            {"prompt": "Translate 'Excuse me, can you help me?' to French", "difficulty": "medium", "category": "polite_phrases"},
            {"prompt": "How do you say 'I love this city' in French?", "difficulty": "easy", "category": "expressions"},
            {"prompt": "Translate 'The train arrives at 6:30' to French", "difficulty": "medium", "category": "travel"},
            {"prompt": "Convert 'Good evening, how are you?' to French", "difficulty": "easy", "category": "greetings"},
            
            # German
            {"prompt": "Translate 'How much does this cost?' to German", "difficulty": "medium", "category": "shopping"},
            {"prompt": "How do you say 'I need a doctor' in German?", "difficulty": "medium", "category": "emergency"},
            {"prompt": "Translate 'The weather is beautiful today' to German", "difficulty": "easy", "category": "weather"},
            {"prompt": "Convert 'Please speak slowly' to German", "difficulty": "medium", "category": "communication"},
            
            # Chinese (Mandarin)
            {"prompt": "Translate 'Hello, nice to meet you' to Chinese", "difficulty": "easy", "category": "greetings"},
            {"prompt": "How do you say 'Thank you very much' in Chinese?", "difficulty": "easy", "category": "gratitude"},
            {"prompt": "Translate 'Where is the nearest hospital?' to Chinese", "difficulty": "hard", "category": "directions"},
            {"prompt": "Convert 'I don't understand' to Chinese", "difficulty": "medium", "category": "communication"},
            
            # Japanese
            {"prompt": "Translate 'Excuse me, where is the station?' to Japanese", "difficulty": "hard", "category": "directions"},
            {"prompt": "How do you say 'Good morning' in Japanese?", "difficulty": "easy", "category": "greetings"},
            {"prompt": "Translate 'I'm sorry, I'm late' to Japanese", "difficulty": "medium", "category": "apologies"},
            {"prompt": "Convert 'The food is delicious' to Japanese", "difficulty": "medium", "category": "dining"},
            
            # Multi-language
            {"prompt": "Translate 'Can I have the bill, please?' to Italian", "difficulty": "medium", "category": "restaurant"},
            {"prompt": "How do you say 'I'm lost' in Italian?", "difficulty": "medium", "category": "travel"},
            {"prompt": "Translate 'What time is it?' to Portuguese", "difficulty": "easy", "category": "time"},
            {"prompt": "How do you say 'I'm learning Portuguese' in Portuguese?", "difficulty": "medium", "category": "language_learning"},
            {"prompt": "Translate 'Yes, please' to Russian", "difficulty": "medium", "category": "basic_responses"},
            {"prompt": "How do you say 'Goodbye' in Russian?", "difficulty": "easy", "category": "farewells"}
        ]
        
        return self.add_prompts_to_domain("language_translation", translation_prompts)
    
    def bulk_add_khan_academy_math(self):
        """Add 10 Khan Academy algebra foundation prompts collected by Sahil"""
        khan_math_prompts = [
            {"prompt": "Simplify to create an equivalent expression: 8k - 5(-5k + 3)", "difficulty": "medium", "category": "algebraic_simplification"},
            {"prompt": "Combine like terms to create an equivalent expression: 7.4z - 5(-1.6z + 2.4)", "difficulty": "medium", "category": "combining_like_terms"},
            {"prompt": "Which expressions are equivalent to 4d + 6 + 2d?", "difficulty": "medium", "category": "equivalent_expressions"},
            {"prompt": "Combine like terms to create an equivalent expression: 1.3b + 7.8 - 3.2b", "difficulty": "medium", "category": "combining_like_terms"},
            {"prompt": "Simplify to create an equivalent expression: 6(7 - 3y) + 6(y + 1)", "difficulty": "medium", "category": "distributive_property"},
            {"prompt": "Evaluate ab - 0.5b when a = 1 and b = 5", "difficulty": "medium", "category": "variable_evaluation"},
            {"prompt": "Evaluate 4 - 0.25g + 0.5h when g = 10 and h = 5", "difficulty": "medium", "category": "variable_evaluation"},
            {"prompt": "Evaluate e - (1/2)f when e = 15 and f = 2", "difficulty": "medium", "category": "variable_evaluation"},
            {"prompt": "Evaluate 0.3y + (y/z) when y = 10 and z = 5", "difficulty": "hard", "category": "variable_evaluation"},
            {"prompt": "Evaluate 8p + 3q - 18 when p = 1/2 and q = 7", "difficulty": "medium", "category": "variable_evaluation"}
        ]
        
        return self.add_prompts_to_domain("mathematical_reasoning", khan_math_prompts)
    
    def priority_expansion(self):
        """Add prompts to priority domains - Math and Translation"""
        print("🎯 PRIORITY EXPANSION: Math & Translation")
        print("=" * 50)
        
        # Show initial status
        for domain in ["mathematical_reasoning", "language_translation"]:
            self.show_domain_status(domain)
        
        print("\n📝 Adding priority prompts...")
        
        # Add prompts to priority domains
        math_total = self.bulk_add_math_prompts()
        translation_total = self.bulk_add_translation_prompts()
        
        print(f"\n✅ Priority expansion complete!")
        print(f"📊 Updated totals:")
        print(f"   Mathematical Reasoning: {math_total} prompts")
        print(f"   Language Translation: {translation_total} prompts")
        
        # Show updated status
        print(f"\n📈 Updated status:")
        for domain in ["mathematical_reasoning", "language_translation"]:
            self.show_domain_status(domain)
    
    def demo_expansion(self):
        """Demonstrate how to expand the dataset"""
        print("🚀 Demonstrating Dataset Expansion")
        print("=" * 50)
        
        # Show initial status
        for domain in ["coding", "creative_writing", "factual_qa"]:
            self.show_domain_status(domain)
        
        print("\n📝 Adding new prompts...")
        
        # Add prompts to each domain
        coding_total = self.bulk_add_coding_prompts()
        creative_total = self.bulk_add_creative_writing_prompts()  
        factual_total = self.bulk_add_factual_qa_prompts()
        
        print(f"\n✅ Expansion complete!")
        print(f"📊 Updated totals:")
        print(f"   Coding: {coding_total} prompts")
        print(f"   Creative Writing: {creative_total} prompts")
        print(f"   Factual Q&A: {factual_total} prompts")
        
        # Show updated status
        print(f"\n📈 Updated status:")
        for domain in ["coding", "creative_writing", "factual_qa"]:
            self.show_domain_status(domain)

def main():
    """Main function with menu"""
    print("🎯 OrchestrateX Prompt Adding Tool")
    print("=" * 50)
    
    adder = PromptAdder()
    
    print("What would you like to do?")
    print("1. 📊 Show current status of all domains")
    print("2. ➕ Add sample prompts to coding, creative writing, and factual Q&A")
    print("3. 🎯 PRIORITY: Add math & translation prompts (URGENT)")
    print("4. 🧮 Add only math prompts")
    print("5. 🌍 Add only translation prompts")
    print("6. � Add Khan Academy math prompts (Sahil's collection)")
    print("7. �📋 Show instructions for manual prompt addition")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == "1":
        print("\n📊 Current Dataset Status:")
        print("=" * 30)
        for domain in adder.domains:
            adder.show_domain_status(domain)
    
    elif choice == "2":
        adder.demo_expansion()
    
    elif choice == "3":
        adder.priority_expansion()
    
    elif choice == "4":
        total = adder.bulk_add_math_prompts()
        print(f"\n✅ Added math prompts! Total in domain: {total}")
        adder.show_domain_status("mathematical_reasoning")
    
    elif choice == "5":
        total = adder.bulk_add_translation_prompts()
        print(f"\n✅ Added translation prompts! Total in domain: {total}")
        adder.show_domain_status("language_translation")
    
    elif choice == "6":
        total = adder.bulk_add_khan_academy_math()
        print(f"\n✅ Added Khan Academy math prompts! Total in domain: {total}")
        adder.show_domain_status("mathematical_reasoning")
    
    elif choice == "7":
        print("\n📋 How to Add Prompts Manually:")
        print("=" * 40)
        print("1. Choose a domain to work on")
        print("2. Pick a category from the expansion plan")
        print("3. Create prompts with different difficulty levels")
        print("4. Use this script to add them to the dataset")
        print("5. Aim for 40-50 prompts per category")
        print("\n💡 TIP: Start with domains you're most comfortable with!")
        print("\n🎯 CURRENT PRIORITY: Mathematical Reasoning & Language Translation")
        print("   → These domains have only 10 prompts each (2% complete)")
        print("   → Easiest way: Choose option 3 to add both at once!")
    
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
