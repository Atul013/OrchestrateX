#!/usr/bin/env python3
"""
Khan Academy Math Prompts - Collected by Sahil from Khan Academy Algebra Foundations
10 high-quality prompts from Quiz 1 and Quiz 2
"""

import json
import os
from datetime import datetime

def add_khan_academy_prompts():
    """Add 10 Khan Academy algebra foundation prompts"""
    
    # Khan Academy prompts collected by Sahil
    khan_prompts = [
        {
            "prompt": "Simplify to create an equivalent expression: 8k - 5(-5k + 3)",
            "difficulty": "medium",
            "category": "algebraic_simplification",
            "source": "Khan Academy Quiz 2"
        },
        {
            "prompt": "Combine like terms to create an equivalent expression: 7.4z - 5(-1.6z + 2.4)",
            "difficulty": "medium",
            "category": "combining_like_terms", 
            "source": "Khan Academy Quiz 2"
        },
        {
            "prompt": "Which expressions are equivalent to 4d + 6 + 2d?",
            "difficulty": "medium",
            "category": "equivalent_expressions",
            "source": "Khan Academy Quiz 2"
        },
        {
            "prompt": "Combine like terms to create an equivalent expression: 1.3b + 7.8 - 3.2b",
            "difficulty": "medium",
            "category": "combining_like_terms",
            "source": "Khan Academy Quiz 2"
        },
        {
            "prompt": "Simplify to create an equivalent expression: 6(7 - 3y) + 6(y + 1)",
            "difficulty": "medium",
            "category": "distributive_property",
            "source": "Khan Academy Quiz 2"
        },
        {
            "prompt": "Evaluate ab - 0.5b when a = 1 and b = 5",
            "difficulty": "medium",
            "category": "variable_evaluation",
            "source": "Khan Academy Quiz 1"
        },
        {
            "prompt": "Evaluate 4 - 0.25g + 0.5h when g = 10 and h = 5",
            "difficulty": "medium",
            "category": "variable_evaluation",
            "source": "Khan Academy Quiz 1"
        },
        {
            "prompt": "Evaluate e - (1/2)f when e = 15 and f = 2",
            "difficulty": "medium",
            "category": "variable_evaluation",
            "source": "Khan Academy Quiz 1"
        },
        {
            "prompt": "Evaluate 0.3y + (y/z) when y = 10 and z = 5",
            "difficulty": "hard",
            "category": "variable_evaluation",
            "source": "Khan Academy Quiz 1"
        },
        {
            "prompt": "Evaluate 8p + 3q - 18 when p = 1/2 and q = 7",
            "difficulty": "medium",
            "category": "variable_evaluation",
            "source": "Khan Academy Quiz 1"
        }
    ]
    
    # Load existing mathematical reasoning data
    math_file = "../raw_data/mathematical_reasoning.json"
    
    try:
        with open(math_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    
    # Add new prompts with proper structure
    current_time = datetime.now().isoformat()
    next_id = len(existing_data) + 1
    
    for prompt_data in khan_prompts:
        new_prompt = {
            "id": next_id,
            "prompt": prompt_data["prompt"],
            "domain": "mathematical_reasoning",
            "difficulty": prompt_data["difficulty"],
            "category": prompt_data["category"],
            "language": "en",
            "created_at": current_time,
            "source": prompt_data["source"],
            "chatbot_responses": {},
            "ratings": {},
            "metadata": {
                "collector": "Sahil",
                "collection_method": "Khan Academy screenshots",
                "quality_checked": True,
                "khan_academy_topic": "Algebra Foundations"
            }
        }
        existing_data.append(new_prompt)
        next_id += 1
    
    # Save updated data
    with open(math_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Added {len(khan_prompts)} Khan Academy prompts!")
    print(f"📊 Total mathematical reasoning prompts: {len(existing_data)}")
    print(f"📚 Categories added:")
    categories = {}
    for prompt in khan_prompts:
        cat = prompt["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"   - {cat}: {count} prompts")
    
    return len(existing_data)

if __name__ == "__main__":
    print("🎯 Adding Khan Academy Math Prompts")
    print("=" * 50)
    total = add_khan_academy_prompts()
    print(f"\n🎉 Success! Mathematical reasoning now has {total} prompts")
    print("📈 Progress update: From 31 → 41 prompts (8.2% complete)")
