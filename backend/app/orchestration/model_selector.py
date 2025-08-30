import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Import the prompt analyzer function
from prompt_analyzer import extract_prompt_features

class ModelSelector:
    """
    Advanced model selection system that trains on prompt features and predicts
    the best AI model for new prompts with confidence scores.
    """
    
    def __init__(self):
        self.mlb_categories = MultiLabelBinarizer()
        self.le_domain = LabelEncoder()
        self.le_intent = LabelEncoder()
        self.le_target = LabelEncoder()
        self.scaler = StandardScaler()
        self.classifier = None
        self.feature_columns = []
        self.model_classes = []
        
    def prepare_features(self, df: pd.DataFrame, fit_transformers=True):
        """
        Convert categorical fields to numerical features suitable for model training.
        
        Args:
            df: DataFrame with columns ['categories', 'topic_domain', 'intent_type', 'confidence', 'token_count']
            fit_transformers: Whether to fit the transformers (True for training, False for prediction)
            
        Returns:
            np.array: Feature matrix ready for training/prediction
        """
        features = []
        
        # 1. Handle categories (multi-label binary encoding)
        categories_lists = df['categories'].apply(lambda x: x if isinstance(x, list) else [x])
        if fit_transformers:
            categories_encoded = self.mlb_categories.fit_transform(categories_lists)
        else:
            categories_encoded = self.mlb_categories.transform(categories_lists)
        
        features.append(categories_encoded)
        
        # 2. Handle topic_domain (label encoding + one-hot)
        if fit_transformers:
            domain_encoded = self.le_domain.fit_transform(df['topic_domain'])
        else:
            domain_encoded = self.le_domain.transform(df['topic_domain'])
        
        # Convert to one-hot
        domain_onehot = np.eye(len(self.le_domain.classes_))[domain_encoded]
        features.append(domain_onehot)
        
        # 3. Handle intent_type (label encoding + one-hot)
        if fit_transformers:
            intent_encoded = self.le_intent.fit_transform(df['intent_type'])
        else:
            intent_encoded = self.le_intent.transform(df['intent_type'])
        
        # Convert to one-hot
        intent_onehot = np.eye(len(self.le_intent.classes_))[intent_encoded]
        features.append(intent_onehot)
        
        # 4. Numerical features
        numerical_features = df[['token_count']].values
        features.append(numerical_features)
        
        # 5. Confidence scores (if available)
        if 'confidence' in df.columns:
            if isinstance(df['confidence'].iloc[0], dict):
                # Extract confidence sub-scores
                conf_overall = df['confidence'].apply(lambda x: x.get('overall', 0)).values.reshape(-1, 1)
                conf_category = df['confidence'].apply(lambda x: x.get('category', 0)).values.reshape(-1, 1)
                conf_domain = df['confidence'].apply(lambda x: x.get('domain', 0)).values.reshape(-1, 1)
                conf_intent = df['confidence'].apply(lambda x: x.get('intent', 0)).values.reshape(-1, 1)
                
                features.extend([conf_overall, conf_category, conf_domain, conf_intent])
            else:
                # Single confidence value
                conf_features = df['confidence'].values.reshape(-1, 1)
                features.append(conf_features)
        
        # 6. Advanced derived features
        # Category diversity (number of categories)
        category_count = df['categories'].apply(len).values.reshape(-1, 1)
        features.append(category_count)
        
        # Combine all features
        X = np.hstack(features)
        
        # Scale features
        if fit_transformers:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        # Store feature column names for interpretation
        if fit_transformers:
            self.feature_columns = (
                [f'cat_{cat}' for cat in self.mlb_categories.classes_] +
                [f'domain_{domain}' for domain in self.le_domain.classes_] +
                [f'intent_{intent}' for intent in self.le_intent.classes_] +
                ['token_count', 'conf_overall', 'conf_category', 'conf_domain', 'conf_intent', 'category_count']
            )
        
        return X_scaled
    
    def train_model_selector(self, df: pd.DataFrame, test_size=0.2, algorithm='logistic'):
        """
        Train model selector classifier from prompt features and best model labels.
        
        Args:
            df: DataFrame with columns including 'best_model' and prompt features
            test_size: Fraction of data to use for testing
            algorithm: 'logistic' or 'random_forest'
            
        Returns:
            dict: Training results including accuracy and classification report
        """
        
        # Prepare features
        X = self.prepare_features(df, fit_transformers=True)
        
        # Encode target variable
        y = self.le_target.fit_transform(df['best_model'])
        self.model_classes = self.le_target.classes_
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Choose and train classifier
        if algorithm == 'logistic':
            self.classifier = LogisticRegression(
                random_state=42, 
                max_iter=1000,
                class_weight='balanced'  # Handle imbalanced data
            )
        elif algorithm == 'random_forest':
            self.classifier = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight='balanced'
            )
        else:
            raise ValueError("Algorithm must be 'logistic' or 'random_forest'")
        
        # Train the model
        self.classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(self.classifier, X_train, y_train, cv=5)
        
        # Classification report
        report = classification_report(
            y_test, y_pred, 
            target_names=self.model_classes,
            output_dict=True
        )
        
        results = {
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': report,
            'feature_importance': self._get_feature_importance()
        }
        
        return results
    
    def _get_feature_importance(self):
        """Get feature importance from trained model."""
        if hasattr(self.classifier, 'feature_importances_'):
            # Random Forest
            importance = self.classifier.feature_importances_
        elif hasattr(self.classifier, 'coef_'):
            # Logistic Regression - use absolute values of coefficients
            importance = np.abs(self.classifier.coef_).mean(axis=0)
        else:
            return None
        
        feature_importance = dict(zip(self.feature_columns, importance))
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
    
    def select_best_model(self, prompt: str):
        """
        Given a prompt string, return predicted best model and confidence scores using trained selector.
        
        Args:
            prompt: Input prompt string
            
        Returns:
            dict: Contains predicted_model, confidence_scores, and prompt_features
        """
        if self.classifier is None:
            raise ValueError("Model not trained yet. Call train_model_selector first.")
        
        # Extract features from prompt
        prompt_features = extract_prompt_features(prompt)
        
        # Convert to DataFrame format expected by prepare_features
        feature_df = pd.DataFrame([{
            'categories': prompt_features['categories'],
            'topic_domain': prompt_features['topic_domain'],
            'intent_type': prompt_features['intent_type'],
            'confidence': prompt_features['confidence'],
            'token_count': prompt_features['token_count']
        }])
        
        # Prepare features for prediction
        X = self.prepare_features(feature_df, fit_transformers=False)
        
        # Get prediction and probabilities
        prediction = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        
        # Convert back to model names
        predicted_model = self.le_target.inverse_transform([prediction])[0]
        
        # Create confidence scores for all models
        confidence_scores = dict(zip(self.model_classes, probabilities))
        
        return {
            'predicted_model': predicted_model,
            'confidence_scores': confidence_scores,
            'prompt_features': prompt_features,
            'prediction_confidence': max(probabilities)
        }
    
    def save_model(self, filepath: str):
        """Save the trained model and preprocessors."""
        model_data = {
            'classifier': self.classifier,
            'mlb_categories': self.mlb_categories,
            'le_domain': self.le_domain,
            'le_intent': self.le_intent,
            'le_target': self.le_target,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'model_classes': self.model_classes
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """Load a previously trained model and preprocessors."""
        model_data = joblib.load(filepath)
        self.classifier = model_data['classifier']
        self.mlb_categories = model_data['mlb_categories']
        self.le_domain = model_data['le_domain']
        self.le_intent = model_data['le_intent']
        self.le_target = model_data['le_target']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.model_classes = model_data['model_classes']


def create_sample_dataset(n_samples=1000):
    """
    Create a sample dataset for demonstration purposes.
    This simulates the structure you would have from real prompt analysis.
    """
    np.random.seed(42)
    
    # Define possible models
    models = ['GLM4.5', 'GPT-OSS', 'Llama 4 Maverick', 'MoonshotAI Kimi', 'Qwen3', 'TNG DeepSeek']
    
    # Sample prompts for different categories
    sample_prompts = [
        # Coding prompts (favor technical models)
        "Write a Python function to sort arrays",
        "Create a REST API using Django",
        "Debug this JavaScript code",
        "Implement a binary search algorithm",
        "Optimize SQL query performance",
        
        # Reasoning prompts (favor analytical models)
        "Explain why renewable energy is sustainable", 
        "Analyze economic implications of remote work",
        "Compare machine learning algorithms",
        "Prove mathematical theorems",
        "Evaluate pros and cons of cryptocurrency",
        
        # General prompts (favor conversational models)
        "Hello, how are you?",
        "Tell me a fun fact about dolphins",
        "What's the weather like?",
        "Help me plan a vacation",
        "Give me cooking advice"
    ]
    
    data = []
    for _ in range(n_samples):
        # Randomly select a prompt and modify it slightly
        base_prompt = np.random.choice(sample_prompts)
        prompt = base_prompt + f" (variation {np.random.randint(1, 100)})"
        
        # Extract features
        features = extract_prompt_features(prompt)
        
        # Simulate best model selection based on prompt characteristics
        best_model = simulate_best_model_selection(features)
        
        data.append({
            'prompt': prompt,
            'categories': features['categories'],
            'topic_domain': features['topic_domain'],
            'intent_type': features['intent_type'],
            'confidence': features['confidence'],
            'token_count': features['token_count'],
            'best_model': best_model
        })
    
    return pd.DataFrame(data)

def simulate_best_model_selection(features):
    """
    Simulate realistic model selection based on prompt features.
    This represents the ground truth you would have from actual model performance data.
    """
    models = ['GLM4.5', 'GPT-OSS', 'Llama 4 Maverick', 'MoonshotAI Kimi', 'Qwen3', 'TNG DeepSeek']
    
    # Define model preferences based on prompt characteristics
    if 'coding' in features['categories']:
        if features['topic_domain'] == 'technical':
            # Technical coding tasks - favor specialized models
            return np.random.choice(['TNG DeepSeek', 'GLM4.5', 'GPT-OSS'], p=[0.4, 0.3, 0.3])
        else:
            # General coding tasks
            return np.random.choice(['GPT-OSS', 'TNG DeepSeek', 'Llama 4 Maverick'], p=[0.4, 0.3, 0.3])
    
    elif 'reasoning' in features['categories']:
        if features['topic_domain'] == 'logical':
            # Analytical reasoning - favor logic-oriented models
            return np.random.choice(['GLM4.5', 'Qwen3', 'GPT-OSS'], p=[0.4, 0.3, 0.3])
        else:
            # General reasoning
            return np.random.choice(['GPT-OSS', 'GLM4.5', 'MoonshotAI Kimi'], p=[0.4, 0.3, 0.3])
    
    else:  # General conversation
        # Conversational tasks - favor general-purpose models
        return np.random.choice(['MoonshotAI Kimi', 'GPT-OSS', 'Llama 4 Maverick'], p=[0.4, 0.3, 0.3])


# Demonstration and testing
if __name__ == "__main__":
    print("=== MODEL SELECTOR TRAINING AND TESTING ===\n")
    
    # 1. Create sample dataset
    print("1. Creating sample dataset...")
    df = create_sample_dataset(n_samples=500)
    print(f"   Dataset created with {len(df)} samples")
    print(f"   Model distribution:")
    print(df['best_model'].value_counts().to_string())
    print()
    
    # 2. Initialize and train model selector
    print("2. Training model selector...")
    selector = ModelSelector()
    
    # Train with logistic regression
    results = selector.train_model_selector(df, algorithm='logistic')
    
    print(f"   Training accuracy: {results['accuracy']:.3f}")
    print(f"   Cross-validation: {results['cv_mean']:.3f} ± {results['cv_std']:.3f}")
    print()
    
    # 3. Show feature importance
    print("3. Feature importance (top 10):")
    importance = results['feature_importance']
    for i, (feature, score) in enumerate(list(importance.items())[:10]):
        print(f"   {i+1:2d}. {feature}: {score:.3f}")
    print()
    
    # 4. Test with new prompts
    print("4. Testing with new prompts:")
    test_prompts = [
        "Write a Python function to implement quicksort",
        "Explain the economic benefits of renewable energy",
        "Hello, can you help me with cooking recipes?",
        "Debug this JavaScript error in my React app",
        "Analyze the logical flaws in this argument",
        "What's the best way to learn machine learning?"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        result = selector.select_best_model(prompt)
        
        print(f"   {i}. \"{prompt}\"")
        print(f"      → Predicted: {result['predicted_model']} (confidence: {result['prediction_confidence']:.3f})")
        
        # Show top 3 model confidences
        top_models = sorted(result['confidence_scores'].items(), key=lambda x: x[1], reverse=True)[:3]
        confidence_str = ", ".join([f"{model}: {conf:.3f}" for model, conf in top_models])
        print(f"      → Top 3: {confidence_str}")
        print()
    
    # 5. Save the trained model
    print("5. Saving trained model...")
    selector.save_model('model_selector.pkl')
    print("   Model saved to 'model_selector.pkl'")
    print("\n=== TRAINING COMPLETE ===")
