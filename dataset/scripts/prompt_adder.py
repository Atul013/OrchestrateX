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
    print("3. 📋 Show instructions for manual prompt addition")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n📊 Current Dataset Status:")
        print("=" * 30)
        for domain in adder.domains:
            adder.show_domain_status(domain)
    
    elif choice == "2":
        adder.demo_expansion()
    
    elif choice == "3":
        print("\n📋 How to Add Prompts Manually:")
        print("=" * 40)
        print("1. Choose a domain to work on")
        print("2. Pick a category from the expansion plan")
        print("3. Create prompts with different difficulty levels")
        print("4. Use this script to add them to the dataset")
        print("5. Aim for 40-50 prompts per category")
        print("\n💡 TIP: Start with domains you're most comfortable with!")
    
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
