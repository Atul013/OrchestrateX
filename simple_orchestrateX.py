#!/usr/bin/env python3
"""
OrchestrateX Simple Algorithm
UI → Algorithm → MongoDB Docker
No complex backend needed!
"""

from pymongo import MongoClient
from datetime import datetime
import json
import random

class SimpleOrchestrateX:
    def __init__(self):
        # Connect to MongoDB Docker
        self.connection_string = "mongodb://project_admin:project_password@localhost:27019/orchestratex?authSource=admin"
        self.client = MongoClient(self.connection_string)
        self.db = self.client.orchestratex
        
        # Available AI models
        self.models = {
            "gpt-4": {"good_for": ["coding", "complex_analysis", "detailed_explanations"], "cost": 0.03},
            "gpt-3.5": {"good_for": ["general_chat", "simple_questions", "quick_responses"], "cost": 0.002},
            "claude-3": {"good_for": ["creative_writing", "analysis", "reasoning"], "cost": 0.025},
            "gemini-pro": {"good_for": ["research", "factual_questions", "summaries"], "cost": 0.01}
        }
    
    def analyze_prompt(self, user_prompt):
        """Simple algorithm to choose best model based on prompt"""
        prompt_lower = user_prompt.lower()
        
        # Simple keyword-based selection
        if any(word in prompt_lower for word in ["code", "python", "javascript", "programming", "function"]):
            return "gpt-4", 0.95, "Coding task detected - GPT-4 best for programming"
        
        elif any(word in prompt_lower for word in ["creative", "story", "write", "poem", "article"]):
            return "claude-3", 0.90, "Creative writing task - Claude-3 excels at creativity"
        
        elif any(word in prompt_lower for word in ["research", "facts", "information", "summary"]):
            return "gemini-pro", 0.85, "Research task - Gemini-Pro good for factual information"
        
        elif len(user_prompt) < 50:
            return "gpt-3.5", 0.80, "Simple short question - GPT-3.5 is sufficient and cost-effective"
        
        else:
            return "gpt-4", 0.75, "Complex general task - GPT-4 as default for comprehensive response"
    
    def simulate_model_response(self, model_name, user_prompt):
        """Simulate getting response from chosen model"""
        responses = {
            "gpt-4": f"[GPT-4 Response] I'll help you with: {user_prompt[:50]}... (detailed technical response)",
            "gpt-3.5": f"[GPT-3.5 Response] Quick answer for: {user_prompt[:30]}... (simple response)",
            "claude-3": f"[Claude-3 Response] Creative approach to: {user_prompt[:40]}... (thoughtful response)",
            "gemini-pro": f"[Gemini-Pro Response] Research-based answer: {user_prompt[:35]}... (factual response)"
        }
        
        return {
            "response_text": responses.get(model_name, "Generic response"),
            "response_time_ms": random.randint(500, 3000),
            "token_count": random.randint(50, 500),
            "cost": self.models[model_name]["cost"] * random.uniform(0.5, 2.0)
        }
    
    def process_user_input(self, user_input_data):
        """Main processing: UI input → Algorithm → MongoDB"""
        
        print(f"🎯 Processing: {user_input_data['prompt'][:50]}...")
        
        # Step 1: Algorithm chooses best model
        selected_model, confidence, reasoning = self.analyze_prompt(user_input_data['prompt'])
        
        print(f"🤖 Algorithm chose: {selected_model} (confidence: {confidence})")
        print(f"💭 Reasoning: {reasoning}")
        
        # Step 2: Simulate getting response from chosen model
        model_response = self.simulate_model_response(selected_model, user_input_data['prompt'])
        
        print(f"📝 Model response: {model_response['response_text'][:60]}...")
        
        # Step 3: Store everything in MongoDB Docker
        session_doc = {
            "session_id": f"session_{int(datetime.now().timestamp())}",
            "user_input": {
                "user_id": user_input_data.get("user_id", "anonymous"),
                "prompt": user_input_data["prompt"],
                "timestamp": datetime.now()
            },
            "algorithm_decision": {
                "selected_model": selected_model,
                "confidence_score": confidence,
                "reasoning": reasoning,
                "available_models": list(self.models.keys()),
                "selection_timestamp": datetime.now()
            },
            "model_response": {
                "model_name": selected_model,
                "response_text": model_response["response_text"],
                "response_time_ms": model_response["response_time_ms"],
                "token_count": model_response["token_count"],
                "cost": round(model_response["cost"], 4),
                "response_timestamp": datetime.now()
            },
            "workflow": "UI → Algorithm → MongoDB",
            "created_at": datetime.now()
        }
        
        # Store in MongoDB Docker
        result = self.db.user_sessions.insert_one(session_doc)
        
        print(f"💾 Stored in MongoDB! Document ID: {result.inserted_id}")
        
        return {
            "session_id": session_doc["session_id"],
            "selected_model": selected_model,
            "confidence": confidence,
            "response": model_response["response_text"],
            "cost": model_response["cost"],
            "mongodb_id": str(result.inserted_id)
        }
    
    def get_analytics(self):
        """Get simple analytics from MongoDB"""
        total_sessions = self.db.user_sessions.count_documents({})
        
        # Most used models
        pipeline = [
            {"$group": {"_id": "$algorithm_decision.selected_model", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        model_usage = list(self.db.user_sessions.aggregate(pipeline))
        
        return {
            "total_sessions": total_sessions,
            "model_usage": model_usage
        }
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()

# Test function
def test_simple_algorithm():
    """Test the simple algorithm"""
    
    print("🚀 Testing Simple OrchestrateX Algorithm")
    print("UI → Algorithm → MongoDB Docker")
    print("=" * 60)
    
    # Initialize
    orchestrateX = SimpleOrchestrateX()
    
    # Test cases (simulating UI inputs)
    test_inputs = [
        {
            "user_id": "test_user_1",
            "prompt": "Write a Python function to calculate fibonacci numbers"
        },
        {
            "user_id": "test_user_2", 
            "prompt": "Tell me a creative story about a robot"
        },
        {
            "user_id": "test_user_3",
            "prompt": "What are the benefits of renewable energy?"
        },
        {
            "user_id": "test_user_4",
            "prompt": "Hi, how are you?"
        }
    ]
    
    results = []
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n📱 Test {i}: UI Input")
        print(f"   User: {user_input['user_id']}")
        print(f"   Prompt: {user_input['prompt']}")
        
        # Process through algorithm
        result = orchestrateX.process_user_input(user_input)
        results.append(result)
        
        print(f"   ✅ Session: {result['session_id']}")
        print(f"   💾 MongoDB ID: {result['mongodb_id']}")
        
    # Show analytics
    print(f"\n📊 Analytics from MongoDB:")
    analytics = orchestrateX.get_analytics()
    print(f"   Total sessions stored: {analytics['total_sessions']}")
    print(f"   Model usage: {analytics['model_usage']}")
    
    print(f"\n🎉 Success! All data stored in MongoDB Docker")
    print(f"🌐 View at: http://localhost:8081 (admin/admin)")
    
    orchestrateX.close()
    return results

if __name__ == "__main__":
    test_simple_algorithm()
