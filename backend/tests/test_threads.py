"""
Test cases for thread endpoints
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestThreadEndpoints:
    
    def test_create_thread(self, test_session_data, test_thread_data):
        """Test creating a new conversation thread"""
        # First create a session
        session_response = client.post("/api/sessions/", json=test_session_data)
        session_id = session_response.json()["id"]
        
        # Update thread data with actual session ID
        thread_data = test_thread_data.copy()
        thread_data["session_id"] = session_id
        
        # Create thread
        response = client.post("/api/threads/", json=thread_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["session_id"] == session_id
        assert data["original_prompt"] == thread_data["original_prompt"]
        assert data["domain"] == thread_data["domain"]
        assert data["thread_status"] == "initializing"
    
    def test_get_thread(self, test_session_data, test_thread_data):
        """Test retrieving a thread"""
        # Create session and thread
        session_response = client.post("/api/sessions/", json=test_session_data)
        session_id = session_response.json()["id"]
        
        thread_data = test_thread_data.copy()
        thread_data["session_id"] = session_id
        
        thread_response = client.post("/api/threads/", json=thread_data)
        thread_id = thread_response.json()["id"]
        
        # Retrieve thread
        response = client.get(f"/api/threads/{thread_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == thread_id
        assert data["original_prompt"] == thread_data["original_prompt"]
    
    def test_list_session_threads(self, test_session_data, test_thread_data):
        """Test listing threads for a session"""
        # Create session and thread
        session_response = client.post("/api/sessions/", json=test_session_data)
        session_id = session_response.json()["id"]
        
        thread_data = test_thread_data.copy()
        thread_data["session_id"] = session_id
        
        client.post("/api/threads/", json=thread_data)
        
        # List threads
        response = client.get(f"/api/threads/session/{session_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["session_id"] == session_id
    
    def test_update_thread_status(self, test_session_data, test_thread_data):
        """Test updating thread status"""
        # Create session and thread
        session_response = client.post("/api/sessions/", json=test_session_data)
        session_id = session_response.json()["id"]
        
        thread_data = test_thread_data.copy()
        thread_data["session_id"] = session_id
        
        thread_response = client.post("/api/threads/", json=thread_data)
        thread_id = thread_response.json()["id"]
        
        # Update status
        response = client.patch(f"/api/threads/{thread_id}/status", 
                              json={"status": "responding"})
        assert response.status_code == 200
        
        # Verify update
        get_response = client.get(f"/api/threads/{thread_id}")
        assert get_response.json()["thread_status"] == "responding"
    
    def test_thread_not_found(self):
        """Test retrieving non-existent thread"""
        fake_id = "64f1a2b3c4d5e6f7a8b9c0d1"
        response = client.get(f"/api/threads/{fake_id}")
        assert response.status_code == 404
