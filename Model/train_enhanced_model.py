#!/usr/bin/env python3
"""
Enhanced Model Trainer with 5000 samples
Trains on realistic dataset for better ML fallback
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def train_enhanced_model():
    """Train model on the enhanced 5000-sample dataset."""
    
    print("🔥 Training Enhanced Model Selector...")
    
    # Load the enhanced dataset
    try:
        df = pd.read_csv('enhanced_dataset_5000.csv')
        print(f"✅ Loaded {len(df)} samples from enhanced dataset")
    except FileNotFoundError:
        print("❌ Enhanced dataset not found. Run create_enhanced_dataset.py first.")
        return
    
    # Prepare features
    print("🔧 Preparing features...")
    
    # Handle categories (convert string representation back to list)
    df['categories'] = df['categories'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    
    # Handle confidence (extract overall score from dict string)
    def extract_confidence(conf_str):
        try:
            if isinstance(conf_str, str):
                conf_dict = eval(conf_str)
                return conf_dict.get('overall', 0.5)
            return float(conf_str) if conf_str else 0.5
        except:
            return 0.5
    
    df['confidence_score'] = df['confidence'].apply(extract_confidence)
    
    # Create feature matrix
    mlb = MultiLabelBinarizer()
    categories_encoded = mlb.fit_transform(df['categories'])
    
    # Create additional features
    feature_matrix = []
    for idx, row in df.iterrows():
        features = list(categories_encoded[idx])  # Category features
        
        # Add numerical features
        features.extend([
            1 if row['topic_domain'] == 'technical' else 0,
            1 if row['topic_domain'] == 'creative' else 0,
            1 if row['topic_domain'] == 'academic' else 0,
            1 if row['intent_type'] == 'question' else 0,
            1 if row['intent_type'] == 'task' else 0,
            1 if row['intent_type'] == 'creative' else 0,
            1 if row['intent_type'] == 'code_request' else 0,
            row['confidence_score'],
            row['token_count'],
            len(row['prompt']),  # Character count
            row['prompt'].lower().count('python'),  # Python mentions
            row['prompt'].lower().count('analyze'),  # Analysis keywords
            row['prompt'].lower().count('create'),  # Creative keywords
        ])
        
        feature_matrix.append(features)
    
    X = np.array(feature_matrix)
    y = df['best_model'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Training set: {len(X_train)} samples")
    print(f"📊 Test set: {len(X_test)} samples")
    print(f"📊 Features: {X.shape[1]} dimensions")
    
    # Try different models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=200, 
            max_depth=15, 
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        ),
        'Logistic Regression': LogisticRegression(
            random_state=42, 
            max_iter=1000,
            C=1.0
        )
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    for name, model in models.items():
        print(f"\n🧠 Training {name}...")
        
        # Create pipeline with scaling
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ {name} Accuracy: {accuracy:.1%}")
        
        if accuracy > best_score:
            best_score = accuracy
            best_model = pipeline
            best_name = name
    
    print(f"\n🏆 Best Model: {best_name} ({best_score:.1%})")
    
    # Detailed evaluation of best model
    print(f"\n📋 Detailed Results for {best_name}:")
    y_pred_best = best_model.predict(X_test)
    
    print("\n🎯 Classification Report:")
    print(classification_report(y_test, y_pred_best))
    
    print("\n📊 Model Distribution in Test Set:")
    unique, counts = np.unique(y_test, return_counts=True)
    for model_name, count in zip(unique, counts):
        print(f"  {model_name}: {count} samples")
    
    # Save the best model
    joblib.dump(best_model, 'enhanced_model_selector.pkl')
    print(f"\n💾 Saved enhanced model to 'enhanced_model_selector.pkl'")
    
    # Test with sample prompts
    print(f"\n🧪 Testing with sample prompts:")
    test_prompts = [
        "Write a Python function for machine learning",
        "Analyze the economic impact of AI", 
        "Create a creative marketing campaign",
        "Design a secure authentication system",
        "Explain quantum physics simply"
    ]
    
    for prompt in test_prompts:
        # Create simple features for testing (simplified version)
        simple_features = np.zeros(X.shape[1])
        simple_features[0] = 1  # General category
        simple_features[-9] = 0.7  # Confidence
        simple_features[-8] = len(prompt.split())  # Token count
        simple_features[-7] = len(prompt)  # Char count
        simple_features[-6] = prompt.lower().count('python')
        simple_features[-5] = prompt.lower().count('analyze')
        simple_features[-4] = prompt.lower().count('create')
        
        prediction = best_model.predict([simple_features])[0]
        probability = max(best_model.predict_proba([simple_features])[0])
        
        print(f"  '{prompt[:50]}...' -> {prediction} ({probability:.1%})")
    
    return best_model, best_score

if __name__ == "__main__":
    model, score = train_enhanced_model()
    print(f"\n🎉 Training complete! Final accuracy: {score:.1%}")
