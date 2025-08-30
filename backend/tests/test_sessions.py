"""
Test cases for session endpoints
"""

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    """Create test client"""
    return TestClient(app)

class TestSessionEndpoints:
    
    def test_create_session(self, client, test_session_data):
        """Test creating a new session"""
        response = client.post("/api/sessions/", json=test_session_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "_id" in data  # Currently using _id instead of id
        assert data["user_id"] == test_session_data["user_id"]
        assert data["max_iterations"] == test_session_data["max_iterations"]
        assert data["status"] == "active"
    
    def test_get_session(self, client, test_session_data):
        """Test retrieving a session"""
        # First create a session
        create_response = client.post("/api/sessions/", json=test_session_data)
        session_id = create_response.json()["_id"]  # Currently using _id
        
        # Then retrieve it
        response = client.get(f"/api/sessions/{session_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["_id"] == session_id  # Currently using _id
        assert data["user_id"] == test_session_data["user_id"]
    
    def test_list_user_sessions(self, client, test_session_data):
        """Test listing sessions for a user"""
        # Create a session first
        client.post("/api/sessions/", json=test_session_data)
        
        # List sessions for the user
        response = client.get(f"/api/sessions/user/{test_session_data['user_id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["user_id"] == test_session_data["user_id"]
    
    def test_update_session_status(self, client, test_session_data):
        """Test updating session status"""
        # Create a session
        create_response = client.post("/api/sessions/", json=test_session_data)
        session_id = create_response.json()["_id"]  # Currently using _id
        
        # Update status
        response = client.patch(f"/api/sessions/{session_id}/status", 
                              json={"status": "completed"})
        assert response.status_code == 200
        
        # Verify update
        get_response = client.get(f"/api/sessions/{session_id}")
        assert get_response.json()["status"] == "completed"
    
    def test_session_not_found(self, client):
        """Test retrieving non-existent session"""
        fake_id = "64f1a2b3c4d5e6f7a8b9c0d1"
        response = client.get(f"/api/sessions/{fake_id}")
        assert response.status_code == 404
    
    def test_invalid_session_data(self, client):
        """Test creating session with invalid data"""
        invalid_data = {
            "user_id": "",  # Empty user_id
            "max_iterations": 0  # Invalid iteration count
        }
        response = client.post("/api/sessions/", json=invalid_data)
        assert response.status_code == 422  # Validation error
