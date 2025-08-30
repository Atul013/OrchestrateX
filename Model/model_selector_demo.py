"""
Model Selector Usage Example

This demonstrates how to use the trained model selector to predict
the best AI model for any given prompt.
"""

from model_selector import ModelSelector

def main():
    """Main demonstration of model selector usage."""
    
    print("=== MODEL SELECTOR USAGE DEMONSTRATION ===\n")
    
    # Load the pre-trained model
    print("Loading trained model...")
    selector = ModelSelector()
    selector.load_model('model_selector.pkl')
    print("Model loaded successfully!\n")
    
    # Test prompts covering different categories
    test_prompts = [
        # Technical/Coding prompts
        "Create a RESTful API using Python Flask with JWT authentication",
        "Write a recursive function to traverse a binary tree",
        "How do I optimize database queries for better performance?",
        
        # Analytical/Reasoning prompts  
        "Analyze the impact of climate change on global agriculture",
        "Compare the advantages and disadvantages of different sorting algorithms",
        "Explain the philosophical implications of artificial intelligence",
        
        # General/Conversational prompts
        "What are some good movies to watch this weekend?",
        "Help me plan a healthy meal for dinner",
        "Can you tell me about the history of jazz music?",
        
        # Mixed/Complex prompts
        "Explain how machine learning algorithms work and implement a simple one",
        "What are the ethical considerations in AI development?",
    ]
    
    print("Testing model predictions:\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i:2d}. Prompt: \"{prompt}\"")
        
        # Get prediction
        result = selector.select_best_model(prompt)
        
        # Display results
        print(f"    Best Model: {result['predicted_model']}")
        print(f"    Confidence: {result['prediction_confidence']:.3f}")
        
        # Show prompt analysis
        features = result['prompt_features']
        print(f"    Categories: {features['categories']}")
        print(f"    Domain: {features['topic_domain']} | Intent: {features['intent_type']}")
        
        # Show top 3 model confidences
        top_models = sorted(result['confidence_scores'].items(), 
                          key=lambda x: x[1], reverse=True)[:3]
        
        print("    Model Confidences:")
        for j, (model, confidence) in enumerate(top_models, 1):
            print(f"      {j}. {model}: {confidence:.3f}")
        
        print()
    
    print("=== DEMONSTRATION COMPLETE ===")

def predict_single_prompt(prompt_text):
    """
    Simplified function to get model prediction for a single prompt.
    
    Args:
        prompt_text (str): The user prompt to analyze
        
    Returns:
        dict: Prediction results
    """
    selector = ModelSelector()
    selector.load_model('model_selector.pkl')
    return selector.select_best_model(prompt_text)


if __name__ == "__main__":
    main()
