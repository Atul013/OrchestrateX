"""
OrchestrateX Backend API
FastAPI application for multi-AI orchestration system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.routes import sessions, threads, models, orchestration, analytics
from app.websocket import routes as websocket_routes

# Global database connection
database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    print("🚀 Starting OrchestrateX Backend...")
    global database
    database = await connect_to_mongo()
    app.state.database = database
    
    # Initialize AI providers and orchestration engine
    try:
        from app.ai_providers import provider_manager
        from app.orchestration.engine import orchestration_engine
        
        # Set API keys (in production, these would come from environment variables)
        # provider_manager.set_api_key("openai", "your-openai-key")
        # provider_manager.set_api_key("anthropic", "your-anthropic-key")
        
        await provider_manager.initialize_providers()
        await orchestration_engine.initialize()
        
        print("✅ AI providers and orchestration engine initialized")
    except Exception as e:
        print(f"⚠️  Warning: AI providers initialization failed: {e}")
    
    print("✅ OrchestrateX Backend started successfully!")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down OrchestrateX Backend...")
    try:
        await provider_manager.close_all()
    except:
        pass
    await close_mongo_connection()
    print("✅ OrchestrateX Backend shutdown complete")

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
app.include_router(websocket_routes.router, tags=["websocket"])

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
        port=8001,
        reload=True,
        log_level="info"
    )
