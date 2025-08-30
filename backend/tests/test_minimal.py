"""
Minimal test to verify setup
"""

def test_simple():
    """Simple test that should always pass"""
    assert 1 + 1 == 2

def test_imports():
    """Test that we can import required modules"""
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    assert True

if __name__ == "__main__":
    test_simple()
    test_imports()
    print("✅ Basic tests passed")
