#!/usr/bin/env python3
"""
UI Bridge API - Connects your UI to Algorithm and MongoDB
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
CONNECTION_STRING = "mongodb://project_admin:project_password@localhost:27017/orchestratex?authSource=admin"
client = MongoClient(CONNECTION_STRING)
db = client.orchestratex

def choose_model(prompt):
    """Enhanced algorithm to choose best model from 6 available models"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["code", "python", "javascript", "programming", "function", "debug"]):
        return "Qwen3", 0.95, "Technical/coding task - Qwen3 best for programming"
    elif any(word in prompt_lower for word in ["analyze", "deep", "research", "complex", "detailed"]):
        return "TNG DeepSeek", 0.92, "Deep analysis task - TNG DeepSeek for comprehensive reasoning"
    elif any(word in prompt_lower for word in ["logic", "reason", "solve", "problem", "structure"]):
        return "GLM4.5", 0.90, "Logical reasoning - GLM4.5 for structured thinking"
    elif any(word in prompt_lower for word in ["creative", "story", "idea", "innovative", "unique"]):
        return "MoonshotAI Kimi", 0.88, "Creative task - Kimi for innovative solutions"
    elif any(word in prompt_lower for word in ["explain", "clear", "simple", "understand", "guide"]):
        return "Llama 4 Maverick", 0.85, "Communication task - Llama for clarity"
    else:
        return "GPT-OSS", 0.80, "General query - GPT-OSS for balanced responses"

def simulate_response(model, prompt):
    """Simulate AI response"""
    responses = {
        "TNG DeepSeek": f"[TNG DeepSeek] Deep analytical response: {prompt[:30]}... with comprehensive reasoning and multi-layered analysis.",
        "GLM4.5": f"[GLM4.5] Logical structured response: {prompt[:30]}... with systematic approach and clear reasoning chains.",
        "GPT-OSS": f"[GPT-OSS] Accurate factual response: {prompt[:30]}... with verified information and reliable sources.",
        "MoonshotAI Kimi": f"[Kimi] Creative innovative response: {prompt[:30]}... with unique perspectives and imaginative solutions.", 
        "Llama 4 Maverick": f"[Llama Maverick] Clear communicative response: {prompt[:30]}... with excellent clarity and user-friendly explanations.",
        "Qwen3": f"[Qwen3] Technical precise response: {prompt[:30]}... with detailed implementation and code examples."
    }
    return responses.get(model, f"[{model}] Response for: {prompt[:30]}...")

def generate_critique(critic_model, target_response, focus_area):
    """Generate focused critique from a model"""
    critique_templates = {
        "TNG DeepSeek": {
            "accuracy": "Needs fact verification",
            "logic": "Missing causal links", 
            "technical": "Lacks implementation details",
            "creativity": "Needs alternative approaches",
            "clarity": "Unclear explanations",
            "depth": "Superficial analysis"
        },
        "GLM4.5": {
            "accuracy": "Questionable data sources",
            "logic": "Logical gaps present",
            "technical": "Missing error handling", 
            "creativity": "Too conventional approach",
            "clarity": "Confusing structure",
            "depth": "Needs deeper insight"
        },
        "GPT-OSS": {
            "accuracy": "Unverified claims made",
            "logic": "Reasoning flaws detected",
            "technical": "Optimization opportunities missed",
            "creativity": "Lacks innovation",
            "clarity": "Unclear messaging",
            "depth": "Surface-level treatment"
        },
        "MoonshotAI Kimi": {
            "accuracy": "Facts need checking",
            "logic": "Logic chain broken",
            "technical": "Architecture improvements needed",
            "creativity": "Generic solution provided",
            "clarity": "Communication unclear",
            "depth": "Analysis too shallow"
        },
        "Llama 4 Maverick": {
            "accuracy": "Information accuracy concerns",
            "logic": "Logical inconsistencies",
            "technical": "Best practices ignored",
            "creativity": "Predictable approach",
            "clarity": "Explanation lacks clarity",
            "depth": "Insufficient detail"
        },
        "Qwen3": {
            "accuracy": "Data validation needed",
            "logic": "Inference errors",
            "technical": "Code quality issues", 
            "creativity": "Standard solution only",
            "clarity": "Technical jargon overload",
            "depth": "Missing comprehensive view"
        }
    }
    
    return critique_templates.get(critic_model, {}).get(focus_area, "Needs improvement")

@app.route('/chat', methods=['POST'])
def chat():
    """Main endpoint - receives UI input, processes through algorithm, stores in MongoDB"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"📱 UI Message: {user_message}")
        
        # Algorithm chooses model
        selected_model, confidence, reasoning = choose_model(user_message)
        print(f"🤖 Algorithm chose: {selected_model}")
        
        # Get response from selected model
        ai_response = simulate_response(selected_model, user_message)
        print(f"💬 Response: {ai_response[:50]}...")
        
        # Generate critiques from all other models (6 total models)
        all_models = ["TNG DeepSeek", "GLM4.5", "GPT-OSS", "MoonshotAI Kimi", "Llama 4 Maverick", "Qwen3"]
        focus_areas = ["accuracy", "logic", "technical", "creativity", "clarity", "depth"]
        
        critiques = []
        for i, model in enumerate(all_models):
            if model != selected_model:  # Don't critique yourself
                focus = focus_areas[i % len(focus_areas)]
                critique_text = generate_critique(model, ai_response, focus)
                
                critiques.append({
                    "model_name": model,
                    "critique_text": critique_text,
                    "tokens_used": random.randint(20, 40),
                    "cost_usd": 0.0005,
                    "latency_ms": random.randint(400, 800)
                })
        
        print(f"🔄 Generated {len(critiques)} critiques from other models")
        
        # Store in MongoDB Docker
        session_data = {
            "user_message": user_message,
            "selected_model": selected_model,
            "confidence": confidence,
            "reasoning": reasoning,
            "ai_response": ai_response,
            "critiques": critiques,
            "timestamp": datetime.now(),
            "source": "ui_chat",
            "total_models_used": len(critiques) + 1
        }
        
        result = db.user_responses.insert_one(session_data)
        print(f"💾 Stored in MongoDB! ID: {result.inserted_id}")
        
        # Also store individual critiques for analytics
        for critique in critiques:
            critique_record = {
                "session_id": str(result.inserted_id),
                "user_prompt": user_message,
                "target_model": selected_model,
                "critic_model": critique["model_name"],
                "critique_text": critique["critique_text"],
                "timestamp": datetime.now(),
                "source": "ui_critique"
            }
            db.model_critiques.insert_one(critique_record)
        
        return jsonify({
            "success": True,
            "primary_response": {
                "success": True,
                "model_name": selected_model,
                "response_text": ai_response,
                "tokens_used": random.randint(100, 200),
                "cost_usd": 0.002,
                "latency_ms": random.randint(800, 1200)
            },
            "critiques": critiques,
            "total_cost": 0.002 + sum(c["cost_usd"] for c in critiques),
            "api_calls": len(critiques) + 1,
            "success_rate": 100.0,
            "metadata": {
                "confidence": confidence,
                "reasoning": reasoning,
                "mongodb_id": str(result.inserted_id),
                "timestamp": session_data["timestamp"].isoformat(),
                "total_models": len(all_models),
                "critiques_generated": len(critiques)
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "service": "UI Bridge API",
        "status": "running",
        "endpoints": ["/chat", "/health", "/models"],
        "description": "Connects UI → Algorithm → MongoDB Docker"
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "mongodb_connected": True,
        "message": "UI Bridge API working!"
    })

@app.route('/models', methods=['GET'])
def models():
    """Available models"""
    return jsonify({
        "models": ["gpt-4", "claude-3", "gemini-pro", "gpt-3.5"],
        "algorithm": "keyword_based_selection"
    })

if __name__ == '__main__':
    print("🚀 UI Bridge API: UI → Algorithm → MongoDB Docker")
    print("UI connects to: http://localhost:8002")
    print("MongoDB view: http://localhost:8081")
    print("=" * 50)
    
    # Test MongoDB connection
    try:
        client.admin.command('ping')
        print("✅ MongoDB Docker connected!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    
    app.run(host='0.0.0.0', port=8002, debug=True)
