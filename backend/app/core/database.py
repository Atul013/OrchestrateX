"""
Database connection and configuration for OrchestrateX
"""

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration with fallback to local MongoDB
MONGODB_CONNECTION_STRING = os.getenv(
    "MONGODB_CONNECTION_STRING", 
    "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "orchestratex")

# Global database client
client: motor.motor_asyncio.AsyncIOMotorClient = None

async def connect_to_mongo() -> AsyncIOMotorDatabase:
    """Create database connection"""
    global client
    try:
        # Configure connection based on connection string type
        if "mongodb+srv://" in MONGODB_CONNECTION_STRING:
            # Atlas connection - use default settings
            client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
            logging.info("Connecting to MongoDB Atlas...")
        else:
            # Local MongoDB connection - with timeout
            client = motor.motor_asyncio.AsyncIOMotorClient(
                MONGODB_CONNECTION_STRING,
                serverSelectionTimeoutMS=5000
            )
            logging.info("Connecting to local MongoDB...")
        
        # Test the connection
        await client.admin.command('ping')
        logging.info(f"Successfully connected to MongoDB: {DATABASE_NAME}")
        
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
