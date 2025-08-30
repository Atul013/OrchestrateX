# AI Model Selector System

A comprehensive machine learning system that analyzes user prompts and predicts the best AI model to handle each request, with confidence scores for all available models.

## 🚀 **System Overview**

The AI Model Selector combines advanced prompt analysis with machine learning to intelligently route user requests to the most suitable AI model. It consists of two main components:

1. **Prompt Analyzer** (`prompt_analyzer.py`) - Extracts sophisticated features from user prompts
2. **Model Selector** (`model_selector.py`) - Trains and applies ML classifiers for model prediction

## 📊 **Architecture**

```
User Prompt → Feature Extraction → ML Classifier → Best Model + Confidence Scores
```

### **Feature Extraction Pipeline**
- **Categories**: Multi-label classification (coding, reasoning, general)
- **Domain**: Topic classification (technical, logical, casual)
- **Intent**: Purpose detection (question, instruction, code_request, reasoning_task)
- **Confidence**: Multi-dimensional confidence scoring
- **Token Analysis**: Advanced tokenization and n-gram processing

### **Machine Learning Pipeline**
- **Feature Engineering**: Categorical encoding, scaling, derived features
- **Algorithms**: Logistic Regression, Random Forest (configurable)
- **Cross-validation**: 5-fold CV for robust evaluation
- **Class Balance**: Handles imbalanced datasets with weighted classes

## 🛠 **Installation & Setup**

### **Prerequisites**
```bash
pip install scikit-learn pandas numpy joblib
```

### **Files Structure**
```
OrchestrateX/
├── Algorithm/
│   └── prompt_analyzer.py      # Advanced prompt feature extraction
├── model_selector.py           # ML training and prediction system
├── model_selector_demo.py      # Usage demonstration
└── model_selector.pkl          # Trained model (generated after training)
```

## 📝 **Usage Examples**

### **1. Training a New Model**

```python
from model_selector import ModelSelector, create_sample_dataset
import pandas as pd

# Create or load your dataset
# Required columns: 'categories', 'topic_domain', 'intent_type', 'confidence', 'token_count', 'best_model'
df = create_sample_dataset(n_samples=1000)  # Or load your real data

# Initialize and train
selector = ModelSelector()
results = selector.train_model_selector(df, algorithm='logistic')

print(f"Training accuracy: {results['accuracy']:.3f}")
print(f"Cross-validation: {results['cv_mean']:.3f} ± {results['cv_std']:.3f}")

# Save the trained model
selector.save_model('my_model_selector.pkl')
```

### **2. Using a Trained Model**

```python
from model_selector import ModelSelector

# Load pre-trained model
selector = ModelSelector()
selector.load_model('model_selector.pkl')

# Predict best model for a new prompt
result = selector.select_best_model("Write a Python function to sort arrays")

print(f"Best Model: {result['predicted_model']}")
print(f"Confidence: {result['prediction_confidence']:.3f}")
print(f"All Models: {result['confidence_scores']}")
```

### **3. Simplified Single Prediction**

```python
from model_selector_demo import predict_single_prompt

# Quick prediction function
result = predict_single_prompt("Explain quantum physics concepts")
print(f"Recommended model: {result['predicted_model']}")
```

## 🎯 **Model Performance**

### **Training Results** (500 samples)
- **Accuracy**: 26.0% (6-class classification baseline ~16.7%)
- **Cross-validation**: 36.5% ± 2.2%
- **Feature Importance**: Domain and category features most predictive

### **Feature Importance Rankings**
1. **domain_casual** (0.457) - Casual conversation detection
2. **cat_general** (0.413) - General category classification  
3. **domain_logical** (0.408) - Logical reasoning detection
4. **conf_category** (0.388) - Category confidence scores
5. **category_count** (0.387) - Number of categories detected

## 🤖 **Available Models**

The system currently supports 6 AI models:

| Model | Best For | Example Use Cases |
|-------|----------|-------------------|
| **TNG DeepSeek** | Technical coding tasks | API development, algorithm implementation |
| **GLM4.5** | Analytical reasoning | Mathematical proofs, logical analysis |
| **GPT-OSS** | General purpose | Mixed coding+reasoning tasks |
| **MoonshotAI Kimi** | Conversational tasks | Advice, recommendations, discussions |
| **Llama 4 Maverick** | General conversation | Entertainment, casual questions |
| **Qwen3** | Specialized reasoning | Economic analysis, scientific explanations |

## 📊 **Prediction Examples**

| Prompt | Predicted Model | Confidence | Reasoning |
|--------|----------------|------------|-----------|
| "Write a Python function to implement quicksort" | TNG DeepSeek | 0.456 | Technical coding task |
| "Explain economic benefits of renewable energy" | Qwen3 | 0.647 | Analytical reasoning |
| "Hello, can you help with cooking recipes?" | Llama 4 Maverick | 0.376 | Casual conversation |
| "Debug JavaScript error in React app" | TNG DeepSeek | 0.591 | Technical debugging |

## 🔧 **Advanced Configuration**

### **Custom Feature Engineering**

```python
class CustomModelSelector(ModelSelector):
    def prepare_features(self, df, fit_transformers=True):
        # Add custom features
        X = super().prepare_features(df, fit_transformers)
        
        # Add your custom features here
        custom_features = df['custom_column'].values.reshape(-1, 1)
        X = np.hstack([X, custom_features])
        
        return X
```

### **Algorithm Selection**

```python
# Use Random Forest instead of Logistic Regression
results = selector.train_model_selector(df, algorithm='random_forest')

# Access feature importance for Random Forest
if hasattr(selector.classifier, 'feature_importances_'):
    print("Feature importances:", selector.classifier.feature_importances_)
```

### **Custom Model Classes**

```python
# Define your own model set
models = ['GPT-4', 'Claude-3', 'Gemini-Pro', 'Custom-Model']

# Update the simulation function in create_sample_dataset()
def simulate_best_model_selection(features):
    # Your custom logic here
    if 'coding' in features['categories']:
        return 'GPT-4'  # Your preference
    # ... more logic
```

## 📈 **Data Requirements**

### **Training Dataset Format**

Your DataFrame should contain these columns:

```python
{
    'prompt': str,           # Original user prompt
    'categories': list,      # ['coding', 'reasoning'] etc.
    'topic_domain': str,     # 'technical', 'logical', 'casual'
    'intent_type': str,      # 'question', 'instruction', etc.
    'confidence': dict,      # {'overall': 0.8, 'category': 0.7, ...}
    'token_count': int,      # Number of tokens
    'best_model': str        # Ground truth best model
}
```

### **Feature Extraction**

The `extract_prompt_features()` function automatically generates all required features from raw prompts:

```python
from Algorithm.prompt_analyzer import extract_prompt_features

features = extract_prompt_features("Your prompt here")
# Returns all required columns for training
```

## 🧪 **Testing & Validation**

### **Model Evaluation**

```python
# Get detailed classification report
results = selector.train_model_selector(df)
report = results['classification_report']

for model_name, metrics in report.items():
    if isinstance(metrics, dict):
        print(f"{model_name}: Precision={metrics['precision']:.3f}, "
              f"Recall={metrics['recall']:.3f}, F1={metrics['f1-score']:.3f}")
```

### **Cross-Validation**

```python
from sklearn.model_selection import cross_val_score

# Custom cross-validation
scores = cross_val_score(selector.classifier, X, y, cv=10)
print(f"10-fold CV: {scores.mean():.3f} ± {scores.std():.3f}")
```

## 🚀 **Production Deployment**

### **API Integration**

```python
from flask import Flask, request, jsonify
from model_selector import ModelSelector

app = Flask(__name__)
selector = ModelSelector()
selector.load_model('production_model.pkl')

@app.route('/predict', methods=['POST'])
def predict_model():
    prompt = request.json['prompt']
    result = selector.select_best_model(prompt)
    
    return jsonify({
        'best_model': result['predicted_model'],
        'confidence': result['prediction_confidence'],
        'all_models': result['confidence_scores']
    })
```

### **Batch Prediction**

```python
def predict_batch(prompts):
    """Predict best models for multiple prompts efficiently."""
    results = []
    for prompt in prompts:
        result = selector.select_best_model(prompt)
        results.append({
            'prompt': prompt,
            'model': result['predicted_model'],
            'confidence': result['prediction_confidence']
        })
    return results
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Import Error**: Ensure `prompt_analyzer.py` is in the correct path
2. **Low Accuracy**: Increase training data size or improve feature engineering
3. **Memory Issues**: Reduce dataset size or use incremental learning
4. **Class Imbalance**: Use `class_weight='balanced'` in classifier

### **Performance Optimization**

```python
# For large datasets, use SGD classifier
from sklearn.linear_model import SGDClassifier

selector.classifier = SGDClassifier(
    loss='log',  # For probability estimates
    class_weight='balanced',
    random_state=42
)
```

## 📚 **References**

- **Prompt Analysis**: Multi-tier keyword classification with contextual scoring
- **Feature Engineering**: Categorical encoding, normalization, derived features  
- **Machine Learning**: Scikit-learn LogisticRegression and RandomForest
- **Evaluation**: Cross-validation, classification reports, feature importance

---

**Built for OrchestrateX AI Model Orchestration System** 🎯
