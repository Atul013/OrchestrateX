"""
Simple Expansion Guide for OrchestrateX Dataset
Author: Sahil (Part 2 - Dataset Creation & Model Specialty Analysis)
"""

import json
import os

class SimpleExpansionGuide:
    """Simple tool to create expansion guides for each domain"""
    
    def __init__(self):
        self.domains_info = {
            "coding": {
                "current_target": 500,
                "categories": [
                    "Python basics", "JavaScript fundamentals", "Data structures",
                    "Algorithms", "Web development", "Database queries", "API development",
                    "Debugging", "Testing", "Code optimization", "Object-oriented programming"
                ],
                "sample_prompts": [
                    "Write a Python function to find the largest number in a list",
                    "Create a JavaScript function to validate email addresses",
                    "Implement bubble sort algorithm in any language",
                    "How do you connect to a MySQL database in Python?",
                    "Write a REST API endpoint to get user information",
                    "Debug this code that's not working properly",
                    "Create unit tests for a calculator function",
                    "Optimize this SQL query for better performance"
                ]
            },
            "creative_writing": {
                "current_target": 500,
                "categories": [
                    "Short stories", "Poetry", "Character descriptions", "Dialogue writing",
                    "Scene descriptions", "Plot development", "Fantasy writing", "Sci-fi concepts",
                    "Mystery plots", "Romance scenes", "Horror elements", "Comedy writing"
                ],
                "sample_prompts": [
                    "Write a short story about a robot learning to feel emotions",
                    "Create a poem about the changing seasons",
                    "Describe a mysterious character who appears at midnight",
                    "Write dialogue between a detective and a suspect",
                    "Describe a futuristic city in detail",
                    "Create a plot twist for a mystery story",
                    "Write a romantic scene in a coffee shop",
                    "Describe a haunted house from the ghost's perspective"
                ]
            },
            "factual_qa": {
                "current_target": 500,
                "categories": [
                    "Geography", "History", "Science", "Technology", "Literature",
                    "Current events", "Health", "Environment", "Politics", "Economics",
                    "Arts and culture", "Sports"
                ],
                "sample_prompts": [
                    "What is the capital of New Zealand?",
                    "Explain how photosynthesis works",
                    "Who invented the internet and when?",
                    "What are the main causes of global warming?",
                    "Describe the water cycle process",
                    "What happened during the French Revolution?",
                    "How do vaccines work in the human body?",
                    "What is artificial intelligence and how is it used today?"
                ]
            },
            "mathematical_reasoning": {
                "current_target": 500,
                "categories": [
                    "Basic arithmetic", "Algebra", "Geometry", "Statistics", "Probability",
                    "Calculus", "Word problems", "Logic puzzles", "Mathematical proofs",
                    "Number theory", "Trigonometry", "Financial mathematics"
                ],
                "sample_prompts": [
                    "Solve for x: 3x + 7 = 22",
                    "Find the area of a triangle with base 8 and height 6",
                    "What is the probability of getting heads twice in a row?",
                    "Calculate compound interest on $1000 at 5% for 3 years",
                    "Find the derivative of f(x) = 2x² + 3x - 1",
                    "If a train travels 60 mph for 2.5 hours, how far does it go?",
                    "Prove that the sum of angles in a triangle is 180 degrees",
                    "What is the square root of 144?"
                ]
            },
            "language_translation": {
                "current_target": 500,
                "categories": [
                    "Basic phrases", "Conversational", "Business language", "Academic text",
                    "Technical terms", "Cultural expressions", "Formal writing", "Informal chat",
                    "Poetry translation", "Legal documents", "Medical terms", "Travel phrases"
                ],
                "sample_prompts": [
                    "Translate 'Good morning, how are you?' to Spanish",
                    "How do you say 'Thank you very much' in French?",
                    "Translate 'I would like to make a reservation' to German",
                    "Convert 'The meeting is scheduled for tomorrow' to Italian",
                    "Translate this medical term: 'hypertension' to Portuguese",
                    "How do you say 'Happy birthday' in Japanese?",
                    "Translate 'Please help me' to Arabic",
                    "Convert 'I love this city' to Chinese"
                ]
            },
            "sentiment_analysis": {
                "current_target": 500,
                "categories": [
                    "Product reviews", "Movie reviews", "Social media posts", "Customer feedback",
                    "News comments", "Personal expressions", "Business emails", "Survey responses",
                    "Forum discussions", "App store reviews", "Restaurant reviews", "Book reviews"
                ],
                "sample_prompts": [
                    "Analyze sentiment: 'This product exceeded my expectations!'",
                    "What's the sentiment: 'The movie was okay, nothing special'",
                    "Classify: 'Worst customer service I've ever experienced'",
                    "Determine sentiment: 'Love the new update, so much better!'",
                    "Analyze: 'The food was good but the service was slow'",
                    "What sentiment: 'Meh, could be better I guess'",
                    "Classify: 'Absolutely fantastic! Highly recommend!'",
                    "Determine: 'Not sure if I like this or not'"
                ]
            }
        }
    
    def get_current_count(self, domain):
        """Get current prompt count for domain"""
        filename = f"../raw_data/{domain}_prompts.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return len(data)
        return 0
    
    def create_expansion_plan(self, domain):
        """Create expansion plan for a domain"""
        domain_info = self.domains_info.get(domain, {})
        current_count = self.get_current_count(domain)
        target = domain_info.get("current_target", 500)
        remaining = target - current_count
        
        plan = {
            "domain": domain,
            "current_prompts": current_count,
            "target_prompts": target,
            "remaining_needed": remaining,
            "progress_percentage": round((current_count / target) * 100, 1),
            "categories": domain_info.get("categories", []),
            "sample_prompts": domain_info.get("sample_prompts", []),
            "expansion_strategy": [
                f"Create {remaining // len(domain_info.get('categories', [1]))} prompts per category",
                "Include different difficulty levels (easy, medium, hard)",
                "Add variety in question types and formats",
                "Consider multilingual examples where applicable",
                "Focus on real-world applications and use cases"
            ],
            "data_sources": self.get_data_sources(domain),
            "next_steps": [
                "1. Review the sample prompts and categories",
                "2. Research the recommended data sources",
                "3. Create prompts for each category systematically",
                "4. Ensure variety in difficulty and format",
                "5. Test prompts with different AI models"
            ]
        }
        
        return plan
    
    def get_data_sources(self, domain):
        """Get data source recommendations"""
        sources = {
            "coding": [
                "LeetCode problems",
                "HackerRank challenges", 
                "Stack Overflow questions",
                "GitHub repositories",
                "Programming tutorials",
                "Code review examples"
            ],
            "creative_writing": [
                "r/WritingPrompts",
                "Creative writing courses",
                "Literature examples",
                "Writing contest prompts",
                "Author interviews",
                "Creative writing books"
            ],
            "factual_qa": [
                "Wikipedia articles",
                "Educational websites",
                "News articles",
                "Textbooks",
                "Encyclopedia entries",
                "Academic papers"
            ],
            "mathematical_reasoning": [
                "Khan Academy problems",
                "Math textbooks",
                "Online math courses",
                "Math competition problems",
                "Educational worksheets",
                "Academic exercises"
            ],
            "language_translation": [
                "Google Translate examples",
                "Language learning apps",
                "Bilingual dictionaries",
                "Language courses",
                "Cultural websites",
                "Travel phrasebooks"
            ],
            "sentiment_analysis": [
                "Amazon reviews",
                "Yelp reviews",
                "IMDb reviews",
                "Social media posts",
                "Customer feedback",
                "Survey responses"
            ]
        }
        return sources.get(domain, [])
    
    def save_plan(self, domain):
        """Save expansion plan to file"""
        plan = self.create_expansion_plan(domain)
        
        # Ensure directory exists
        os.makedirs("../processed_data", exist_ok=True)
        
        filename = f"../processed_data/{domain}_expansion_plan.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        return plan
    
    def generate_all_plans(self):
        """Generate expansion plans for all domains"""
        print("🎯 Creating Expansion Plans for All Domains")
        print("=" * 50)
        
        total_current = 0
        total_target = 0
        
        for domain in self.domains_info.keys():
            plan = self.save_plan(domain)
            
            total_current += plan["current_prompts"]
            total_target += plan["target_prompts"]
            
            print(f"\n📁 {domain.upper().replace('_', ' ')}:")
            print(f"   Progress: {plan['current_prompts']}/{plan['target_prompts']} ({plan['progress_percentage']}%)")
            print(f"   Remaining: {plan['remaining_needed']} prompts needed")
            print(f"   Categories: {len(plan['categories'])}")
        
        overall_progress = round((total_current / total_target) * 100, 1)
        print(f"\n📊 OVERALL PROGRESS: {total_current}/{total_target} ({overall_progress}%)")
        print(f"\n✅ All expansion plans saved to: dataset/processed_data/")
        
        return {
            "total_current": total_current,
            "total_target": total_target,
            "overall_progress": overall_progress
        }

def main():
    """Main function"""
    print("🚀 OrchestrateX Dataset Expansion Guide")
    print("=" * 50)
    
    guide = SimpleExpansionGuide()
    summary = guide.generate_all_plans()
    
    print(f"\n📋 WHAT YOU NEED TO DO NEXT, SAHIL:")
    print("=" * 50)
    print("1. ✅ Check the expansion plans in dataset/processed_data/")
    print("2. 📚 Research the recommended data sources for each domain")
    print("3. 📝 Start creating prompts using the categories as guidance")
    print("4. 🎯 Aim for variety: different difficulties, formats, and styles")
    print("5. 🔄 Work domain by domain to reach 500 prompts each")
    print("6. 🤖 Once you have enough prompts, start testing with AI models")
    
    print(f"\n💡 TIP: Start with the domain you're most comfortable with!")
    print(f"📈 Current progress: {summary['overall_progress']}% complete")

if __name__ == "__main__":
    main()
