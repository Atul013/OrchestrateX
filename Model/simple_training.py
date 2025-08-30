from model_selector import ModelSelector, create_sample_dataset

# Step 1: Create or load dataset
df = create_sample_dataset(n_samples=1000)

# Step 2: Initialize selector and train
selector = ModelSelector()
results = selector.train_model_selector(df, algorithm='logistic')

# Step 3: Print results
print(f"Training accuracy: {results['accuracy']:.3f}")
print(f"Cross-validation: {results['cv_mean']:.3f} ± {results['cv_std']:.3f}")

# Step 4: Feature importance
print("Top 10 feature importances:")
for feature, score in list(results['feature_importance'].items())[:10]:
    print(f"{feature}: {score:.3f}")

# Step 5: Save trained model
selector.save_model('model_selector.pkl')
print("Trained model saved as 'model_selector.pkl'")
