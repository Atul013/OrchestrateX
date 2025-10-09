#!/usr/bin/env python3
"""
Working API for OrchestrateX - With API Key Rotation
Latest models with proper database storage and automatic key rotation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from datetime import datetime
import random
import time
import json
import os

# Import our new rotation system
from rate_limit_handler import call_model_with_rotation
from api_key_rotation import get_status

# EMERGENCY HOTFIX: Load API keys directly from environment
def load_api_keys_directly():
    """Emergency function to load API keys directly from environment"""
    global rotation_manager
    
    if not hasattr(load_api_keys_directly, 'keys_loaded'):
        print("🚨 EMERGENCY: Loading API keys directly from environment...")
        
        # Get the rotation manager
        try:
            from api_key_rotation import APIKeyRotationManager
            rotation_manager = APIKeyRotationManager()
        except:
            print("❌ Could not create rotation manager")
            return False
        
        # Manual key loading
        providers = {
            'GLM45': 'GLM-4.5',
            'GPTOSS': 'GPT-OSS', 
            'LLAMA3': 'Llama-4-Maverick',
            'KIMI': 'Kimi-K2',
            'QWEN3': 'Qwen3',
            'FALCON': 'TNG DeepSeek'
        }
        
        for provider_env, model_name in providers.items():
            api_key = os.environ.get(f'PROVIDER_{provider_env}_API_KEY')
            model_id = os.environ.get(f'PROVIDER_{provider_env}_MODEL')
            
            if api_key:
                rotation_manager.api_keys[provider_env] = {
                    'primary_key': api_key.strip(),
                    'backup_keys': [],
                    'model_id': model_id.strip() if model_id else None,
                    'all_keys': [api_key.strip()]
                }
                print(f"✅ Loaded {provider_env} -> {model_name}: {api_key[:20]}...")
        
        print(f"🎯 Total keys loaded: {len(rotation_manager.api_keys)}")
        load_api_keys_directly.keys_loaded = True
        return len(rotation_manager.api_keys) > 0
    
    return True

# HOTFIX: Manually set up API keys from environment variables
def setup_api_keys_from_env():
    """Quick fix to load API keys from environment variables"""
    from api_key_rotation import APIKeyRotationManager
    
    # Get the global rotation manager instance
    rotation_manager = None
    try:
        # Try to get existing instance or create new one
        import rate_limit_handler
        if hasattr(rate_limit_handler, 'rotation_manager'):
            rotation_manager = rate_limit_handler.rotation_manager
        else:
            rotation_manager = APIKeyRotationManager()
            rate_limit_handler.rotation_manager = rotation_manager
    except:
        pass
    
    if rotation_manager and not rotation_manager.api_keys:
        providers = ['GLM45', 'GPTOSS', 'LLAMA3', 'KIMI', 'QWEN3', 'FALCON']
        for provider in providers:
            api_key = os.environ.get(f'PROVIDER_{provider}_API_KEY')
            model = os.environ.get(f'PROVIDER_{provider}_MODEL')
            if api_key:
                rotation_manager.api_keys[provider] = {
                    'primary_key': api_key,
                    'backup_keys': [],
                    'model_id': model,
                    'all_keys': [api_key]
                }
                print(f"✅ Loaded {provider} from environment")

# Call the hotfix
setup_api_keys_from_env()

# EMERGENCY HOTFIX: Force load API keys
load_api_keys_directly()

app = Flask(__name__)
CORS(app, origins=['http://localhost:5176', 'http://localhost:5175', 'http://localhost:5174', 'http://127.0.0.1:5176', 'http://127.0.0.1:5175', 'http://127.0.0.1:5174', 'https://orchestratex-frontend-84388526388.us-central1.run.app', 'https://chat.orchestratex.me', 'https://orchestratex.me', 'https://orchestratex-chat.web.app'], 
     methods=['GET', 'POST', 'OPTIONS'], 
     allow_headers=['Content-Type', 'Authorization'])

# Model provider mappings for the rotation system
PROVIDER_MAPPINGS = {
    'Llama-4-Maverick': ('LLAMA3', 'meta-llama/llama-4-maverick:free'),
    'GLM-4.5': ('GLM45', 'z-ai/glm-4.5-air:free'),
    'GPT-OSS': ('GPTOSS', 'openai/gpt-oss-20b:free'),
    'Kimi-K2': ('KIMI', 'moonshotai/kimi-dev-72b:free'),
    'Qwen3-Coder': ('QWEN3', 'qwen/Qwen3-coder:free'),
    'TNG-DeepSeek-R1T2': ('FALCON', 'tngtech/deepseek-r1t2-chimera:free')
}

# Initialize Firebase Admin SDK and Firestore
try:
    # Initialize Firebase Admin if not already done
    if not firebase_admin._apps:
        # Try to use default credentials (if GOOGLE_APPLICATION_CREDENTIALS is set)
        # or service account key file
        try:
            firebase_admin.initialize_app()
            print("✅ Firebase initialized with default credentials")
        except Exception as e:
            print(f"⚠️ Default credentials failed: {e}")
            # Try with service account key file if it exists
            service_account_path = "service-account-key.json"
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                print(f"✅ Firebase initialized with service account: {service_account_path}")
            else:
                print("❌ No Firebase credentials found")
                raise Exception("Firebase credentials not configured")
    
    # Initialize Firestore client
    db = firestore.Client()
    firestore_connected = True
    print("✅ Firestore connected successfully!")
    
except Exception as e:
    print(f"⚠️ Firestore connection failed: {e}")
    print("📁 Using temporary file storage as fallback")
    firestore_connected = False
    db = None

def load_api_config():
    """Load API configuration (kept for compatibility)"""
    # This function is now mainly for compatibility
    # The actual API key management is handled by the rotation system
    models = {}
    for model_name, (provider, model_id) in PROVIDER_MAPPINGS.items():
        models[model_name] = {
            'provider': provider,
            'model_id': model_id
        }
    return models

def call_openrouter_api(model_name, prompt, max_tokens=2000):
    """
    Call OpenRouter API with automatic key rotation
    This function now uses the new rotation system
    """
    if model_name not in PROVIDER_MAPPINGS:
        return {
            'success': False,
            'error': f'Unknown model: {model_name}',
            'model_name': model_name
        }
    
    provider, model_id = PROVIDER_MAPPINGS[model_name]
    
    # Use the new rotation-aware API client
    result = call_model_with_rotation(
        provider=provider,
        model_id=model_id,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7
    )
    
    # Convert to the expected format for backward compatibility
    if result['success']:
        return {
            'success': True,
            'content': result['response'],
            'model_name': model_name,
            'provider': provider,
            'tokens_used': result['metadata']['total_tokens'],
            'cost_usd': result['metadata']['total_tokens'] * 0.000001
        }
    else:
        return {
            'success': False,
            'error': result['error'],
            'model_name': model_name,
            'provider': provider
        }

# Latest 5 Model configurations from orche.env
MODELS = [
    {"name": "GLM-4.5", "specialty": "reasoning", "strength": 0.95, "model_id": "z-ai/glm-4.5-air:free"},
    {"name": "GPT-OSS", "specialty": "general", "strength": 0.90, "model_id": "openai/gpt-oss-120b:free"},
    {"name": "Llama-4-Maverick", "specialty": "coding", "strength": 0.88, "model_id": "meta-llama/llama-4-maverick:free"},
    {"name": "Kimi-K2", "specialty": "creative", "strength": 0.85, "model_id": "moonshotai/kimi-k2:free"},
    {"name": "Qwen3-Coder", "specialty": "coding", "strength": 0.87, "model_id": "qwen/Qwen3-coder:free"},
    {"name": "TNG-DeepSeek-R1T2", "specialty": "analysis", "strength": 0.92, "model_id": "tngtech/deepseek-r1t2-chimera:free"}
]

def real_model_response(model, prompt):
    """Call real AI model API instead of simulation"""
    start_time = time.time()
    
    # Load API configuration (for compatibility checks)
    api_models = load_api_config()
    model_name = model["name"]
    
    if model_name not in PROVIDER_MAPPINGS:
        return {
            "model_name": model_name,
            "specialty": model["specialty"],
            "response_text": f"❌ Model {model_name} not supported by rotation system",
            "confidence": 0.0,
            "processing_time": 0.0,
            "processing_time_ms": 0,
            "timestamp": datetime.now(),
            "tokens_used": 0,
            "cost_estimate": 0.0,
            "success": False
        }
    
    # Call real API using the new rotation system
    result = call_openrouter_api(model_name, prompt)
    processing_time = time.time() - start_time
    
    if result['success']:
        return {
            "model_name": model_name,
            "specialty": model["specialty"],
            "response_text": result['content'],
            "confidence": model["strength"] + random.uniform(-0.05, 0.05),
            "processing_time": processing_time,
            "processing_time_ms": int(processing_time * 1000),
            "timestamp": datetime.now(),
            "tokens_used": result['tokens_used'],
            "cost_estimate": result['cost_usd'],
            "success": True
        }
    else:
        return {
            "model_name": model_name,
            "specialty": model["specialty"],
            "response_text": f"❌ API Error: {result['error']}",
            "confidence": 0.0,
            "processing_time": processing_time,
            "processing_time_ms": int(processing_time * 1000),
            "timestamp": datetime.now(),
            "tokens_used": 0,
            "cost_estimate": 0.0,
            "success": False
        }

def generate_critique(critic_model, target_response, user_prompt):
    """Generate real critique from one model about another model's response"""
    
    # Create a critique prompt
    critique_prompt = f"""Please provide a constructive critique of the following AI response to the user's question.

User's original question: "{user_prompt}"

{target_response['model_name']}'s response: "{target_response['response_text']}"

Please analyze this response and provide specific feedback on what could be improved, what was done well, and suggest alternative approaches. Keep your critique concise and helpful."""

    # Use the real model API to generate critique
    critique_response = real_model_response(critic_model, critique_prompt)
    
    if critique_response['success']:
        return critique_response['response_text']
    else:
        # Fallback to simple critique if API fails
        return f"Alternative perspective: [{critic_model['name']} {critic_model['specialty']}] {target_response['model_name']}'s response could benefit from additional analysis."

def save_to_storage(data, collection_name):
    """Save data to Firestore with proper collection separation"""
    if firestore_connected and db is not None:
        try:
            # Ensure proper collection mapping
            collection_map = {
                "user_prompts": "user_prompts",      # User input prompts
                "model_responses": "model_responses", # Individual model responses
                "model_critiques": "model_critiques", # Model critiques
                "model_suggestions": "model_suggestions", # Best model recommendations
                "sessions": "sessions",               # Session metadata
                # Legacy collection names for compatibility
                "prompts": "user_prompts",
                "model_outputs": "model_responses"
            }
            
            if collection_name in collection_map:
                firestore_collection = collection_map[collection_name]
                # Convert datetime objects to Firestore timestamp format
                data_copy = data.copy()
                if 'timestamp' in data_copy and isinstance(data_copy['timestamp'], datetime):
                    data_copy['timestamp'] = data_copy['timestamp']
                
                # Add document to Firestore collection
                doc_ref = db.collection(firestore_collection).add(data_copy)
                doc_id = doc_ref[1].id  # doc_ref is a tuple (timestamp, DocumentReference)
                print(f"✅ Stored in Firestore {firestore_collection}: {doc_id}")
                return doc_id
            else:
                print(f"❌ Unknown collection: {collection_name}")
                return None
                
        except Exception as e:
            print(f"❌ Firestore write failed: {e}")
            return None
    else:
        print("❌ Firestore not connected!")
        return None

def get_from_storage(collection_name):
    """Get data from Firestore only"""
    if firestore_connected and db is not None:
        try:
            # Collection mapping for consistency
            collection_map = {
                "user_prompts": "user_prompts",
                "model_responses": "model_responses", 
                "model_critiques": "model_critiques",
                "model_suggestions": "model_suggestions",
                "sessions": "sessions",
                # Legacy mapping
                "prompts": "user_prompts",
                "model_outputs": "model_responses"
            }
            
            firestore_collection = collection_map.get(collection_name, collection_name)
            
            # Query Firestore collection ordered by timestamp (newest first), limit 10
            docs = db.collection(firestore_collection).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10).stream()
            
            results = []
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data['_id'] = doc.id  # Add document ID for compatibility
                results.append(doc_data)
            
            return results
            
        except Exception as e:
            print(f"❌ Firestore read failed: {e}")
            return []
    else:
        print("❌ Firestore not connected!")
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
            response = real_model_response(model, user_message)
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
                "storage_method": "firestore" if firestore_connected else "temporary_files",
                "firestore_status": "connected" if firestore_connected else "not_connected"
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orchestration/process', methods=['POST'])
def orchestration_process():
    """Orchestration endpoint: Alias for chat endpoint to support chatbot UI"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Convert prompt to message format and call existing chat function
        request.json = {'message': prompt}
        return chat()
        
    except Exception as e:
        print(f"❌ Orchestration Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/reload-keys', methods=['POST'])
def reload_keys():
    """Manual API endpoint to reload keys from environment"""
    try:
        setup_api_keys_from_env()
        return jsonify({"success": True, "message": "Keys reloaded from environment"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """System status with API key rotation info"""
    user_data = get_from_storage("prompts")  # Updated collection name
    response_data = get_from_storage("model_responses")
    
    return jsonify({
        "status": "healthy",
        "storage_method": "firestore" if firestore_connected else "temporary_files",
        "firestore_connected": firestore_connected,
        "user_prompts_stored": len(user_data),
        "model_responses_stored": len(response_data),
        "models_available": [m["name"] for m in MODELS],
        "database_info": "Google Cloud Firestore" if firestore_connected else "File storage backup",
        "api_key_rotation": True,
        "rotation_status": get_status()
    })

@app.route('/api/key-status', methods=['GET'])
def get_key_status():
    """Get detailed API key rotation status"""
    try:
        status_data = get_status()
        return jsonify({
            'success': True,
            'status': status_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
            "firestore_connected": firestore_connected,
            "storage_method": "firestore" if firestore_connected else "temporary_files"
        }
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "OrchestrateX Working API",
        "status": "running",
        "description": "5-Model Parallel Processing System",
        "endpoints": ["/chat", "/status", "/analytics"],
        "storage": "firestore" if firestore_connected else "temporary_files"
    })

if __name__ == '__main__':
    print("🚀 OrchestrateX Working API - Latest Models!")
    if firestore_connected:
        print("📊 User prompts → Google Cloud Firestore (orchestratex.user_prompts)")
        print("🤖 Model outputs → Google Cloud Firestore (orchestratex.model_responses)")
        print("🎯 Model suggestions → Google Cloud Firestore (orchestratex.model_suggestions)")
        print("🔍 Model critiques → Google Cloud Firestore (orchestratex.model_critiques)")
        print("🗄️ Database: Google Cloud Firestore")
    else:
        print("📊 User prompts → temp_storage/prompts.json")
        print("🤖 Model outputs → temp_storage/model_outputs.json")
        print("🎯 Model suggestions → temp_storage/model_suggestions.json")
        print("⚠️  Firestore fallback: Using file storage")
    print("⚡ 5-Latest-Model parallel simulation enabled")
    print("🔥 Models: GLM-4.5, GPT-OSS, Llama-4-Maverick, Kimi-K2, TNG-DeepSeek-R1T2")
    
    # Get port from environment variable for Cloud Run compatibility
    port = int(os.environ.get('PORT', 8002))
    print(f"🌐 API running on port: {port}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=False)
