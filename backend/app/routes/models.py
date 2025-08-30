"""
AI Models management routes for OrchestrateX API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime
import logging
from bson import ObjectId

from app.models.schemas import AIModelProfile, Domain
from app.core.database import get_database

router = APIRouter()

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

@router.get("/", response_model=List[AIModelProfile])
async def list_models(
    active_only: bool = True,
    available_only: bool = True, 
    db=Depends(get_db)
):
    """List all AI models"""
    try:
        filter_query = {}
        if active_only:
            filter_query["is_active"] = True
        if available_only:
            filter_query["is_available"] = True
        
        cursor = db.ai_model_profiles.find(filter_query)
        
        models = []
        async for model in cursor:
            model["_id"] = str(model["_id"])
            models.append(model)
        
        return models
        
    except Exception as e:
        logging.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve models")

@router.get("/{model_name}", response_model=AIModelProfile)
async def get_model(model_name: str, db=Depends(get_db)):
    """Get specific model details"""
    try:
        model = await db.ai_model_profiles.find_one({"model_name": model_name})
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        model["_id"] = str(model["_id"])
        return model
        
    except Exception as e:
        logging.error(f"Failed to get model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model")

@router.get("/specialties/{domain}", response_model=List[AIModelProfile])
async def get_models_by_specialty(domain: Domain, db=Depends(get_db)):
    """Get models that specialize in a specific domain"""
    try:
        cursor = db.ai_model_profiles.find({
            "specialties": domain.value,
            "is_active": True,
            "is_available": True
        })
        
        models = []
        async for model in cursor:
            model["_id"] = str(model["_id"])
            models.append(model)
        
        # Sort by performance metrics if available
        models.sort(
            key=lambda x: x.get("performance_metrics", {}).get("average_quality_rating", 0),
            reverse=True
        )
        
        return models
        
    except Exception as e:
        logging.error(f"Failed to get models for domain {domain}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve models by specialty")

@router.put("/{model_name}/status")
async def update_model_status(
    model_name: str, 
    is_available: bool, 
    db=Depends(get_db)
):
    """Update model availability status"""
    try:
        result = await db.ai_model_profiles.update_one(
            {"model_name": model_name},
            {
                "$set": {
                    "is_available": is_available,
                    "last_health_check": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return {"message": f"Model {model_name} status updated to {'available' if is_available else 'unavailable'}"}
        
    except Exception as e:
        logging.error(f"Failed to update model {model_name} status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update model status")

@router.post("/{model_name}/test")
async def test_model_availability(model_name: str, db=Depends(get_db)):
    """Test model availability (placeholder for actual API calls)"""
    try:
        model = await db.ai_model_profiles.find_one({"model_name": model_name})
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # TODO: Implement actual API health check for each model
        # For now, simulate a test
        is_healthy = True  # Replace with actual API call
        
        # Update model status based on test
        await db.ai_model_profiles.update_one(
            {"model_name": model_name},
            {
                "$set": {
                    "is_available": is_healthy,
                    "last_health_check": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "model_name": model_name,
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to test model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to test model availability")
