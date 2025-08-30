"""
Quick test script to check if all imports work
"""
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    print("Testing FastAPI import...")
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
    
    print("Testing Motor import...")
    import motor.motor_asyncio
    print("✅ Motor imported successfully")
    
    print("Testing backend app imports...")
    from backend.app.core.database import connect_to_mongo
    print("✅ Database module imported successfully")
    
    print("Testing routes...")
    from backend.app.routes import sessions, threads, models
    print("✅ Routes imported successfully")
    
    print("\n🎉 All imports successful! Backend should work.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Missing dependency, installing...")
