"""
Conversation threads management routes for OrchestrateX API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
import logging
from bson import ObjectId

from app.models.schemas import (
    ConversationThreadCreate, 
    ConversationThreadResponse,
    ThreadStatus
)
from app.core.database import get_database

router = APIRouter()

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

@router.post("/", response_model=ConversationThreadResponse, status_code=status.HTTP_201_CREATED)
async def create_thread(thread_data: ConversationThreadCreate, db=Depends(get_db)):
    """Create a new conversation thread"""
    try:
        thread_doc = {
            "session_id": thread_data.session_id,
            "original_prompt": thread_data.original_prompt,
            "processed_prompt": thread_data.original_prompt,  # TODO: Add prompt processing
            "domain": thread_data.domain,
            "context": thread_data.context,
            "current_iteration": 0,
            "max_iterations_reached": False,
            "best_model_id": None,
            "best_response_id": None,
            "thread_status": ThreadStatus.INITIALIZING,
            "final_response": None,
            "final_quality_score": None,
            "total_cost": 0.0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.conversation_threads.insert_one(thread_doc)
        
        # Retrieve the created thread
        created_thread = await db.conversation_threads.find_one({"_id": result.inserted_id})
        created_thread["_id"] = str(created_thread["_id"])
        
        logging.info(f"Created thread {result.inserted_id} for session {thread_data.session_id}")
        return created_thread
        
    except Exception as e:
        logging.error(f"Failed to create thread: {e}")
        raise HTTPException(status_code=500, detail="Failed to create thread")

@router.get("/{thread_id}", response_model=ConversationThreadResponse)
async def get_thread(thread_id: str, db=Depends(get_db)):
    """Get thread details by ID"""
    try:
        thread = await db.conversation_threads.find_one({"_id": ObjectId(thread_id)})
        
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        thread["_id"] = str(thread["_id"])
        return thread
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid thread ID format")
    except Exception as e:
        logging.error(f"Failed to get thread {thread_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve thread")

@router.get("/session/{session_id}", response_model=List[ConversationThreadResponse])
async def get_session_threads(session_id: str, db=Depends(get_db)):
    """Get all threads for a session"""
    try:
        cursor = db.conversation_threads.find(
            {"session_id": session_id}
        ).sort("created_at", -1)
        
        threads = []
        async for thread in cursor:
            thread["_id"] = str(thread["_id"])
            threads.append(thread)
        
        return threads
        
    except Exception as e:
        logging.error(f"Failed to get threads for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session threads")

@router.put("/{thread_id}/status")
async def update_thread_status(thread_id: str, status: ThreadStatus, db=Depends(get_db)):
    """Update thread status"""
    try:
        result = await db.conversation_threads.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$set": {
                    "thread_status": status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        return {"message": "Thread status updated successfully"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid thread ID format")
    except Exception as e:
        logging.error(f"Failed to update thread {thread_id} status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update thread status")
