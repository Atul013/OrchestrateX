"""
Database connection and configuration for OrchestrateX
"""

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

# Database configuration
MONGODB_CONNECTION_STRING = "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
DATABASE_NAME = "orchestratex"

# Global database client
client: motor.motor_asyncio.AsyncIOMotorClient = None

async def connect_to_mongo() -> AsyncIOMotorDatabase:
    """Create database connection"""
    global client
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
        
        # Test the connection
        await client.admin.command('ping')
        logging.info("Successfully connected to MongoDB")
        
        database = client[DATABASE_NAME]
        return database
        
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        logging.info("Disconnected from MongoDB")

async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return client[DATABASE_NAME]
