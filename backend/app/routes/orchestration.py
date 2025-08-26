"""
Orchestration management routes for OrchestrateX API
Enhanced with full orchestration engine integration
"""

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging
from bson import ObjectId

from app.models.schemas import (
    OrchestrationRequest,
    OrchestrationStatus,
    ThreadStatus
)
from app.core.database import get_database
from app.orchestration.engine import orchestration_engine
from app.ai_providers import provider_manager

router = APIRouter()

class PromptRequest(BaseModel):
    session_id: str
    prompt: str
    max_iterations: int = 5
    quality_threshold: float = 0.8
    cost_limit: Optional[float] = None

class IterationRequest(BaseModel):
    thread_id: str
    feedback: Optional[str] = None

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

@router.post("/prompt")
async def submit_prompt_for_orchestration(request: PromptRequest, background_tasks: BackgroundTasks, db=Depends(get_db)):
    """Submit a prompt for orchestrated multi-AI processing"""
    try:
        logging.info(f"Received orchestration request: {request.prompt[:50]}...")
        
        # Initialize orchestration engine if not already done
        if orchestration_engine.db is None:
            await orchestration_engine.initialize()
        
        # Start orchestration process
        result = await orchestration_engine.orchestrate_prompt(
            session_id=request.session_id,
            prompt=request.prompt,
            max_iterations=request.max_iterations,
            quality_threshold=request.quality_threshold
        )
        
        return {
            "status": "success",
            "message": "Orchestration completed",
            "result": result
        }
        
    except Exception as e:
        logging.error(f"Failed to process orchestration request: {e}")
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")

@router.get("/status/{thread_id}")
async def get_orchestration_status(thread_id: str, db=Depends(get_db)):
    """Get orchestration status for a thread"""
    try:
        thread = await db.conversation_threads.find_one({"_id": ObjectId(thread_id)})
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        # Get latest responses
        responses = await db.model_responses.find(
            {"thread_id": thread_id}
        ).sort("iteration_number", -1).limit(5).to_list(5)
        
        # Get evaluations
        evaluations = await db.model_evaluations.find(
            {"thread_id": thread_id}
        ).sort("iteration_number", -1).limit(3).to_list(3)
        
        return {
            "thread_id": thread_id,
            "status": thread.get("thread_status", "unknown"),
            "iterations_used": thread.get("iterations_used", 0),
            "current_quality_score": thread.get("final_quality_score", 0.0),
            "recent_responses": [
                {
                    "iteration": r["iteration_number"],
                    "model": r["model_name"],
                    "response_preview": r["response_text"][:200] + "..." if len(r["response_text"]) > 200 else r["response_text"],
                    "quality": next((e["overall_score"] for e in evaluations if e.get("iteration_number") == r["iteration_number"]), None)
                }
                for r in responses
            ],
            "last_updated": thread.get("updated_at", datetime.utcnow()).isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get orchestration status for {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

@router.post("/iteration")
async def trigger_next_iteration(request: IterationRequest, db=Depends(get_db)):
    """Trigger next iteration of orchestration"""
    try:
        # This would be implemented to manually trigger next iteration
        return {
            "status": "success",
            "message": "Next iteration triggered",
            "thread_id": request.thread_id,
            "feedback_applied": request.feedback is not None
        }
        
    except Exception as e:
        logging.error(f"Failed to trigger iteration: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to trigger iteration: {str(e)}")

@router.put("/stop/{thread_id}")
async def stop_orchestration(thread_id: str, db=Depends(get_db)):
    """Stop orchestration process"""
    try:
        result = await db.conversation_threads.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$set": {
                    "thread_status": "stopped",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        return {
            "status": "success",
            "message": f"Orchestration stopped for thread {thread_id}"
        }
        
    except Exception as e:
        logging.error(f"Failed to stop orchestration for {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stop orchestration: {str(e)}")

@router.get("/models/health")
async def check_models_health():
    """Check the health status of all AI providers"""
    try:
        # Initialize providers if not already done
        if not provider_manager.providers:
            await provider_manager.initialize_providers()
        
        health_status = await provider_manager.check_all_providers_health()
        
        return {
            "status": "success",
            "providers_health": health_status,
            "healthy_count": sum(1 for status in health_status.values() if status),
            "total_count": len(health_status),
            "check_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.post("/test")
async def test_orchestration():
    """Test endpoint for orchestration system"""
    try:
        # Initialize if needed
        if orchestration_engine.db is None:
            await orchestration_engine.initialize()
        
        # Test with a simple prompt
        test_session_id = "test_session_" + datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        result = await orchestration_engine.orchestrate_prompt(
            session_id=test_session_id,
            prompt="Hello, please introduce yourself and explain what you can do.",
            max_iterations=2,
            quality_threshold=0.7
        )
        
        return {
            "status": "success",
            "message": "Orchestration test completed",
            "test_result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")
