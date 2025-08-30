#!/usr/bin/env python3
"""
Backend Health Check Script
Tests all major components of the OrchestrateX backend
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        # Core imports
        from app.core.database import connect_to_mongo, close_mongo_connection
        print("✅ Database module imported")
        
        # Model imports
        from app.models.schemas import Domain, SessionStatus, ThreadStatus, OrchestrationStatus
        print("✅ Schema models imported")
        
        # Provider imports
        from app.ai_providers import provider_manager
        print("✅ AI providers imported")
        
        # Route imports
        from app.routes import sessions, threads, models, orchestration, analytics
        print("✅ Route modules imported")
        
        # Orchestration engine
        from app.orchestration.engine import orchestration_engine
        print("✅ Orchestration engine imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_database_connection():
    """Test database connection (optional)"""
    print("\n🔍 Testing database connection...")
    
    try:
        from app.core.database import connect_to_mongo, close_mongo_connection
        
        # Try to connect
        database = await connect_to_mongo()
        print("✅ Database connection successful")
        await close_mongo_connection()
        return True
        
    except Exception as e:
        print(f"⚠️  Database connection failed (this is optional): {e}")
        return False

async def test_fastapi_app():
    """Test FastAPI app creation"""
    print("\n🔍 Testing FastAPI app creation...")
    
    try:
        from main import app
        print("✅ FastAPI app created successfully")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 OrchestrateX Backend Health Check\n")
    
    tests = [
        ("Module Imports", test_imports()),
        ("Database Connection", test_database_connection()), 
        ("FastAPI App", test_fastapi_app())
    ]
    
    results = []
    for name, test_coro in tests:
        try:
            result = await test_coro
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
    
    print("\n📊 Test Summary:")
    print("=" * 50)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nResult: {passed}/{len(results)} tests passed")
    
    if passed >= 2:  # Allow database to fail
        print("\n🎉 Backend is ready to run!")
        print("💡 To start the server, run: python main.py")
        if passed < len(results):
            print("⚠️  Note: Database connection failed. Make sure MongoDB is running for full functionality.")
    else:
        print("\n❌ Backend has critical issues that need to be fixed.")
        
    return passed >= 2

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
