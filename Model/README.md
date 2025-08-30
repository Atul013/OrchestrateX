# Model Directory - AI Model Management & Selection

This directory contains all AI model-related components for the OrchestrateX system, including individual model testing, intelligent prompt analysis, and ML-based model selection.

## 📁 **Directory Structure**

```
Model/
├── Individual Model Tests
│   ├── Deepseek_test.py           # TNG DeepSeek model testing
│   ├── GLM45_test.py              # GLM4.5 model testing  
│   ├── GPTOSS_test.py             # GPT-OSS model testing
│   ├── Kimi_test.py               # MoonshotAI Kimi model testing
│   ├── Llama4_test.py             # Llama 4 Maverick model testing
│   └── Qwen_test.py               # Qwen3 model testing
│
├── Model Configuration
│   └── Model_parameters.csv       # Model specifications and parameters
│
├── Intelligent Model Selection
│   ├── prompt_analyzer.py         # Advanced prompt feature extraction
│   ├── model_selector.py          # ML-based model selection system
│   ├── model_selector_demo.py     # Usage examples and demonstrations
│   ├── model_selector.pkl         # Trained ML model (auto-generated)
│   └── MODEL_SELECTOR_GUIDE.md    # Comprehensive system documentation
│
└── README.md                      # This file
```

## 🚀 **Quick Start**

### **1. Test Individual Models**
```bash
# Test a specific model
python Deepseek_test.py
python GLM45_test.py
python Kimi_test.py
# ... etc
```

### **2. Use Intelligent Model Selection**
```bash
# Train and test the model selector
python model_selector.py

# Run interactive demonstrations
python model_selector_demo.py
```

### **3. Integrate into Your Application**
```python
from model_selector import ModelSelector

# Load pre-trained selector
selector = ModelSelector()
selector.load_model('model_selector.pkl')

# Get best model for any prompt
result = selector.select_best_model("Write a Python function to sort arrays")
print(f"Best model: {result['predicted_model']}")
print(f"Confidence: {result['prediction_confidence']:.3f}")
```

## 🎯 **Available AI Models**

| Model | Provider | Specialization | Use Cases |
|-------|----------|----------------|-----------|
| **TNG DeepSeek** | DeepSeek | Technical Coding | API development, algorithms, debugging |
| **GLM4.5** | Zhipu AI | Analytical Reasoning | Mathematical proofs, logical analysis |
| **GPT-OSS** | OpenRouter | General Purpose | Mixed coding+reasoning, versatile tasks |
| **MoonshotAI Kimi** | Moonshot AI | Conversational | Advice, recommendations, discussions |
| **Llama 4 Maverick** | Meta | General Conversation | Entertainment, casual questions |
| **Qwen3** | Alibaba | Specialized Reasoning | Economic analysis, scientific explanations |

## 🧠 **Intelligent Model Selection System**

### **How It Works**
1. **Prompt Analysis**: Extracts 15+ sophisticated features from user prompts
2. **Feature Engineering**: Converts categorical data to numerical features
3. **ML Classification**: Uses trained models to predict best AI model
4. **Confidence Scoring**: Provides confidence scores for all available models

### **Feature Categories**
- **Categories**: Coding, Reasoning, General (multi-label)
- **Domain**: Technical, Logical, Casual
- **Intent**: Question, Instruction, Code Request, Reasoning Task
- **Confidence**: Multi-dimensional confidence metrics
- **Token Analysis**: Advanced tokenization and n-gram processing

### **Performance Metrics**
- **Training Accuracy**: 26.0% (vs 16.7% random baseline)
- **Cross-Validation**: 36.5% ± 2.2%
- **Feature Importance**: Domain and category features most predictive

## 🔧 **Usage Examples**

### **Quick Model Prediction**
```python
from model_selector_demo import predict_single_prompt

# Simple prediction
result = predict_single_prompt("Debug this JavaScript error")
print(f"Recommended: {result['predicted_model']}")
```

### **Batch Processing**
```python
from model_selector import ModelSelector

selector = ModelSelector()
selector.load_model('model_selector.pkl')

prompts = [
    "Write a REST API in Python",
    "Explain quantum physics",
    "Help me cook dinner"
]

for prompt in prompts:
    result = selector.select_best_model(prompt)
    print(f"{prompt} → {result['predicted_model']}")
```

### **Training Custom Model**
```python
import pandas as pd
from model_selector import ModelSelector

# Load your labeled dataset
df = pd.read_csv('your_data.csv')

# Train custom selector
selector = ModelSelector()
results = selector.train_model_selector(df)
selector.save_model('custom_model.pkl')

print(f"Accuracy: {results['accuracy']:.3f}")
```

## 📊 **Model Selection Examples**

| **Prompt** | **Selected Model** | **Confidence** | **Reasoning** |
|------------|-------------------|----------------|---------------|
| "Write a Python function for quicksort" | TNG DeepSeek | 0.456 | Technical coding task |
| "Explain economic benefits of renewable energy" | Qwen3 | 0.647 | Analytical reasoning |
| "Hello, help with cooking recipes?" | Llama 4 Maverick | 0.376 | Casual conversation |
| "Debug JavaScript error in React" | TNG DeepSeek | 0.591 | Technical debugging |
| "Analyze logical flaws in argument" | Qwen3 | 0.606 | Logical reasoning |
| "Best way to learn machine learning?" | Llama 4 Maverick | 0.986 | General advice |

## 🔍 **Individual Model Testing**

Each model test script provides:
- **API Connection Testing**: Verify model availability
- **Response Quality Analysis**: Evaluate output quality
- **Performance Metrics**: Response time and reliability
- **Debugging Information**: Error handling and logging

### **Test Script Features**
```python
# Example: Running Deepseek test
python Deepseek_test.py

# Output includes:
# ✅ API connection status
# ⏱️ Response time metrics  
# 📊 Output quality assessment
# 🐛 Error reporting
```

## 📈 **Model Parameters & Configuration**

The `Model_parameters.csv` file contains:
- Model specifications
- API endpoints and authentication
- Performance characteristics
- Specialized capabilities
- Cost and usage metrics

## 🛠 **Development & Customization**

### **Adding New Models**
1. Create new test script (e.g., `NewModel_test.py`)
2. Add model parameters to `Model_parameters.csv`
3. Update model selector training data
4. Retrain selection model

### **Customizing Selection Logic**
```python
# Modify model_selector.py
def simulate_best_model_selection(features):
    # Add your custom logic here
    if 'custom_category' in features['categories']:
        return 'YourNewModel'
    # ... existing logic
```

### **Feature Engineering**
```python
# Extend prompt_analyzer.py
def extract_custom_features(prompt):
    # Add domain-specific feature extraction
    custom_score = analyze_domain_specific_patterns(prompt)
    return custom_score
```

## 🔒 **Security & API Keys**

- API keys are stored in `orche.env` file (not in this directory)
- Each model test handles authentication independently
- Model selector doesn't require API keys (uses cached features)

## 📚 **Documentation**

- **Comprehensive Guide**: `MODEL_SELECTOR_GUIDE.md` - Complete system documentation
- **API Reference**: Individual test scripts contain usage examples
- **Configuration**: `Model_parameters.csv` for model specifications

## 🧪 **Testing & Validation**

### **Run All Tests**
```bash
# Test all models
for f in *_test.py; do python "$f"; done

# Test model selector system
python model_selector.py
```

### **Validation Metrics**
- Cross-validation accuracy
- Feature importance analysis
- Model confidence calibration
- Classification reports per model

## 🚀 **Production Deployment**

### **API Integration**
```python
from flask import Flask, request, jsonify
from model_selector import ModelSelector

app = Flask(__name__)
selector = ModelSelector()
selector.load_model('model_selector.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    prompt = request.json['prompt']
    result = selector.select_best_model(prompt)
    return jsonify(result)
```

### **Batch Processing**
```python
def process_batch(prompts):
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

## 🤝 **Contributing**

1. **Adding Models**: Follow existing test script patterns
2. **Improving Selection**: Enhance feature extraction or ML algorithms
3. **Documentation**: Update this README and guides
4. **Testing**: Ensure all scripts work with new additions

## 📞 **Support**

- **Issues**: Check individual test scripts for API connection problems
- **Performance**: Monitor model response times and accuracy
- **Updates**: Retrain model selector when adding new models
- **Documentation**: Refer to `MODEL_SELECTOR_GUIDE.md` for detailed information

---

**Built for OrchestrateX AI Model Orchestration System** 🎯

*Last Updated: August 31, 2025*
