#!/usr/bin/env python3
"""
Show what the training dataset looks like and where it comes from.
"""

from model_selector import create_sample_dataset
import pandas as pd

def inspect_dataset():
    print("🔍 DATASET INSPECTION")
    print("=" * 50)
    
    # Create a small sample to inspect
    print("Creating sample dataset...")
    df = create_sample_dataset(n_samples=10)  # Small sample for inspection
    
    print(f"\n📊 Dataset shape: {df.shape}")
    print(f"📝 Columns: {list(df.columns)}")
    
    print("\n🎯 SAMPLE DATA (first 5 rows):")
    print("=" * 80)
    
    for i, row in df.head().iterrows():
        print(f"\n{i+1}. Prompt: '{row['prompt']}'")
        print(f"   Categories: {row['categories']}")
        print(f"   Domain: {row['topic_domain']} | Intent: {row['intent_type']}")
        print(f"   Tokens: {row['token_count']} | Best Model: {row['best_model']}")
        print(f"   Confidence: Overall={row['confidence']['overall']:.3f}")
    
    print("\n📈 MODEL DISTRIBUTION:")
    print(df['best_model'].value_counts().to_string())
    
    print("\n🎨 CATEGORY DISTRIBUTION:")
    all_categories = []
    for cats in df['categories']:
        all_categories.extend(cats)
    from collections import Counter
    cat_counts = Counter(all_categories)
    for cat, count in cat_counts.items():
        print(f"   {cat}: {count}")
    
    print("\n🎯 DOMAIN DISTRIBUTION:")
    print(df['topic_domain'].value_counts().to_string())
    
    print("\n💡 INTENT DISTRIBUTION:")
    print(df['intent_type'].value_counts().to_string())
    
    print("\n" + "=" * 80)
    print("📝 IMPORTANT: This is SIMULATED data, not real user data!")
    print("🎯 In production, you would use:")
    print("   - Real user prompts")
    print("   - Actual model performance results")
    print("   - A/B testing data")
    print("   - User satisfaction ratings")

if __name__ == "__main__":
    inspect_dataset()
