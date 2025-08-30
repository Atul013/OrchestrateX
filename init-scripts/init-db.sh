#!/bin/bash
# OrchestrateX Database Initialization Script
# This script initializes the MongoDB database for the multi-AI orchestration system

set -e

echo "🚀 Starting OrchestrateX Database Initialization..."

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to start..."
until mongosh --host localhost:27017 --eval "print(\"MongoDB is ready\")" >/dev/null 2>&1; do
    echo "Waiting for MongoDB..."
    sleep 2
done

echo "✅ MongoDB is ready!"

# Initialize the database with collections and indexes
echo "📁 Creating database and collections..."
mongosh --host localhost:27017 <<EOF
use orchestratex;

// Create collections with schema validation
db.createCollection("sessions", {
    validator: {
        \$jsonSchema: {
            bsonType: "object",
            required: ["id", "created_at"],
            properties: {
                id: { bsonType: "string" },
                user_id: { bsonType: "string" },
                created_at: { bsonType: "date" },
                updated_at: { bsonType: "date" },
                status: { enum: ["active", "completed", "failed"] }
            }
        }
    }
});

db.createCollection("threads", {
    validator: {
        \$jsonSchema: {
            bsonType: "object",
            required: ["id", "session_id", "created_at"],
            properties: {
                id: { bsonType: "string" },
                session_id: { bsonType: "string" },
                created_at: { bsonType: "date" },
                messages: { bsonType: "array" }
            }
        }
    }
});

db.createCollection("orchestration_requests");
db.createCollection("ai_responses");
db.createCollection("performance_metrics");
db.createCollection("cost_tracking");
db.createCollection("model_analytics");
db.createCollection("prompt_history");
db.createCollection("user_preferences");

echo "✅ Collections created successfully!"
EOF

# Create indexes for better performance
echo "🔍 Creating database indexes..."
mongosh --host localhost:27017 <<EOF
use orchestratex;

// Session indexes
db.sessions.createIndex({ "id": 1 }, { unique: true });
db.sessions.createIndex({ "user_id": 1 });
db.sessions.createIndex({ "created_at": -1 });
db.sessions.createIndex({ "status": 1 });

// Thread indexes
db.threads.createIndex({ "id": 1 }, { unique: true });
db.threads.createIndex({ "session_id": 1 });
db.threads.createIndex({ "created_at": -1 });

// Orchestration indexes
db.orchestration_requests.createIndex({ "request_id": 1 }, { unique: true });
db.orchestration_requests.createIndex({ "session_id": 1 });
db.orchestration_requests.createIndex({ "created_at": -1 });
db.orchestration_requests.createIndex({ "status": 1 });

// AI response indexes
db.ai_responses.createIndex({ "response_id": 1 }, { unique: true });
db.ai_responses.createIndex({ "request_id": 1 });
db.ai_responses.createIndex({ "provider": 1 });
db.ai_responses.createIndex({ "model": 1 });
db.ai_responses.createIndex({ "created_at": -1 });

// Performance metrics indexes
db.performance_metrics.createIndex({ "request_id": 1 });
db.performance_metrics.createIndex({ "provider": 1 });
db.performance_metrics.createIndex({ "model": 1 });
db.performance_metrics.createIndex({ "timestamp": -1 });

// Cost tracking indexes
db.cost_tracking.createIndex({ "request_id": 1 });
db.cost_tracking.createIndex({ "provider": 1 });
db.cost_tracking.createIndex({ "date": -1 });

// Model analytics indexes
db.model_analytics.createIndex({ "model": 1 });
db.model_analytics.createIndex({ "provider": 1 });
db.model_analytics.createIndex({ "date": -1 });

// Prompt history indexes
db.prompt_history.createIndex({ "prompt_id": 1 }, { unique: true });
db.prompt_history.createIndex({ "session_id": 1 });
db.prompt_history.createIndex({ "created_at": -1 });

// User preferences indexes
db.user_preferences.createIndex({ "user_id": 1 }, { unique: true });

echo "✅ Indexes created successfully!"
EOF

echo "🎉 OrchestrateX Database initialization completed successfully!"
echo "📊 Database: orchestratex"
echo "📁 Collections: 9 collections created"
echo "🔍 Indexes: Optimized for performance"
echo "🔐 Security: Schema validation enabled"
