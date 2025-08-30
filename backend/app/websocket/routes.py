"""
WebSocket Routes for Real-Time Communication
"""

import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
import logging

from .manager import manager

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time orchestration updates"""
    
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "subscribe_thread":
                    thread_id = message.get("thread_id")
                    if thread_id:
                        await manager.subscribe_to_thread(websocket, thread_id)
                
                elif message.get("type") == "unsubscribe_thread":
                    thread_id = message.get("thread_id")
                    if thread_id:
                        await manager.unsubscribe_from_thread(websocket, thread_id)
                
                elif message.get("type") == "ping":
                    # Respond to ping
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }, websocket)
                
                elif message.get("type") == "get_stats":
                    # Send connection statistics
                    stats = manager.get_connection_stats()
                    await manager.send_personal_message({
                        "type": "stats",
                        "data": stats
                    }, websocket)
                
                else:
                    # Echo unknown messages
                    await manager.send_personal_message({
                        "type": "echo",
                        "original_message": message
                    }, websocket)
            
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        logging.info(f"WebSocket disconnected for session: {session_id}")
    
    except Exception as e:
        logging.error(f"WebSocket error for session {session_id}: {e}")
        manager.disconnect(websocket, session_id)

@router.websocket("/ws/thread/{thread_id}")
async def thread_websocket_endpoint(websocket: WebSocket, thread_id: str):
    """WebSocket endpoint for specific thread updates"""
    
    # Use thread_id as session_id for this connection
    await manager.connect(websocket, f"thread_{thread_id}")
    await manager.subscribe_to_thread(websocket, thread_id)
    
    try:
        while True:
            # Keep connection alive and handle messages
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await manager.send_personal_message({
                        "type": "pong",
                        "thread_id": thread_id,
                        "timestamp": message.get("timestamp")
                    }, websocket)
                
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, f"thread_{thread_id}")
        logging.info(f"Thread WebSocket disconnected for thread: {thread_id}")
    
    except Exception as e:
        logging.error(f"Thread WebSocket error for {thread_id}: {e}")
        manager.disconnect(websocket, f"thread_{thread_id}")

# Helper functions for integration with orchestration engine

async def notify_orchestration_start(session_id: str, thread_id: str, prompt: str):
    """Notify clients of orchestration start"""
    await manager.broadcast_orchestration_start(session_id, thread_id, prompt)

async def notify_model_selection(thread_id: str, model_name: str, iteration: int, reasoning: str):
    """Notify clients of model selection"""
    await manager.broadcast_model_selection(thread_id, model_name, iteration, reasoning)

async def notify_response_generated(thread_id: str, model_name: str, iteration: int, response_preview: str):
    """Notify clients of response generation"""
    await manager.broadcast_response_generated(thread_id, model_name, iteration, response_preview)

async def notify_evaluation_complete(thread_id: str, iteration: int, quality_score: float):
    """Notify clients of evaluation completion"""
    await manager.broadcast_evaluation_complete(thread_id, iteration, quality_score)

async def notify_criticism_received(thread_id: str, iteration: int, criticism_summary: str):
    """Notify clients of criticism received"""
    await manager.broadcast_criticism_received(thread_id, iteration, criticism_summary)

async def notify_orchestration_complete(thread_id: str, final_quality: float, iterations_used: int):
    """Notify clients of orchestration completion"""
    await manager.broadcast_orchestration_complete(thread_id, final_quality, iterations_used)

async def notify_error(thread_id: str, error_message: str):
    """Notify clients of errors"""
    await manager.broadcast_error(thread_id, error_message)
