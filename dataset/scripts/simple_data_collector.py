"""
Simple Dataset Collection Script for OrchestrateX
Author: Sahil (Part 2 - Dataset Creation & Model Specialty Analysis)

This script helps collect prompts from various sources and organize them by domain.
No external dependencies required - uses only Python standard library.
"""

import json
import os
from datetime import datetime

class DatasetCollector:
    """Main class for collecting and organizing dataset prompts"""
    
    def __init__(self):
        self.domains = [
            "coding",
            "creative_writing", 
            "factual_qa",
            "mathematical_reasoning",
            "language_translation",
            "sentiment_analysis"
        ]
        
        self.models = [
            "GLM 4.5",
            "Llama 3.1", 
            "GPT OSS",
            "Mistral",
            "Claude 3.5"
        ]
        
        self.target_prompts_per_domain = 500
        
    def create_prompt_template(self, prompt, domain):
        """Create a standardized prompt template"""
        return {
            "id": f"{domain}_{len(prompt)}_{hash(prompt) % 10000}",
            "prompt": prompt,
            "domain": domain,
            "difficulty": "unknown",  # To be classified later
            "language": "english",    # Default, can be updated
            "created_at": datetime.now().isoformat(),
            "chatbot_responses": {},
            "ratings": {},
            "metadata": {}
        }
    
    def load_sample_prompts(self):
        """Load sample prompts for each domain to get started"""
        sample_prompts = {
            "coding": [
                "Write a Python function to find the factorial of a number",
                "Create a simple REST API using Flask",
                "Implement a binary search algorithm",
                "Write a function to reverse a linked list",
                "Create a class for a basic calculator",
                "How do you handle exceptions in Python?",
                "Explain the difference between list and tuple",
                "Write a function to check if a string is palindrome",
                "Create a simple database connection in Python",
                "Implement a sorting algorithm of your choice"
            ],
            "creative_writing": [
                "Write a short story about a time traveler",
                "Create a poem about the ocean",
                "Write a dialogue between two aliens meeting for the first time",
                "Describe a magical forest in vivid detail",
                "Write a letter from the future to the past",
                "Create a character description for a detective story",
                "Write a haiku about technology",
                "Describe the perfect day from a child's perspective",
                "Write a monologue for a superhero",
                "Create a story that starts with 'The door was already open...'"
            ],
            "factual_qa": [
                "What is the capital of Australia?",
                "Explain the process of photosynthesis",
                "Who invented the telephone?",
                "What are the main causes of climate change?",
                "Describe the structure of an atom",
                "What is the largest planet in our solar system?",
                "Who wrote Romeo and Juliet?",
                "What is the chemical formula for water?",
                "In which year did World War II end?",
                "What is the speed of light?"
            ],
            "mathematical_reasoning": [
                "Solve: 2x + 5 = 17",
                "Find the area of a circle with radius 7",
                "Calculate the probability of rolling two sixes with two dice",
                "Explain the Pythagorean theorem with an example",
                "Find the derivative of f(x) = x^2 + 3x + 2",
                "What is 15% of 200?",
                "Solve the system: x + y = 10, x - y = 2",
                "Calculate the compound interest on $1000 at 5% for 3 years",
                "Find the prime factors of 84",
                "What is the sum of angles in a triangle?"
            ],
            "language_translation": [
                "Translate 'Hello, how are you?' to Spanish",
                "Convert 'Good morning' to French",
                "Translate 'Thank you very much' to German",
                "Convert 'I love programming' to Italian",
                "Translate 'The weather is nice today' to Japanese",
                "How do you say 'Happy birthday' in Portuguese?",
                "Translate 'Where is the library?' to Chinese",
                "Convert 'I am hungry' to Russian",
                "Translate 'Beautiful sunset' to Arabic",
                "How do you say 'Good luck' in Dutch?"
            ],
            "sentiment_analysis": [
                "Analyze the sentiment: 'I absolutely love this product!'",
                "What's the sentiment of: 'This movie was terrible'",
                "Classify sentiment: 'The service was okay, nothing special'",
                "Determine sentiment: 'Best day ever! So happy!'",
                "Analyze: 'I'm feeling quite disappointed with the results'",
                "What's the sentiment: 'The food was amazing, will definitely come back!'",
                "Classify: 'Meh, could be better'",
                "Analyze sentiment: 'Worst experience of my life'",
                "Determine sentiment: 'Not bad, but not great either'",
                "What's the sentiment: 'Exceeded all my expectations!'"
            ]
        }
        return sample_prompts
    
    def ensure_directory_exists(self, directory):
        """Create directory if it doesn't exist"""
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def save_prompts_to_file(self, domain, prompts):
        """Save prompts to a JSON file"""
        # Ensure raw_data directory exists
        raw_data_dir = "../raw_data"
        self.ensure_directory_exists(raw_data_dir)
        
        filename = f"{raw_data_dir}/{domain}_prompts.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(prompts)} prompts for {domain} domain")
    
    def generate_initial_dataset(self):
        """Generate initial dataset with sample prompts"""
        sample_prompts = self.load_sample_prompts()
        
        print("Creating initial dataset...")
        for domain, prompts in sample_prompts.items():
            formatted_prompts = []
            for prompt in prompts:
                formatted_prompts.append(self.create_prompt_template(prompt, domain))
            
            self.save_prompts_to_file(domain, formatted_prompts)
        
        print(f"\n✅ Initial dataset created!")
        print(f"📁 Files saved in: dataset/raw_data/")
        print(f"🎯 Current: {len(sample_prompts['coding'])} prompts per domain")
        print(f"🎯 Target: {self.target_prompts_per_domain} prompts per domain")
        
    def show_dataset_status(self):
        """Show current status of dataset"""
        print("\n📊 Dataset Status:")
        print("=" * 40)
        
        raw_data_dir = "../raw_data"
        if not os.path.exists(raw_data_dir):
            print("❌ No dataset files found")
            return
            
        for domain in self.domains:
            filename = f"{raw_data_dir}/{domain}_prompts.json"
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    count = len(data)
                    progress = (count / self.target_prompts_per_domain) * 100
                    print(f"{domain}: {count}/{self.target_prompts_per_domain} prompts ({progress:.1f}%)")
            else:
                print(f"{domain}: 0/{self.target_prompts_per_domain} prompts (0%)")

def main():
    """Main execution function"""
    print("🚀 OrchestrateX Dataset Collection Tool")
    print("=" * 50)
    
    collector = DatasetCollector()
    
    # Show current status
    collector.show_dataset_status()
    
    # Generate initial dataset
    collector.generate_initial_dataset()
    
    # Show updated status
    collector.show_dataset_status()
    
    print("\n📋 Your roadmap as Sahil:")
    print("1. ✅ Create initial dataset structure (DONE)")
    print("2. 🔄 Expand to 500+ prompts per domain (IN PROGRESS)")
    print("3. 🤖 Collect responses from all 5 AI models")
    print("4. 👥 Set up human evaluation system")
    print("5. 📊 Create final structured dataset")
    
    print("\n🎯 Next Steps:")
    print("- Research and collect more prompts from public datasets")
    print("- Add difficulty levels and multilingual prompts")
    print("- Set up API connections to test model responses")

if __name__ == "__main__":
    main()
