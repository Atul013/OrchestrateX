#!/usr/bin/env python3
"""
Advanced OrchestrateX Multi-Model Parallel Processing
- User prompts stored in 'user_database' 
- 5 models run in parallel, responses stored in 'model_responses_database'
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import asyncio
import concurrent.futures
import time
import random

app = Flask(__name__)
CORS(app)

# Separate MongoDB connections for different purposes
USER_DB_CONNECTION = "mongodb://project_admin:project_password@localhost:27017/user_database?authSource=admin"
MODEL_DB_CONNECTION = "mongodb://project_admin:project_password@localhost:27017/model_responses?authSource=admin"

user_client = MongoClient(USER_DB_CONNECTION)
model_client = MongoClient(MODEL_DB_CONNECTION)

user_db = user_client.user_database
model_db = model_client.model_responses

# Latest 5 Model configurations from orche.env
MODELS = [
    {"name": "GLM-4.5", "specialty": "reasoning", "strength": 0.95, "model_id": "z-ai/glm-4.5-air:free"},
    {"name": "GPT-OSS", "specialty": "general", "strength": 0.90, "model_id": "openai/gpt-oss-120b:free"},
    {"name": "Llama-4-Maverick", "specialty": "coding", "strength": 0.88, "model_id": "meta-llama/llama-4-maverick:free"},
    {"name": "Kimi-K2", "specialty": "creative", "strength": 0.85, "model_id": "moonshotai/kimi-k2:free"},
    {"name": "TNG-DeepSeek-R1T2", "specialty": "analysis", "strength": 0.92, "model_id": "tngtech/deepseek-r1t2-chimera:free"}
]

def simulate_model_response(model, prompt, delay=None):
    """Simulate AI model response with realistic delay"""
    if delay is None:
        delay = random.uniform(1, 3)  # Random delay 1-3 seconds
    
    time.sleep(delay)
    
    # Generate different types of responses based on model specialty
    responses = {
        "gpt-4": f"[GPT-4 Reasoning] Analyzed '{prompt[:30]}...' - Step-by-step approach: {random.randint(1,10)} key points identified.",
        "claude-3": f"[Claude-3 Creative] Creative interpretation of '{prompt[:30]}...' - Novel perspective with {random.randint(3,8)} unique insights.",
        "gemini-pro": f"[Gemini-Pro Factual] Factual analysis of '{prompt[:30]}...' - {random.randint(5,15)} verified data points sourced.",
        "llama-3": f"[Llama-3 Coding] Technical solution for '{prompt[:30]}...' - {random.randint(2,6)} implementation strategies.",
        "mistral-large": f"[Mistral Analysis] Deep analysis of '{prompt[:30]}...' - {random.randint(4,9)} analytical dimensions explored."
    }
    
    return {
        "model_name": model["name"],
        "specialty": model["specialty"],
        "response_text": responses.get(model["name"], f"Response from {model['name']}"),
        "confidence": model["strength"] + random.uniform(-0.05, 0.05),
        "processing_time_ms": int(delay * 1000),
        "timestamp": datetime.now(),
        "tokens_used": random.randint(100, 500),
        "cost_estimate": round(random.uniform(0.001, 0.01), 4)
    }

def run_models_parallel(prompt):
    """Run all 5 models in parallel"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all model tasks
        future_to_model = {
            executor.submit(simulate_model_response, model, prompt): model 
            for model in MODELS
        }
        
        results = []
        for future in concurrent.futures.as_completed(future_to_model):
            model = future_to_model[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Model {model['name']} failed: {e}")
        
        return results

@app.route('/chat', methods=['POST'])
def parallel_chat():
    """Main endpoint: Store user prompt + Run 5 models in parallel"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"📱 User Message: {user_message}")
        
        # 1. Store user prompt in user_database
        user_session = {
            "user_message": user_message,
            "timestamp": datetime.now(),
            "session_id": f"session_{int(time.time())}",
            "source": "ui_interface",
            "status": "processing"
        }
        
        user_result = user_db.user_prompts.insert_one(user_session)
        session_id = str(user_result.inserted_id)
        print(f"💾 User prompt stored in user_database! ID: {session_id}")
        
        # 2. Run 5 models in parallel
        print("🚀 Starting parallel processing with 5 models...")
        start_time = time.time()
        
        model_responses = run_models_parallel(user_message)
        
        total_time = time.time() - start_time
        print(f"⚡ All 5 models completed in {total_time:.2f} seconds")
        
        # 3. Store all model responses in model_responses_database
        batch_insert_data = []
        for response in model_responses:
            response_record = {
                "session_id": session_id,
                "user_message": user_message,
                **response,
                "batch_id": f"batch_{int(time.time())}"
            }
            batch_insert_data.append(response_record)
        
        model_db.parallel_responses.insert_many(batch_insert_data)
        print(f"💾 All 5 model responses stored in model_responses database!")
        
        # 4. Find best response
        best_response = max(model_responses, key=lambda x: x['confidence'])
        
        # 5. Update user session as completed
        user_db.user_prompts.update_one(
            {"_id": user_result.inserted_id},
            {"$set": {
                "status": "completed",
                "best_model": best_response["model_name"],
                "total_processing_time": total_time,
                "models_used": len(model_responses),
                "completed_at": datetime.now()
            }}
        )
        
        print(f"🏆 Best response from: {best_response['model_name']} (confidence: {best_response['confidence']:.3f})")
        
        # 6. Return UI-compatible response
        return jsonify({
            "success": True,
            "primary_response": {
                "success": True,
                "model_name": best_response["model_name"],
                "response_text": best_response["response_text"],
                "tokens_used": best_response["tokens_used"],
                "cost_usd": best_response["cost_estimate"],
                "latency_ms": int(total_time * 1000)
            },
            "critiques": [
                {
                    "model_name": resp["model_name"],
                    "critique_text": f"Alternative perspective: {resp['response_text'][:100]}...",
                    "confidence": resp["confidence"]
                }
                for resp in model_responses if resp != best_response
            ][:3],  # Show top 3 alternatives
            "metadata": {
                "session_id": session_id,
                "total_models": len(model_responses),
                "processing_time_seconds": round(total_time, 2),
                "user_db_stored": True,
                "model_db_stored": True,
                "parallel_processing": True
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def system_status():
    """Check system status and database connections"""
    try:
        # Test user database
        user_client.admin.command('ping')
        user_count = user_db.user_prompts.count_documents({})
        
        # Test model database  
        model_client.admin.command('ping')
        model_count = model_db.parallel_responses.count_documents({})
        
        return jsonify({
            "status": "healthy",
            "user_database": {
                "connected": True,
                "total_prompts": user_count
            },
            "model_database": {
                "connected": True,
                "total_responses": model_count
            },
            "parallel_models": len(MODELS),
            "models_available": [m["name"] for m in MODELS]
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/analytics', methods=['GET'])
def analytics():
    """Get analytics from both databases"""
    try:
        # User database analytics
        recent_prompts = list(user_db.user_prompts.find().sort("timestamp", -1).limit(5))
        
        # Model database analytics
        model_stats = {}
        for model in MODELS:
            count = model_db.parallel_responses.count_documents({"model_name": model["name"]})
            avg_confidence = list(model_db.parallel_responses.aggregate([
                {"$match": {"model_name": model["name"]}},
                {"$group": {"_id": None, "avg_confidence": {"$avg": "$confidence"}}}
            ]))
            model_stats[model["name"]] = {
                "total_responses": count,
                "avg_confidence": round(avg_confidence[0]["avg_confidence"], 3) if avg_confidence else 0
            }
        
        return jsonify({
            "user_analytics": {
                "total_sessions": user_db.user_prompts.count_documents({}),
                "completed_sessions": user_db.user_prompts.count_documents({"status": "completed"}),
                "recent_prompts": [
                    {
                        "message": p.get("user_message", "")[:50] + "...",
                        "timestamp": p.get("timestamp"),
                        "status": p.get("status")
                    }
                    for p in recent_prompts
                ]
            },
            "model_analytics": {
                "total_parallel_responses": model_db.parallel_responses.count_documents({}),
                "model_performance": model_stats
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Advanced OrchestrateX: Parallel 5-Model System")
    print("📊 User prompts → user_database")
    print("🤖 Model responses → model_responses database") 
    print("⚡ Parallel processing enabled")
    print("=" * 60)
    
    # Test database connections
    try:
        user_client.admin.command('ping')
        model_client.admin.command('ping')
        print("✅ Both databases connected!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    app.run(host='0.0.0.0', port=8002, debug=True)
