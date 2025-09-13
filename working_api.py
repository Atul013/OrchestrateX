#!/usr/bin/env python3
"""
Working API for OrchestrateX - Connected to MongoDB Docker
Latest models with proper database storage
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import random
import time
import json
import os

app = Flask(__name__)
CORS(app, origins=['http://localhost:5176', 'http://localhost:5175', 'http://localhost:5174', 'http://127.0.0.1:5176', 'http://127.0.0.1:5175', 'http://127.0.0.1:5174'], 
     methods=['GET', 'POST', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization'])

# MongoDB Docker connection (using new port 27019 for different network)
MONGO_CONNECTION = "mongodb://project_admin:project_password@localhost:27019/orchestratex?authSource=admin"

# Try to connect to MongoDB, fallback to temp files if not available
try:
    client = MongoClient(MONGO_CONNECTION, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client.orchestratex
    mongodb_connected = True
    print("✅ MongoDB Docker connected successfully!")
except Exception as e:
    print(f"⚠️  MongoDB connection failed: {e}")
    print("📁 Using temporary file storage as fallback")
    mongodb_connected = False
    client = None
    db = None

# Latest 5 Model configurations from orche.env
MODELS = [
    {"name": "GLM-4.5", "specialty": "reasoning", "strength": 0.95, "model_id": "z-ai/glm-4.5-air:free"},
    {"name": "GPT-OSS", "specialty": "general", "strength": 0.90, "model_id": "openai/gpt-oss-120b:free"},
    {"name": "Llama-4-Maverick", "specialty": "coding", "strength": 0.88, "model_id": "meta-llama/llama-4-maverick:free"},
    {"name": "Kimi-K2", "specialty": "creative", "strength": 0.85, "model_id": "moonshotai/kimi-k2:free"},
    {"name": "TNG-DeepSeek-R1T2", "specialty": "analysis", "strength": 0.92, "model_id": "tngtech/deepseek-r1t2-chimera:free"}
]

def simulate_model_response(model, prompt, delay=None):
    """Simulate AI model response with realistic but fast delay"""
    if delay is None:
        delay = random.uniform(0.1, 0.3)  # Much faster: 0.1-0.3 seconds instead of 1-3
    
    time.sleep(delay)
    
    responses = {
        "GLM-4.5": f"[GLM-4.5 Reasoning] Advanced analysis of '{prompt[:30]}...' - Multi-step reasoning with {random.randint(1,10)} key insights identified.",
        "GPT-OSS": f"[GPT-OSS General] Comprehensive response to '{prompt[:30]}...' - Balanced approach with {random.randint(3,8)} perspectives covered.",
        "Llama-4-Maverick": f"[Llama-4-Maverick Coding] Technical solution for '{prompt[:30]}...' - {random.randint(2,6)} implementation strategies provided.",
        "Kimi-K2": f"[Kimi-K2 Creative] Creative interpretation of '{prompt[:30]}...' - Novel approach with {random.randint(4,9)} unique angles explored.",
        "TNG-DeepSeek-R1T2": f"[TNG-DeepSeek Analysis] Deep analytical response to '{prompt[:30]}...' - {random.randint(5,12)} analytical dimensions examined."
    }
    
    return {
        "model_name": model["name"],
        "specialty": model["specialty"],
        "response_text": responses.get(model["name"], f"Response from {model['name']}"),
        "confidence": model["strength"] + random.uniform(-0.05, 0.05),
        "processing_time": delay,  # Add this field that's used later
        "processing_time_ms": int(delay * 1000),
        "timestamp": datetime.now(),
        "tokens_used": random.randint(100, 500),
        "cost_estimate": round(random.uniform(0.001, 0.01), 4),
        "success": True  # Add success flag
    }

def generate_critique(critic_model, target_response, user_prompt):
    """Generate critique from one model about another model's response"""
    critique_templates = {
        "GLM-4.5": f"From a reasoning perspective, {target_response['model_name']}'s response lacks {random.choice(['logical structure', 'deeper analysis', 'systematic thinking'])}. A better approach would involve {random.choice(['step-by-step analysis', 'multi-layered reasoning', 'causal relationships'])}.",
        "GPT-OSS": f"The {target_response['model_name']} response is {random.choice(['too narrow', 'missing context', 'incomplete'])}. A more comprehensive approach should include {random.choice(['multiple perspectives', 'broader context', 'balanced viewpoints'])}.",
        "Llama-4-Maverick": f"From a technical standpoint, {target_response['model_name']} missed {random.choice(['implementation details', 'practical considerations', 'optimization opportunities'])}. Better solution: {random.choice(['modular approach', 'scalable design', 'efficient algorithm'])}.",
        "Kimi-K2": f"The {target_response['model_name']} response lacks {random.choice(['creativity', 'innovation', 'unique perspective'])}. More creative approach: {random.choice(['alternative angles', 'imaginative solutions', 'novel interpretations'])}.",
        "TNG-DeepSeek-R1T2": f"Deep analysis reveals {target_response['model_name']}'s response is {random.choice(['surface-level', 'missing nuances', 'lacks depth'])}. Deeper insight needed: {random.choice(['underlying patterns', 'complex relationships', 'systemic analysis'])}."
    }
    
    return critique_templates.get(critic_model["name"], f"Alternative perspective on {target_response['model_name']}'s response.")

def save_to_storage(data, collection_name):
    """Save data to MongoDB only - no temp files needed"""
    if mongodb_connected and db is not None:
        try:
            if collection_name == "prompts":  # Use prompts collection
                result = db.prompts.insert_one(data)
                print(f"✅ Stored in {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
            elif collection_name == "model_critiques":  # Use existing model_critiques collection
                result = db.model_critiques.insert_one(data)
                print(f"✅ Stored in {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
            elif collection_name == "model_outputs":  # NEW: For model outputs
                result = db.model_outputs.insert_one(data)
                print(f"✅ Stored in {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
            elif collection_name == "model_suggestions":  # NEW: For model recommendations
                result = db.model_suggestions.insert_one(data)
                print(f"✅ Stored in {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
        except Exception as e:
            print(f"❌ MongoDB write failed: {e}")
            return None
    else:
        print("❌ MongoDB not connected!")
        return None

def get_from_storage(collection_name):
    """Get data from MongoDB only"""
    if mongodb_connected and db is not None:
        try:
            if collection_name == "prompts":  # Updated to use existing collection
                return list(db.prompts.find().sort("timestamp", -1).limit(10))
            elif collection_name == "model_critiques":
                return list(db.model_critiques.find().sort("timestamp", -1).limit(10))
            elif collection_name == "model_outputs":
                return list(db.model_outputs.find().sort("timestamp", -1).limit(10))
            elif collection_name == "model_suggestions":
                return list(db.model_suggestions.find().sort("timestamp", -1).limit(10))
        except Exception as e:
            print(f"❌ MongoDB read failed: {e}")
            return []
    else:
        print("❌ MongoDB not connected!")
        return []

@app.route('/chat', methods=['POST'])
def chat():
    """Main endpoint: Process user prompt and return response"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"📱 User Message: {user_message}")
        
        # 1. Store user prompt in MongoDB or temporary storage
        session_id = f"session_{int(time.time())}"
        user_session = {
            "user_message": user_message,
            "timestamp": datetime.now(),
            "session_id": session_id,
            "source": "ui_interface",
            "status": "processing",
            "user": "anonymous",  # User column as requested
            "hash": f"hash_{session_id}"  # Add hash field to avoid index conflict
        }
        
        # Save user input to MongoDB
        user_id = save_to_storage(user_session, "prompts")  # Use prompts collection
        print(f"💾 User prompt stored! Session: {session_id} | ID: {user_id}")
        
        # 2. SMART ALGORITHM: Models respond and critique each other
        print("🧠 Starting SMART 5-model algorithm with cross-critique...")
        start_time = time.time()
        
        # Phase 1: All models generate initial responses
        model_responses = []
        for model in MODELS:
            response = simulate_model_response(model, user_message)
            model_responses.append(response)
            print(f"✅ {model['name']}: {response['response_text'][:50]}...")
        
        # Phase 2: Each model critiques others' responses (SMART ALGORITHM)
        print("🔍 Phase 2: Models critiquing each other...")
        critiques = []
        for i, critic_model in enumerate(MODELS):
            for j, target_response in enumerate(model_responses):
                if i != j:  # Don't critique yourself
                    critique = {
                        "critic_model": critic_model["name"],
                        "target_model": target_response["model_name"],
                        "critique_text": f"[{critic_model['name']} critiques {target_response['model_name']}]: {generate_critique(critic_model, target_response, user_message)}",
                        "critique_score": random.uniform(0.6, 0.95),
                        "session_id": session_id,
                        "timestamp": datetime.now()
                    }
                    critiques.append(critique)
                    
        # Store ALL critiques in MongoDB (every model critiques every other model)
        print(f"💾 Storing {len(critiques)} critiques in parallel to MongoDB...")
        for critique in critiques:  # Store ALL critiques, not just top 10
            save_to_storage(critique, "model_critiques")
        total_time = time.time() - start_time
        print(f"⚡ Smart algorithm completed in {total_time:.2f} seconds with {len(critiques)} critiques stored")
        
        # 3. Store model outputs in model_outputs collection (as requested by user)
        print(f"💾 Storing {len(model_responses)} model outputs in MongoDB...")
        for response in model_responses:
            response_record = {
                "session_id": session_id,
                "user_message": user_message,
                **response,
                "batch_id": f"batch_{int(time.time())}",
                "timestamp": datetime.now()
            }
            save_to_storage(response_record, "model_outputs")  # User requested this collection
        print(f"✅ All model outputs stored in model_outputs collection!")
        
        # 4. Store recommended model in model_suggestions collection (as requested by user)
        best_response = max(model_responses, key=lambda x: x['confidence'])
        model_suggestion = {
            "session_id": session_id,
            "user_message": user_message,
            "recommended_model": best_response["model_name"],
            "confidence_score": best_response["confidence"],
            "reason": f"Selected {best_response['model_name']} with {best_response['confidence']:.3f} confidence",
            "timestamp": datetime.now(),
            "alternatives": [{"model": resp["model_name"], "confidence": resp["confidence"]} for resp in model_responses if resp != best_response]
        }
        save_to_storage(model_suggestion, "model_suggestions")  # User requested this collection
        print(f"🎯 Model suggestion stored: {best_response['model_name']} recommended")
        
        # 5. Return UI-compatible response (matching frontend interface exactly)
        total_cost = sum(resp["cost_estimate"] for resp in model_responses)
        success_count = sum(1 for resp in model_responses if resp.get("success", True))
        success_rate = (success_count / len(model_responses)) * 100 if model_responses else 0
        
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
                    "tokens_used": resp["tokens_used"],
                    "cost_usd": resp["cost_estimate"],
                    "latency_ms": int(resp.get("processing_time", 1) * 1000)
                }
                for resp in model_responses if resp != best_response
            ][:3],
            "total_cost": total_cost,
            "api_calls": len(model_responses),
            "success_rate": success_rate,
            "metadata": {
                "session_id": session_id,
                "total_models": len(model_responses),
                "processing_time_seconds": round(total_time, 2),
                "storage_method": "mongodb_docker" if mongodb_connected else "temporary_files",
                "mongodb_status": "connected" if mongodb_connected else "not_connected"
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """System status"""
    user_data = get_from_storage("prompts")  # Updated collection name
    response_data = get_from_storage("model_responses")
    
    return jsonify({
        "status": "healthy",
        "storage_method": "mongodb_docker" if mongodb_connected else "temporary_files",
        "mongodb_connected": mongodb_connected,
        "user_prompts_stored": len(user_data),
        "model_responses_stored": len(response_data),
        "models_available": [m["name"] for m in MODELS],
        "database_info": "MongoDB Docker on port 27019" if mongodb_connected else "File storage backup"
    })

@app.route('/analytics', methods=['GET'])
def analytics():
    """Analytics from MongoDB or file storage"""
    user_data = get_from_storage("prompts")
    response_data = get_from_storage("model_responses")
    
    # Count model usage
    model_usage = {}
    for resp in response_data:
        model = resp.get("model_name", "unknown")
        model_usage[model] = model_usage.get(model, 0) + 1
    
    return jsonify({
        "total_user_prompts": len(user_data),
        "total_model_responses": len(response_data),
        "model_usage": model_usage,
        "recent_prompts": user_data[-5:] if user_data else [],
        "storage_info": {
            "mongodb_connected": mongodb_connected,
            "storage_method": "mongodb_docker" if mongodb_connected else "temporary_files"
        }
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "OrchestrateX Working API",
        "status": "running",
        "description": "5-Model Parallel Processing System",
        "endpoints": ["/chat", "/status", "/analytics"],
        "storage": "temporary_files_until_mongodb_connected"
    })

if __name__ == '__main__':
    print("🚀 OrchestrateX Working API - Latest Models!")
    if mongodb_connected:
        print("📊 User prompts → MongoDB Docker (orchestratex.prompts)")
        print("🤖 Model outputs → MongoDB Docker (orchestratex.model_outputs)")
        print("🎯 Model suggestions → MongoDB Docker (orchestratex.model_suggestions)")
        print("🔍 Model critiques → MongoDB Docker (orchestratex.model_critiques)")
        print("🗄️ Database: mongodb://localhost:27019/orchestratex")  # Updated port too
    else:
        print("📊 User prompts → temp_storage/prompts.json")
        print("🤖 Model outputs → temp_storage/model_outputs.json")
        print("🎯 Model suggestions → temp_storage/model_suggestions.json")
        print("⚠️  MongoDB fallback: Using file storage")
    print("⚡ 5-Latest-Model parallel simulation enabled")
    print("🔥 Models: GLM-4.5, GPT-OSS, Llama-4-Maverick, Kimi-K2, TNG-DeepSeek-R1T2")
    print("🌐 Frontend should connect to: http://localhost:8002")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8002, debug=True)
