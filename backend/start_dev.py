#!/usr/bin/env python3
"""
OrchestrateX Backend Development Server
Starts the backend with graceful handling of missing dependencies
"""

import asyncio
import uvicorn
import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

async def check_database():
    """Check if database is available"""
    try:
        from app.core.database import connect_to_mongo, close_mongo_connection
        db = await connect_to_mongo()
        await close_mongo_connection()
        return True
    except Exception as e:
        print(f"⚠️  Database not available: {e}")
        print("   The server will start but database features will be limited.")
        return False

def main():
    """Start the development server"""
    print("🚀 Starting OrchestrateX Backend...")
    
    # Check if we can import the main app
    try:
        from main import app
        print("✅ Backend modules loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load backend: {e}")
        sys.exit(1)
    
    # Check database asynchronously (don't block startup)
    try:
        asyncio.run(check_database())
    except Exception as e:
        print(f"⚠️  Database check failed: {e}")
    
    print("\n🌐 Starting server on http://localhost:8001")
    print("📖 API documentation: http://localhost:8001/docs")
    print("🔍 Health check: http://localhost:8001/health")
    print("\n💡 Press Ctrl+C to stop the server")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
