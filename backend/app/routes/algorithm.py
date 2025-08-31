"""
Algorithm Integration Routes for OrchestrateX Backend
Integrates ModelSelector algorithm with existing database
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from datetime import datetime
import logging
import os
import sys
from bson import ObjectId

# Add Model directory to path to import your algorithm
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Model")
sys.path.append(model_path)

try:
    from model_selector import ModelSelector
    import joblib
    model_available = True
except ImportError:
    logging.warning("ModelSelector not available")
    model_available = False

from app.core.database import get_database
from pydantic import BaseModel

router = APIRouter()

# Global model instance
model_selector = None

class PredictRequest(BaseModel):
    prompt: str
    user_id: str = "anonymous"

class ChatRequest(BaseModel):
    prompt: str
    user_id: str = "anonymous"
    session_id: str = None

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

def load_model():
    """Load your trained ModelSelector"""
    global model_selector
    try:
        model_path_file = os.path.join(model_path, "model_selector.pkl")
        if model_available and os.path.exists(model_path_file):
            model_selector = joblib.load(model_path_file)
            logging.info("✅ ModelSelector loaded successfully!")
            return True
        else:
            logging.error(f"❌ Model file not found: {model_path_file}")
            return False
    except Exception as e:
        logging.error(f"❌ Error loading model: {e}")
        return False

@router.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()

@router.get("/algorithm/health")
async def algorithm_health():
    """Check algorithm health status"""
    return {
        "algorithm_status": "loaded" if model_selector else "not_loaded",
        "model_available": model_available,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/algorithm/predict")
async def predict_best_model(request: PredictRequest, db=Depends(get_db)):
    """Use your algorithm to predict the best model for a prompt"""
    try:
        if not model_selector:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Use your ModelSelector algorithm
        prediction_result = model_selector.predict_best_model(request.prompt)
        
        # Store prediction in your existing algorithm_metrics collection
        metrics_doc = {
            "user_id": request.user_id,
            "prompt": request.prompt,
            "predicted_model": prediction_result['predicted_model'],
            "prediction_confidence": prediction_result['prediction_confidence'],
            "confidence_scores": prediction_result['confidence_scores'],
            "prompt_features": prediction_result['prompt_features'],
            "algorithm_version": "1.0",
            "created_at": datetime.utcnow()
        }
        
        result = await db.algorithm_metrics.insert_one(metrics_doc)
        
        return {
            "success": True,
            "prediction_id": str(result.inserted_id),
            "predicted_model": prediction_result['predicted_model'],
            "confidence": prediction_result['prediction_confidence'],
            "all_model_scores": prediction_result['confidence_scores'],
            "prompt_analysis": prediction_result['prompt_features']
        }
        
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/algorithm/chat")
async def handle_chat_with_algorithm(request: ChatRequest, db=Depends(get_db)):
    """Handle chat using your algorithm with existing database schema"""
    try:
        # Step 1: Create or get session
        session_doc = None
        if request.session_id:
            session_doc = await db.user_sessions.find_one({"_id": ObjectId(request.session_id)})
        
        if not session_doc:
            # Create new session
            session_doc = {
                "user_id": request.user_id,
                "session_start": datetime.utcnow(),
                "max_iterations": 5,
                "status": "active",
                "total_cost": 0.0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            session_result = await db.user_sessions.insert_one(session_doc)
            session_id = str(session_result.inserted_id)
        else:
            session_id = str(session_doc["_id"])
        
        # Step 2: Use your algorithm to choose the best model
        prediction_result = {}
        chosen_model = "fallback_model"
        confidence = 0.5
        
        if model_selector:
            prediction_result = model_selector.predict_best_model(request.prompt)
            chosen_model = prediction_result['predicted_model']
            confidence = prediction_result['prediction_confidence']
        
        # Step 3: Create conversation thread in your existing schema
        thread_doc = {
            "session_id": ObjectId(session_id),
            "original_prompt": request.prompt,
            "processed_prompt": request.prompt,
            "domain": prediction_result.get('prompt_features', {}).get('topic_domain', 'general'),
            "complexity_level": "moderate",
            "language": "en",
            "thread_status": "active",
            "total_iterations": 1,
            "current_iteration": 1,
            "algorithm_selection": {
                "selected_model": chosen_model,
                "confidence_score": confidence,
                "selection_reasoning": f"Algorithm selected based on prompt analysis",
                "all_scores": prediction_result.get('confidence_scores', {})
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        thread_result = await db.conversation_threads.insert_one(thread_doc)
        thread_id = str(thread_result.inserted_id)
        
        # Step 4: Generate response (placeholder - integrate with your actual models)
        response_text = f"Response from {chosen_model} (confidence: {confidence:.2f}): This is a simulated response to '{request.prompt[:50]}...'"
        
        # Step 5: Store model response in your existing schema
        response_doc = {
            "thread_id": ObjectId(thread_id),
            "model_name": chosen_model,
            "model_version": "latest",
            "provider": "algorithm_selected",
            "iteration_number": 1,
            "prompt_tokens": len(request.prompt.split()),
            "completion_tokens": len(response_text.split()),
            "total_tokens": len(request.prompt.split()) + len(response_text.split()),
            "response_text": response_text,
            "response_time": 0.5,
            "api_cost": 0.01,
            "confidence_score": confidence,
            "quality_metrics": {
                "coherence": 8.5,
                "relevance": 9.0,
                "accuracy": 8.0,
                "completeness": 8.5
            },
            "model_metadata": {
                "algorithm_choice": True,
                "confidence_scores": prediction_result.get('confidence_scores', {}),
                "prompt_features": prediction_result.get('prompt_features', {})
            },
            "created_at": datetime.utcnow()
        }
        
        response_result = await db.model_responses.insert_one(response_doc)
        
        # Step 6: Store algorithm metrics
        if model_selector:
            metrics_doc = {
                "user_id": request.user_id,
                "session_id": session_id,
                "thread_id": thread_id,
                "prompt": request.prompt,
                "predicted_model": chosen_model,
                "prediction_confidence": confidence,
                "confidence_scores": prediction_result.get('confidence_scores', {}),
                "prompt_features": prediction_result.get('prompt_features', {}),
                "actual_model_used": chosen_model,
                "prediction_correct": True,
                "algorithm_version": "1.0",
                "created_at": datetime.utcnow()
            }
            await db.algorithm_metrics.insert_one(metrics_doc)
        
        return {
            "success": True,
            "session_id": session_id,
            "thread_id": thread_id,
            "response_id": str(response_result.inserted_id),
            "response": response_text,
            "model_used": chosen_model,
            "confidence": confidence,
            "stored_in_existing_db": True
        }
        
    except Exception as e:
        logging.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/algorithm/analytics")
async def get_algorithm_analytics(limit: int = 10, db=Depends(get_db)):
    """Get algorithm analytics from your existing database"""
    try:
        cursor = db.algorithm_metrics.find().sort("created_at", -1).limit(limit)
        analytics = []
        
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc:
                doc['created_at'] = doc['created_at'].isoformat()
            analytics.append(doc)
        
        return {
            "success": True,
            "analytics": analytics,
            "count": len(analytics)
        }
        
    except Exception as e:
        logging.error(f"Error fetching analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/algorithm/conversations")
async def get_algorithm_conversations(user_id: str = None, limit: int = 10, db=Depends(get_db)):
    """Get conversations with algorithm selections from your existing database"""
    try:
        query = {}
        if user_id:
            # Find sessions for this user first
            sessions_cursor = db.user_sessions.find({"user_id": user_id}, {"_id": 1})
            session_ids = [session["_id"] async for session in sessions_cursor]
            query["session_id"] = {"$in": session_ids}
        
        cursor = db.conversation_threads.find(query).sort("created_at", -1).limit(limit)
        conversations = []
        
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            doc['session_id'] = str(doc['session_id'])
            if 'created_at' in doc:
                doc['created_at'] = doc['created_at'].isoformat()
            conversations.append(doc)
        
        return {
            "success": True,
            "conversations": conversations,
            "count": len(conversations)
        }
        
    except Exception as e:
        logging.error(f"Error fetching conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
