"""
Session management routes for OrchestrateX API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
import logging
from bson import ObjectId

from app.models.schemas import (
    UserSessionCreate, 
    UserSessionResponse, 
    SessionStatus
)
from app.core.database import get_database

router = APIRouter()

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

@router.post("/", response_model=UserSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: UserSessionCreate, db=Depends(get_db)):
    """Create a new user session"""
    try:
        session_doc = {
            "user_id": session_data.user_id,
            "session_start": datetime.utcnow(),
            "session_end": None,
            "max_iterations": session_data.max_iterations,
            "status": SessionStatus.ACTIVE,
            "total_cost": 0.0,
            "user_satisfaction": None,
            "settings": session_data.settings or {
                "preferred_models": [],
                "excluded_models": [],
                "cost_limit": 10.0,
                "quality_threshold": 8.0
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.user_sessions.insert_one(session_doc)
        
        # Retrieve the created session
        created_session = await db.user_sessions.find_one({"_id": result.inserted_id})
        created_session["_id"] = str(created_session["_id"])
        
        logging.info(f"Created session {result.inserted_id} for user {session_data.user_id}")
        return created_session
        
    except Exception as e:
        logging.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")

@router.get("/{session_id}", response_model=UserSessionResponse)
async def get_session(session_id: str, db=Depends(get_db)):
    """Get session details by ID"""
    try:
        session = await db.user_sessions.find_one({"_id": ObjectId(session_id)})
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session["_id"] = str(session["_id"])
        return session
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except Exception as e:
        logging.error(f"Failed to get session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve session")

@router.get("/user/{user_id}", response_model=List[UserSessionResponse])
async def get_user_sessions(user_id: str, db=Depends(get_db)):
    """Get all sessions for a user"""
    try:
        cursor = db.user_sessions.find(
            {"user_id": user_id}
        ).sort("session_start", -1)
        
        sessions = []
        async for session in cursor:
            session["_id"] = str(session["_id"])
            sessions.append(session)
        
        return sessions
        
    except Exception as e:
        logging.error(f"Failed to get sessions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user sessions")

@router.put("/{session_id}/settings")
async def update_session_settings(session_id: str, settings: dict, db=Depends(get_db)):
    """Update session settings"""
    try:
        result = await db.user_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "settings": settings,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session settings updated successfully"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except Exception as e:
        logging.error(f"Failed to update session {session_id} settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update session settings")

@router.delete("/{session_id}")
async def end_session(session_id: str, db=Depends(get_db)):
    """End a session"""
    try:
        result = await db.user_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "status": SessionStatus.COMPLETED,
                    "session_end": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session ended successfully"}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    except Exception as e:
        logging.error(f"Failed to end session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to end session")
