"""
CRUD operations for conversation threads
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.schemas import ConversationThreadCreate, ThreadStatus, Domain

class ThreadCRUD:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.conversation_threads
    
    async def create_thread(self, thread_data: ConversationThreadCreate) -> str:
        """Create a new conversation thread"""
        thread_doc = {
            "session_id": ObjectId(thread_data.session_id),
            "original_prompt": thread_data.original_prompt,
            "domain": thread_data.domain,
            "context": thread_data.context,
            "current_iteration": 0,
            "max_iterations_reached": False,
            "thread_status": ThreadStatus.INITIALIZING,
            "total_cost": 0.0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(thread_doc)
        return str(result.inserted_id)
    
    async def get_thread(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get thread by ID"""
        thread = await self.collection.find_one({"_id": ObjectId(thread_id)})
        return thread
    
    async def list_session_threads(
        self, 
        session_id: str,
        status: Optional[ThreadStatus] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List threads for a session"""
        filter_query = {"session_id": ObjectId(session_id)}
        if status:
            filter_query["thread_status"] = status
        
        cursor = self.collection.find(filter_query).sort("created_at", -1).limit(limit)
        threads = await cursor.to_list(length=None)
        return threads
    
    async def update_thread_status(
        self, 
        thread_id: str, 
        status: ThreadStatus,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update thread status and optional additional data"""
        update_data = {
            "thread_status": status,
            "updated_at": datetime.utcnow()
        }
        
        if additional_data:
            update_data.update(additional_data)
        
        if status == ThreadStatus.COMPLETED:
            update_data["completed_at"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(thread_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    async def increment_iteration(self, thread_id: str) -> bool:
        """Increment current iteration count"""
        result = await self.collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$inc": {"current_iteration": 1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    async def set_best_response(
        self, 
        thread_id: str, 
        model_id: str, 
        response_id: str,
        quality_score: float
    ) -> bool:
        """Set the best response for a thread"""
        result = await self.collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$set": {
                    "best_model_id": model_id,
                    "best_response_id": ObjectId(response_id),
                    "final_quality_score": quality_score,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    async def set_final_response(
        self, 
        thread_id: str, 
        final_response: str,
        user_accepted: bool = False
    ) -> bool:
        """Set the final response text"""
        result = await self.collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$set": {
                    "final_response": final_response,
                    "user_accepted": user_accepted,
                    "thread_status": ThreadStatus.COMPLETED,
                    "completed_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    async def update_cost(self, thread_id: str, additional_cost: float) -> bool:
        """Add to thread total cost"""
        result = await self.collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$inc": {"total_cost": additional_cost},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0
    
    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread"""
        result = await self.collection.delete_one({"_id": ObjectId(thread_id)})
        return result.deleted_count > 0
    
    async def get_threads_by_domain(self, domain: Domain, limit: int = 100) -> List[Dict[str, Any]]:
        """Get threads by domain for analytics"""
        cursor = self.collection.find({"domain": domain}).sort("created_at", -1).limit(limit)
        threads = await cursor.to_list(length=None)
        return threads

# Factory function
def get_thread_crud(database: AsyncIOMotorDatabase) -> ThreadCRUD:
    return ThreadCRUD(database)
