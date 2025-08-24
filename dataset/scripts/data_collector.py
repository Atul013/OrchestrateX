"""
Dataset Collection Script for OrchestrateX
Author: Sahil (Part 2 - Dataset Creation & Model Specialty Analysis)

This script helps collect prompts from various sources and organize them by domain.
"""

import json
import csv
import pandas as pd
from typing import Dict, List, Any
import requests
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
        
    def create_prompt_template(self, prompt: str, domain: str) -> Dict[str, Any]:
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
    
    def load_sample_prompts(self) -> Dict[str, List[str]]:
        """Load sample prompts for each domain to get started"""
        sample_prompts = {
            "coding": [
                "Write a Python function to find the factorial of a number",
                "Create a simple REST API using Flask",
                "Implement a binary search algorithm",
                "Write a function to reverse a linked list",
                "Create a class for a basic calculator"
            ],
            "creative_writing": [
                "Write a short story about a time traveler",
                "Create a poem about the ocean",
                "Write a dialogue between two aliens meeting for the first time",
                "Describe a magical forest in vivid detail",
                "Write a letter from the future to the past"
            ],
            "factual_qa": [
                "What is the capital of Australia?",
                "Explain the process of photosynthesis",
                "Who invented the telephone?",
                "What are the main causes of climate change?",
                "Describe the structure of an atom"
            ],
            "mathematical_reasoning": [
                "Solve: 2x + 5 = 17",
                "Find the area of a circle with radius 7",
                "Calculate the probability of rolling two sixes with two dice",
                "Explain the Pythagorean theorem with an example",
                "Find the derivative of f(x) = x^2 + 3x + 2"
            ],
            "language_translation": [
                "Translate 'Hello, how are you?' to Spanish",
                "Convert 'Good morning' to French",
                "Translate 'Thank you very much' to German",
                "Convert 'I love programming' to Italian",
                "Translate 'The weather is nice today' to Japanese"
            ],
            "sentiment_analysis": [
                "Analyze the sentiment: 'I absolutely love this product!'",
                "What's the sentiment of: 'This movie was terrible'",
                "Classify sentiment: 'The service was okay, nothing special'",
                "Determine sentiment: 'Best day ever! So happy!'",
                "Analyze: 'I'm feeling quite disappointed with the results'"
            ]
        }
        return sample_prompts
    
    def save_prompts_to_file(self, domain: str, prompts: List[Dict[str, Any]]):
        """Save prompts to a JSON file"""
        filename = f"../raw_data/{domain}_prompts.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(prompts)} prompts for {domain} domain")
    
    def generate_initial_dataset(self):
        """Generate initial dataset with sample prompts"""
        sample_prompts = self.load_sample_prompts()
        
        for domain, prompts in sample_prompts.items():
            formatted_prompts = []
            for prompt in prompts:
                formatted_prompts.append(self.create_prompt_template(prompt, domain))
            
            self.save_prompts_to_file(domain, formatted_prompts)
        
        print(f"\n✅ Initial dataset created!")
        print(f"📁 Files saved in: dataset/raw_data/")
        print(f"🎯 Next step: Expand each domain to {self.target_prompts_per_domain} prompts")

def main():
    """Main execution function"""
    print("🚀 OrchestrateX Dataset Collection Tool")
    print("=" * 50)
    
    collector = DatasetCollector()
    collector.generate_initial_dataset()
    
    print("\n📋 Your tasks as Sahil:")
    print("1. ✅ Create initial dataset structure (DONE)")
    print("2. 🔄 Expand to 500+ prompts per domain")
    print("3. 🤖 Collect responses from all 5 AI models")
    print("4. 👥 Set up human evaluation system")
    print("5. 📊 Create final structured dataset")

if __name__ == "__main__":
    main()
