"""
Direct test execution to bypass any hanging issues
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, r'c:\Users\kalad\OrchestrateX\backend')

async def test_session_creation():
    """Test session creation directly"""
    print("Testing session creation...")
    
    try:
        # Import required modules
        from fastapi.testclient import TestClient
        from fastapi import FastAPI
        from motor.motor_asyncio import AsyncIOMotorClient
        
        # Create test app
        app = FastAPI(title="Test App")
        
        # Import routes
        from app.routes import sessions
        from app.core.database import get_database
        from app.routes.sessions import get_db
        
        # Test database setup
        TEST_MONGODB_URL = "mongodb://project_admin:project_password@localhost:27018/orchestratex_test?authSource=admin"
        test_client = AsyncIOMotorClient(TEST_MONGODB_URL)
        test_database = test_client["orchestratex_test"]
        
        # Override dependencies
        async def override_get_database():
            return test_database
        
        async def override_get_db():
            return test_database
        
        app.dependency_overrides[get_database] = override_get_database
        app.dependency_overrides[get_db] = override_get_db
        
        # Include router
        app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
        
        # Create test client
        client = TestClient(app)
        
        # Test data
        test_data = {
            "user_id": "test_user_123",
            "max_iterations": 5,
            "settings": {
                "preferred_models": ["gpt4", "claude"],
                "cost_limit": 10.0
            }
        }
        
        # Make request
        print("Making POST request...")
        response = client.post("/api/sessions/", json=test_data)
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Session created successfully with ID: {data.get('_id')}")
            return True
        else:
            print(f"❌ Failed to create session: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Running direct session test...")
    print("=" * 50)
    
    try:
        # Run the async test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_session_creation())
        loop.close()
        
        if result:
            print("✅ Direct test PASSED")
        else:
            print("❌ Direct test FAILED")
            
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
