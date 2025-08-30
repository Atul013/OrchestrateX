#!/usr/bin/env python3
"""
Example of how to use REAL data instead of simulated data for training.
"""

import pandas as pd
from model_selector import ModelSelector
from prompt_analyzer import extract_prompt_features

def create_real_dataset_example():
    """
    Example of how you would prepare real data for training.
    """
    print("📝 HOW TO USE REAL DATA FOR TRAINING")
    print("=" * 60)
    
    # Example of what real data might look like
    real_data_example = [
        {
            "prompt": "Write a Python function to sort a list",
            "best_model": "TNG DeepSeek",  # From actual testing/user feedback
            "user_rating": 4.8,          # User satisfaction (optional)
            "response_time": 2.3,        # Model response time (optional)
            "task_success": True          # Did it complete the task? (optional)
        },
        {
            "prompt": "Explain the causes of global warming",
            "best_model": "Qwen3",
            "user_rating": 4.5,
            "response_time": 3.1,
            "task_success": True
        },
        {
            "prompt": "What's a good recipe for pasta?",
            "best_model": "MoonshotAI Kimi",
            "user_rating": 4.2,
            "response_time": 1.8,
            "task_success": True
        },
        {
            "prompt": "Debug this JavaScript error: TypeError undefined",
            "best_model": "TNG DeepSeek",
            "user_rating": 4.9,
            "response_time": 2.7,
            "task_success": True
        },
        {
            "prompt": "Compare renewable vs fossil fuel economics",
            "best_model": "GLM4.5",
            "user_rating": 4.6,
            "response_time": 4.2,
            "task_success": True
        }
    ]
    
    print("🎯 REAL DATA SOURCES:")
    print("1. 📊 A/B Testing Results - Which model performed better?")
    print("2. 👤 User Feedback - Ratings and satisfaction scores")
    print("3. 📈 Performance Metrics - Response time, accuracy, completion rate")
    print("4. 🎪 Production Logs - Real prompts and their outcomes")
    print("5. 🧪 Evaluation Studies - Expert assessment of model outputs")
    print()
    
    # Convert to DataFrame
    df_real = pd.DataFrame(real_data_example)
    print("📋 EXAMPLE REAL DATASET:")
    print(df_real.to_string(index=False))
    print()
    
    # Process real data for training
    print("🔄 PROCESSING REAL DATA FOR TRAINING:")
    processed_data = []
    
    for _, row in df_real.iterrows():
        # Extract features from the prompt
        features = extract_prompt_features(row['prompt'])
        
        # Combine with your labels
        processed_row = {
            'prompt': row['prompt'],
            'categories': features['categories'],
            'topic_domain': features['topic_domain'],
            'intent_type': features['intent_type'],
            'confidence': features['confidence'],
            'token_count': features['token_count'],
            'best_model': row['best_model']  # Your ground truth label
        }
        processed_data.append(processed_row)
    
    df_processed = pd.DataFrame(processed_data)
    print("✅ Processed dataset ready for training!")
    print(f"   Shape: {df_processed.shape}")
    print(f"   Columns: {list(df_processed.columns)}")
    print()
    
    print("🚀 TRAINING WITH REAL DATA:")
    print("```python")
    print("# Use your processed real data")
    print("selector = ModelSelector()")
    print("results = selector.train_model_selector(df_processed)")
    print("selector.save_model('real_model.pkl')")
    print("```")
    print()
    
    print("📁 WHERE TO GET REAL DATA:")
    print("1. 🔄 Start with simulation (what we did) to build initial system")
    print("2. 🚀 Deploy in production with multiple models")
    print("3. 📊 Collect user interactions and performance data")
    print("4. 🎯 Retrain with real data as it accumulates")
    print("5. 🔄 Continuously improve with more data")
    
    return df_processed

def show_data_collection_strategy():
    """Show how to collect real training data in production."""
    print("\n" + "=" * 60)
    print("📈 DATA COLLECTION STRATEGY FOR PRODUCTION")
    print("=" * 60)
    
    print("""
🎯 PHASE 1: BOOTSTRAP (Current - Simulated Data)
   ✅ Use simulated data to build initial system
   ✅ Deploy with multiple models available
   ✅ Start collecting real user interactions

🎯 PHASE 2: COLLECT (Production Deployment)
   📊 Log every user prompt and model selection
   ⏱️  Measure response times for each model
   👤 Collect user feedback/ratings
   🎪 A/B test different models for same prompts

🎯 PHASE 3: RETRAIN (Continuous Improvement)
   🔄 Weekly/monthly retraining with real data
   📈 Compare real vs simulated performance
   🎯 Adjust model selection rules based on data
   🚀 Deploy improved models

🎯 EXAMPLE PRODUCTION LOGGING:
```python
# In your production API
@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['prompt']
    
    # Get model recommendation
    result = selector.select_best_model(prompt)
    selected_model = result['predicted_model']
    
    # Call the model and measure performance
    start_time = time.time()
    response = call_ai_model(selected_model, prompt)
    response_time = time.time() - start_time
    
    # Log for future training
    log_interaction({
        'prompt': prompt,
        'selected_model': selected_model,
        'response_time': response_time,
        'confidence': result['prediction_confidence'],
        'timestamp': datetime.now()
    })
    
    return jsonify({'response': response, 'model': selected_model})

# Collect user feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    interaction_id = request.json['interaction_id']
    rating = request.json['rating']  # 1-5 stars
    
    # Store for training data
    store_feedback(interaction_id, rating)
```

🎯 REAL DATA SOURCES:
1. 📊 User interaction logs
2. ⭐ User ratings and feedback
3. 📈 Model performance metrics
4. 🎪 A/B testing results
5. 👥 Expert evaluations
""")

if __name__ == "__main__":
    df = create_real_dataset_example()
    show_data_collection_strategy()
