#!/usr/bin/env python3
"""
Simplified Model Selector for OrchestrateX
Uses rule-based algorithm for model selection
"""

import re
import random

class ModelSelector:
    """
    Intelligent model selector that chooses the best AI model based on prompt analysis
    """
    
    def __init__(self):
        self.models = {
            "GPT-OSS 120B": {
                "keywords": ["fact", "accurate", "correct", "verify", "truth", "research", "academic"],
                "domains": ["academic", "research", "fact-checking", "knowledge"],
                "confidence_base": 0.85
            },
            "GLM-4.5 Air": {
                "keywords": ["logic", "reason", "solve", "problem", "structure", "analyze", "think"],
                "domains": ["logical-reasoning", "problem-solving", "analysis"],
                "confidence_base": 0.90
            },
            "Qwen3 Coder": {
                "keywords": ["code", "python", "javascript", "programming", "function", "debug", "software", "api"],
                "domains": ["programming", "technical", "coding", "development"],
                "confidence_base": 0.95
            },
            "TNG DeepSeek": {
                "keywords": ["deep", "detailed", "comprehensive", "thorough", "complex", "research"],
                "domains": ["deep-analysis", "research", "comprehensive"],
                "confidence_base": 0.92
            },
            "MoonshotAI Kimi": {
                "keywords": ["creative", "story", "idea", "innovative", "unique", "artistic", "imagine"],
                "domains": ["creative", "storytelling", "innovation"],
                "confidence_base": 0.88
            },
            "Llama 4 Maverick": {
                "keywords": ["explain", "clear", "simple", "understand", "communicate", "teach"],
                "domains": ["explanation", "communication", "teaching"],
                "confidence_base": 0.87
            }
        }
    
    def analyze_prompt(self, prompt):
        """Analyze prompt to extract features"""
        prompt_lower = prompt.lower()
        
        features = {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_question": "?" in prompt,
            "has_code_request": any(word in prompt_lower for word in ["code", "function", "python", "javascript"]),
            "complexity_indicators": len([word for word in ["complex", "detailed", "comprehensive", "deep"] if word in prompt_lower]),
            "creative_indicators": len([word for word in ["story", "creative", "imagine", "unique"] if word in prompt_lower])
        }
        
        return features
    
    def score_model(self, model_name, model_config, prompt):
        """Score a model for the given prompt"""
        prompt_lower = prompt.lower()
        score = model_config["confidence_base"]
        
        # Keyword matching
        keyword_matches = sum(1 for keyword in model_config["keywords"] if keyword in prompt_lower)
        score += keyword_matches * 0.05
        
        # Length bonus for appropriate models
        prompt_length = len(prompt.split())
        if model_name == "TNG DeepSeek" and prompt_length > 20:
            score += 0.05
        elif model_name == "Qwen3 Coder" and any(word in prompt_lower for word in ["code", "function", "programming"]):
            score += 0.10
        elif model_name == "MoonshotAI Kimi" and any(word in prompt_lower for word in ["creative", "story", "idea"]):
            score += 0.08
        
        # Add some randomness to avoid always picking the same model
        score += random.uniform(-0.02, 0.02)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def select_best_model(self, prompt):
        """Select the best model for the given prompt"""
        features = self.analyze_prompt(prompt)
        
        # Score all models
        model_scores = {}
        for model_name, model_config in self.models.items():
            score = self.score_model(model_name, model_config, prompt)
            model_scores[model_name] = score
        
        # Find best model
        best_model = max(model_scores, key=model_scores.get)
        best_confidence = model_scores[best_model]
        
        return {
            "predicted_model": best_model,
            "prediction_confidence": best_confidence,
            "confidence_scores": model_scores,
            "prompt_features": features
        }
    
    def predict(self, prompt):
        """Legacy compatibility method"""
        result = self.select_best_model(prompt)
        return {
            "model": result["predicted_model"],
            "confidence": result["prediction_confidence"],
            "all_confidences": result["confidence_scores"]
        }
    
    def load_model(self, filepath):
        """Load model (placeholder for compatibility)"""
        print(f"✅ Model selector initialized (rule-based)")
        return True
    
    def save_model(self, filepath):
        """Save model (placeholder for compatibility)"""
        print(f"✅ Model selector saved to {filepath}")
        return True

if __name__ == "__main__":
    # Test the model selector
    selector = ModelSelector()
    
    test_prompts = [
        "Write a Python function to sort arrays",
        "Tell me a creative story about robots",
        "Explain quantum physics in simple terms",
        "Help me debug this JavaScript code",
        "Analyze the economic implications of AI"
    ]
    
    print("🧠 Testing Model Selector")
    print("=" * 50)
    
    for prompt in test_prompts:
        result = selector.select_best_model(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Best Model: {result['predicted_model']}")
        print(f"Confidence: {result['prediction_confidence']:.3f}")