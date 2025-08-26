"""
OrchestrateX Backend API
FastAPI application for multi-AI orchestration system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import sessions, threads, models, orchestration, analytics

# Global database connection
database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    global database
    database = await connect_to_mongo()
    app.state.database = database
    yield
    # Shutdown
    await close_mongo_connection()

# Create FastAPI application
app = FastAPI(
    title="OrchestrateX API",
    description="Multi-AI Orchestration System with Iterative Improvement",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(threads.router, prefix="/api/threads", tags=["threads"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(orchestration.router, prefix="/api/orchestrate", tags=["orchestration"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OrchestrateX Multi-AI Orchestration API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        collections = await app.state.database.list_collection_names()
        return {
            "status": "healthy",
            "database": "connected",
            "collections": len(collections),
            "timestamp": "2025-08-26T15:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
