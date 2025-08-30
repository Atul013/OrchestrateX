#!/usr/bin/env python3
"""
Model Selector Training Script
Creates a dataset, trains the model selector, and saves the trained model.
"""

from model_selector import ModelSelector, create_sample_dataset

def main():
    print("=== MODEL SELECTOR TRAINING ===\n")
    
    # Step 1: Create or load dataset
    print("Step 1: Creating simulated dataset...")
    df = create_sample_dataset(n_samples=1000)
    print(f"Dataset created with {len(df)} samples")
    print(f"Model distribution:")
    print(df['best_model'].value_counts().to_string())
    print()

    # Step 2: Initialize selector and train
    print("Step 2: Initializing ModelSelector and training...")
    selector = ModelSelector()
    results = selector.train_model_selector(df, algorithm='logistic')
    print("Training completed!")
    print()

    # Step 3: Print results
    print("Step 3: Training Results:")
    print(f"Training accuracy: {results['accuracy']:.3f}")
    print(f"Cross-validation: {results['cv_mean']:.3f} ± {results['cv_std']:.3f}")
    print()

    # Step 4: Feature importance
    print("Step 4: Top 10 Feature Importances:")
    for i, (feature, score) in enumerate(list(results['feature_importance'].items())[:10], 1):
        print(f"{i:2d}. {feature}: {score:.3f}")
    print()

    # Step 5: Save trained model
    print("Step 5: Saving trained model...")
    selector.save_model('model_selector.pkl')
    print("✅ Trained model saved as 'model_selector.pkl'")
    print()
    
    print("=== TRAINING COMPLETE ===")
    
    # Bonus: Quick test of the saved model
    print("\nBonus: Testing saved model...")
    test_selector = ModelSelector()
    test_selector.load_model('model_selector.pkl')
    
    test_prompt = "Write a Python function to implement binary search"
    result = test_selector.select_best_model(test_prompt)
    print(f"Test prompt: '{test_prompt}'")
    print(f"Predicted model: {result['predicted_model']} (confidence: {result['prediction_confidence']:.3f})")

if __name__ == "__main__":
    main()
