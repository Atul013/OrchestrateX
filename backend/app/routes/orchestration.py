"""
Orchestration management routes for OrchestrateX API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
import logging
from bson import ObjectId

from app.models.schemas import (
    OrchestrationRequest,
    OrchestrationStatus,
    ThreadStatus
)
from app.core.database import get_database

router = APIRouter()

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

@router.post("/prompt")
async def submit_prompt_for_orchestration(request: OrchestrationRequest, db=Depends(get_db)):
    """Submit a prompt for orchestrated multi-AI processing"""
    try:
        # TODO: Implement full orchestration workflow
        # For now, create a basic response structure
        
        logging.info(f"Received orchestration request: {request.prompt[:50]}...")
        
        return {
            "message": "Orchestration request received",
            "prompt": request.prompt,
            "domain": request.domain,
            "max_iterations": request.max_iterations,
            "status": "processing",
            "estimated_completion": "2-5 minutes"
        }
        
    except Exception as e:
        logging.error(f"Failed to process orchestration request: {e}")
        raise HTTPException(status_code=500, detail="Failed to process orchestration request")

@router.get("/status/{thread_id}", response_model=OrchestrationStatus)
async def get_orchestration_status(thread_id: str, db=Depends(get_db)):
    """Get orchestration status for a thread"""
    try:
        thread = await db.conversation_threads.find_one({"_id": ObjectId(thread_id)})
        
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        # Calculate progress percentage
        current_iteration = thread.get("current_iteration", 0)
        max_iterations = thread.get("max_iterations", 5)
        progress = min((current_iteration / max_iterations) * 100, 100)
        
        return OrchestrationStatus(
            thread_id=thread_id,
            status=thread.get("thread_status", ThreadStatus.INITIALIZING),
            current_iteration=current_iteration,
            max_iterations=max_iterations,
            progress_percentage=progress,
            current_best_response=thread.get("final_response"),
            total_cost_so_far=thread.get("total_cost", 0.0)
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid thread ID format")
    except Exception as e:
        logging.error(f"Failed to get orchestration status for {thread_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve orchestration status")

@router.post("/iteration")
async def trigger_next_iteration(thread_id: str, db=Depends(get_db)):
    """Trigger next iteration of orchestration"""
    try:
        # TODO: Implement iteration triggering logic
        
        result = await db.conversation_threads.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$inc": {"current_iteration": 1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        return {"message": "Next iteration triggered successfully"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid thread ID format")
    except Exception as e:
        logging.error(f"Failed to trigger iteration for {thread_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger iteration")

@router.put("/stop/{thread_id}")
async def stop_orchestration(thread_id: str, db=Depends(get_db)):
    """Stop orchestration process"""
    try:
        result = await db.conversation_threads.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$set": {
                    "thread_status": ThreadStatus.COMPLETED,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        return {"message": "Orchestration stopped successfully"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid thread ID format")
    except Exception as e:
        logging.error(f"Failed to stop orchestration for {thread_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop orchestration")
