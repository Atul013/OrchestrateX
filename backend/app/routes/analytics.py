"""
Analytics and performance routes for OrchestrateX API
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime, timedelta
import logging

from app.core.database import get_database

router = APIRouter()

async def get_db():
    """Dependency to get database instance"""
    return await get_database()

@router.get("/model-performance")
async def get_model_performance(db=Depends(get_db)):
    """Get model performance metrics"""
    try:
        # Get all model profiles with performance metrics
        cursor = db.ai_model_profiles.find({}, {
            "model_name": 1,
            "provider": 1,
            "performance_metrics": 1,
            "specialties": 1
        })
        
        performance_data = []
        async for model in cursor:
            performance_data.append({
                "model_name": model["model_name"],
                "provider": model["provider"],
                "specialties": model["specialties"],
                "metrics": model.get("performance_metrics", {})
            })
        
        return {
            "models": performance_data,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get model performance: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model performance")

@router.get("/cost-analysis")
async def get_cost_analysis(days: int = 7, db=Depends(get_db)):
    """Get cost breakdown and analysis"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get sessions within date range
        session_cursor = db.user_sessions.find({
            "created_at": {"$gte": start_date, "$lte": end_date}
        }, {"total_cost": 1, "status": 1, "created_at": 1})
        
        total_cost = 0.0
        session_count = 0
        completed_sessions = 0
        
        async for session in session_cursor:
            session_count += 1
            total_cost += session.get("total_cost", 0.0)
            if session.get("status") == "completed":
                completed_sessions += 1
        
        average_cost_per_session = total_cost / session_count if session_count > 0 else 0.0
        completion_rate = (completed_sessions / session_count * 100) if session_count > 0 else 0.0
        
        return {
            "period": f"Last {days} days",
            "total_cost": round(total_cost, 2),
            "session_count": session_count,
            "average_cost_per_session": round(average_cost_per_session, 2),
            "completion_rate": round(completion_rate, 1),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get cost analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cost analysis")

@router.get("/domain-stats")
async def get_domain_stats(db=Depends(get_db)):
    """Get performance statistics by domain"""
    try:
        # Aggregate threads by domain
        pipeline = [
            {
                "$group": {
                    "_id": "$domain",
                    "count": {"$sum": 1},
                    "avg_iterations": {"$avg": "$current_iteration"},
                    "avg_cost": {"$avg": "$total_cost"},
                    "avg_quality": {"$avg": "$final_quality_score"},
                    "completed": {
                        "$sum": {
                            "$cond": [{"$eq": ["$thread_status", "completed"]}, 1, 0]
                        }
                    }
                }
            },
            {
                "$project": {
                    "domain": "$_id",
                    "total_requests": "$count",
                    "average_iterations": {"$round": ["$avg_iterations", 2]},
                    "average_cost": {"$round": ["$avg_cost", 4]},
                    "average_quality": {"$round": ["$avg_quality", 2]},
                    "completion_rate": {
                        "$round": [{"$multiply": [{"$divide": ["$completed", "$count"]}, 100]}, 1]
                    }
                }
            }
        ]
        
        cursor = db.conversation_threads.aggregate(pipeline)
        domain_stats = []
        
        async for stat in cursor:
            domain_stats.append(stat)
        
        return {
            "domain_statistics": domain_stats,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get domain stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve domain statistics")

@router.get("/selection-accuracy")
async def get_selection_accuracy(db=Depends(get_db)):
    """Get model selection effectiveness metrics"""
    try:
        # TODO: Implement selection accuracy calculation
        # This would require tracking selection success metrics
        
        return {
            "message": "Selection accuracy metrics not yet implemented",
            "overall_accuracy": 85.3,  # Placeholder
            "model_selection_success_rate": 92.1,  # Placeholder
            "improvement_over_random": 34.7,  # Placeholder
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get selection accuracy: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve selection accuracy")

@router.get("/user-satisfaction")
async def get_user_satisfaction(db=Depends(get_db)):
    """Get user satisfaction metrics"""
    try:
        # Get sessions with satisfaction ratings
        cursor = db.user_sessions.find({
            "user_satisfaction": {"$exists": True, "$ne": None}
        }, {"user_satisfaction": 1, "total_cost": 1, "created_at": 1})
        
        ratings = []
        total_cost = 0.0
        
        async for session in cursor:
            if session.get("user_satisfaction"):
                ratings.append(session["user_satisfaction"])
                total_cost += session.get("total_cost", 0.0)
        
        if not ratings:
            return {
                "message": "No user satisfaction data available yet",
                "average_satisfaction": None,
                "total_ratings": 0
            }
        
        average_satisfaction = sum(ratings) / len(ratings)
        
        return {
            "average_satisfaction": round(average_satisfaction, 2),
            "total_ratings": len(ratings),
            "satisfaction_distribution": {
                "excellent (9-10)": len([r for r in ratings if r >= 9]),
                "good (7-8)": len([r for r in ratings if 7 <= r < 9]),
                "fair (5-6)": len([r for r in ratings if 5 <= r < 7]),
                "poor (1-4)": len([r for r in ratings if r < 5])
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get user satisfaction: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user satisfaction")
