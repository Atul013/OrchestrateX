"""
Test configuration and fixtures
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# Test database configuration
TEST_DATABASE_NAME = "orchestratex_test"
TEST_MONGODB_URL = "mongodb://project_admin:project_password@localhost:27018/orchestratex_test?authSource=admin"

# Global test database client
test_client = None
test_database = None

def init_test_db():
    """Initialize test database connection"""
    global test_client, test_database
    
    if test_database is None:
        test_client = AsyncIOMotorClient(TEST_MONGODB_URL)
        test_database = test_client[TEST_DATABASE_NAME]
    
    return test_database

# Override database dependency for testing
async def override_get_database():
    """Override database dependency to use test database"""
    if test_database is None:
        init_test_db()
    return test_database

async def override_get_db():
    """Override the sessions route database dependency"""
    return await override_get_database()

def create_test_app():
    """Create a test version of the FastAPI app without lifespan events"""
    # Create a simple FastAPI app without the complex lifespan
    test_app = FastAPI(
        title="OrchestrateX Test API",
        description="Test version of OrchestrateX API",
        version="1.0.0-test"
    )
    
    # Import and include routes
    from app.routes import sessions
    from app.core.database import get_database
    from app.routes.sessions import get_db
    
    # Apply dependency overrides
    test_app.dependency_overrides[get_database] = override_get_database
    test_app.dependency_overrides[get_db] = override_get_db
    
    # Include the sessions router
    test_app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
    
    return test_app

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up test database for the entire test session"""
    init_test_db()
    print("✅ Test database initialized")
    yield
    # Cleanup will be handled by individual test cleanup

@pytest.fixture(scope="module")
def app():
    """Create test app instance"""
    return create_test_app()

@pytest.fixture
def test_session_data():
    """Sample session data for testing"""
    return {
        "user_id": "test_user_123",
        "max_iterations": 5,
        "settings": {
            "preferred_models": ["gpt4", "claude"],
            "cost_limit": 10.0
        }
    }

@pytest.fixture
def test_thread_data():
    """Sample thread data for testing"""
    return {
        "session_id": "64f1a2b3c4d5e6f7a8b9c0d1",  # Will be replaced with actual session ID
        "original_prompt": "Write a Python function to calculate fibonacci numbers",
        "domain": "coding",
        "context": "This is for a beginner programming tutorial"
    }

# Test data fixtures
