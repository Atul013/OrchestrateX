"""
WebSocket Manager for Real-Time Orchestration Updates
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import logging

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        # Store active connections by session_id
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Store thread subscriptions
        self.thread_subscriptions: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        
        self.active_connections[session_id].append(websocket)
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Connected to OrchestrateX real-time updates"
        }, websocket)
        
        logging.info(f"WebSocket connected for session: {session_id}")
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove a WebSocket connection"""
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            
            # Clean up empty session
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        
        # Remove from thread subscriptions
        for thread_id, connections in self.thread_subscriptions.items():
            if websocket in connections:
                connections.remove(websocket)
        
        logging.info(f"WebSocket disconnected for session: {session_id}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logging.error(f"Failed to send WebSocket message: {e}")
    
    async def send_to_session(self, session_id: str, message: Dict[str, Any]):
        """Send a message to all connections for a session"""
        if session_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for connection in disconnected:
                self.active_connections[session_id].remove(connection)
    
    async def send_to_thread(self, thread_id: str, message: Dict[str, Any]):
        """Send a message to all connections subscribed to a thread"""
        if thread_id in self.thread_subscriptions:
            disconnected = []
            for connection in self.thread_subscriptions[thread_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for connection in disconnected:
                self.thread_subscriptions[thread_id].remove(connection)
    
    async def subscribe_to_thread(self, websocket: WebSocket, thread_id: str):
        """Subscribe a WebSocket to thread updates"""
        if thread_id not in self.thread_subscriptions:
            self.thread_subscriptions[thread_id] = []
        
        if websocket not in self.thread_subscriptions[thread_id]:
            self.thread_subscriptions[thread_id].append(websocket)
        
        await self.send_personal_message({
            "type": "thread_subscription",
            "thread_id": thread_id,
            "status": "subscribed",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    async def unsubscribe_from_thread(self, websocket: WebSocket, thread_id: str):
        """Unsubscribe a WebSocket from thread updates"""
        if thread_id in self.thread_subscriptions:
            if websocket in self.thread_subscriptions[thread_id]:
                self.thread_subscriptions[thread_id].remove(websocket)
        
        await self.send_personal_message({
            "type": "thread_unsubscription",
            "thread_id": thread_id,
            "status": "unsubscribed",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
    
    async def broadcast_orchestration_start(self, session_id: str, thread_id: str, prompt: str):
        """Broadcast orchestration start event"""
        message = {
            "type": "orchestration_started",
            "thread_id": thread_id,
            "session_id": session_id,
            "prompt_preview": prompt[:100] + ("..." if len(prompt) > 100 else ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_session(session_id, message)
        await self.send_to_thread(thread_id, message)
    
    async def broadcast_model_selection(self, thread_id: str, model_name: str, iteration: int, reasoning: str):
        """Broadcast model selection event"""
        message = {
            "type": "model_selected",
            "thread_id": thread_id,
            "iteration": iteration,
            "selected_model": model_name,
            "reasoning": reasoning,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_thread(thread_id, message)
    
    async def broadcast_response_generated(self, thread_id: str, model_name: str, iteration: int, response_preview: str):
        """Broadcast response generation event"""
        message = {
            "type": "response_generated",
            "thread_id": thread_id,
            "iteration": iteration,
            "model": model_name,
            "response_preview": response_preview[:200] + ("..." if len(response_preview) > 200 else ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_thread(thread_id, message)
    
    async def broadcast_evaluation_complete(self, thread_id: str, iteration: int, quality_score: float):
        """Broadcast evaluation completion event"""
        message = {
            "type": "evaluation_complete",
            "thread_id": thread_id,
            "iteration": iteration,
            "quality_score": quality_score,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_thread(thread_id, message)
    
    async def broadcast_criticism_received(self, thread_id: str, iteration: int, criticism_summary: str):
        """Broadcast criticism received event"""
        message = {
            "type": "criticism_received",
            "thread_id": thread_id,
            "iteration": iteration,
            "criticism_summary": criticism_summary,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_thread(thread_id, message)
    
    async def broadcast_orchestration_complete(self, thread_id: str, final_quality: float, iterations_used: int):
        """Broadcast orchestration completion event"""
        message = {
            "type": "orchestration_complete",
            "thread_id": thread_id,
            "final_quality_score": final_quality,
            "iterations_used": iterations_used,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_thread(thread_id, message)
    
    async def broadcast_error(self, thread_id: str, error_message: str):
        """Broadcast error event"""
        message = {
            "type": "error",
            "thread_id": thread_id,
            "error_message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_to_thread(thread_id, message)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_sessions": len(self.active_connections),
            "total_connections": sum(len(connections) for connections in self.active_connections.values()),
            "thread_subscriptions": len(self.thread_subscriptions),
            "active_threads": list(self.thread_subscriptions.keys())
        }

# Global connection manager instance
manager = ConnectionManager()
