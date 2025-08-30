"""
CRUD operations for user sessions
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.schemas import UserSessionCreate, UserSessionResponse, SessionStatus

class SessionCRUD:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.user_sessions
    
    async def create_session(self, session_data: UserSessionCreate) -> str:
        """Create a new user session"""
        session_doc = {
            "user_id": session_data.user_id,
            "session_start": datetime.utcnow(),
            "max_iterations": session_data.max_iterations,
            "status": SessionStatus.ACTIVE,
            "total_cost": 0.0,
            "settings": session_data.settings or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(session_doc)
        return str(result.inserted_id)
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        session = await self.collection.find_one({"_id": ObjectId(session_id)})
        return session
    
    async def list_user_sessions(
        self, 
        user_id: str, 
        status: Optional[SessionStatus] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List sessions for a user"""
        filter_query = {"user_id": user_id}
        if status:
            filter_query["status"] = status
        
        cursor = self.collection.find(filter_query).sort("session_start", -1).limit(limit)
        sessions = await cursor.to_list(length=None)
        return sessions
    
    async def update_session_status(self, session_id: str, status: SessionStatus) -> bool:
        """Update session status"""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        if status in [SessionStatus.COMPLETED, SessionStatus.TERMINATED]:
            update_data["session_end"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    async def update_session_cost(self, session_id: str, additional_cost: float) -> bool:
        """Add to session total cost"""
        result = await self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$inc": {"total_cost": additional_cost},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        result = await self.collection.delete_one({"_id": ObjectId(session_id)})
        return result.deleted_count > 0
    
    async def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        return await self.collection.count_documents({"status": SessionStatus.ACTIVE})

# Factory function
def get_session_crud(database: AsyncIOMotorDatabase) -> SessionCRUD:
    return SessionCRUD(database)
