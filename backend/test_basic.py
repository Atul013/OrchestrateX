"""
Simple test to check basic setup
"""

import asyncio
import pytest
from fastapi.testclient import TestClient

def test_basic_import():
    """Test if we can import the main modules"""
    try:
        from main import app
        from app.core.database import get_database
        print("✅ Basic imports working")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test if FastAPI app can be created"""
    try:
        from main import app
        client = TestClient(app)
        print("✅ TestClient created successfully")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

if __name__ == "__main__":
    print("Running basic tests...")
    test1 = test_basic_import()
    test2 = test_app_creation()
    
    if test1 and test2:
        print("✅ Basic setup is working!")
    else:
        print("❌ Basic setup has issues")
