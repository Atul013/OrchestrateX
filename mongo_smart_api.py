#!/usr/bin/env python3
"""
Simple MongoDB API for OrchestrateX Algorithm Response Storage
Connects to Docker MongoDB with proper authentication
"""

from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
import sys

app = Flask(__name__)

# MongoDB Configuration
MONGO_HOST = "localhost"
MONGO_PORT = 27018
MONGO_USERNAME = "project_admin"
MONGO_PASSWORD = "project_password"
DATABASE_NAME = "orchestratex_db"

# Global MongoDB client
mongo_client = None
db = None

def connect_to_mongodb():
    """Connect to MongoDB with authentication"""
    global mongo_client, db
    
    try:
        # MongoDB connection URI with authentication
        connection_uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
        
        # Create MongoDB client
        mongo_client = MongoClient(connection_uri)
        
        # Test connection
        mongo_client.admin.command('ping')
        
        # Get database
        db = mongo_client[DATABASE_NAME]
        
        print(f"✅ Successfully connected to MongoDB at {MONGO_HOST}:{MONGO_PORT}")
        print(f"✅ Using database: {DATABASE_NAME}")
        
        # List available collections
        collections = db.list_collection_names()
        print(f"📂 Available collections: {collections}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if mongo_client:
            mongo_client.admin.command('ping')
            return jsonify({
                "status": "healthy",
                "database": DATABASE_NAME,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"status": "unhealthy", "error": "No database connection"}), 500
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/store-response', methods=['POST'])
def store_algorithm_response():
    """Store algorithm model selection response"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Prepare response document
        response_doc = {
            "timestamp": datetime.now(),
            "user_input": data.get("user_input"),
            "selected_model": data.get("selected_model"),
            "confidence_score": data.get("confidence_score"),
            "algorithm_version": data.get("algorithm_version", "1.0"),
            "response_text": data.get("response_text"),
            "metadata": data.get("metadata", {})
        }
        
        # Store in model_responses collection
        result = db.model_responses.insert_one(response_doc)
        
        return jsonify({
            "success": True,
            "document_id": str(result.inserted_id),
            "timestamp": response_doc["timestamp"].isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to store response: {str(e)}"}), 500

@app.route('/get-responses', methods=['GET'])
def get_stored_responses():
    """Get stored algorithm responses"""
    try:
        # Get limit parameter
        limit = int(request.args.get('limit', 10))
        
        # Query responses
        responses = list(db.model_responses.find().sort("timestamp", -1).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for response in responses:
            response['_id'] = str(response['_id'])
            response['timestamp'] = response['timestamp'].isoformat()
        
        return jsonify({
            "success": True,
            "count": len(responses),
            "responses": responses
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get responses: {str(e)}"}), 500

@app.route('/collections', methods=['GET'])
def list_collections():
    """List all available collections"""
    try:
        collections = db.list_collection_names()
        return jsonify({
            "success": True,
            "collections": collections
        })
    except Exception as e:
        return jsonify({"error": f"Failed to list collections: {str(e)}"}), 500

if __name__ == "__main__":
    print("🚀 Starting OrchestrateX MongoDB API...")
    
    # Connect to MongoDB
    if connect_to_mongodb():
        print("🌐 Starting Flask server on http://localhost:5001")
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        print("❌ Failed to start API - MongoDB connection failed")
        sys.exit(1)
