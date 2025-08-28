# OrchestrateX Database Schema Documentation

## 📋 Overview

This documentation provides comprehensive information about the OrchestrateX database schema, designed for a sophisticated multi-AI orchestration system that intelligently selects models, manages iterative improvements, and tracks performance metrics.

## 🏗️ Architecture

### System Design Principles
- **Multi-AI Orchestration**: Supports dynamic model selection based on prompt analysis
- **Iterative Improvement**: Enables up to 10 rounds of criticism and refinement
- **Performance Tracking**: Comprehensive analytics and cost monitoring
- **Quality Assurance**: Built-in evaluation and scoring mechanisms
- **Scalability**: Optimized indexes and efficient query patterns

## 📁 File Structure

```
database/
├── schema.js              # MongoDB schema definitions with validation
├── indexes.js             # Collection indexes for performance optimization
├── init_db.js             # Database initialization script
├── enhanced_schema.md     # Detailed schema documentation
└── README.md             # This documentation file
```

## 🗃️ Collections Overview

### Core Collections (9 total)

| Collection | Purpose | Key Features |
|------------|---------|--------------|
| `user_sessions` | User session management | Session tracking, cost limits, user preferences |
| `conversation_threads` | Individual conversations | Thread lifecycle, quality scoring, final responses |
| `ai_model_profiles` | AI model configurations | Model capabilities, specialties, performance metrics |
| `model_responses` | AI model responses | Response content, performance data, quality scores |
| `model_evaluations` | Response evaluations | Multi-criteria scoring, criticism, improvement suggestions |
| `model_selection_history` | Selection decisions | Algorithm decisions, success tracking, performance analysis |
| `criticism_responses` | Improvement responses | Response to criticism, iterative improvements |
| `orchestration_logs` | System logging | Operational logs, error tracking, system health |
| `algorithm_metrics` | Performance analytics | Usage statistics, cost analysis, quality trends |

## 🔗 Integration Guide

### 1. Backend Integration

#### FastAPI/Python Integration
```python
# Use the Pydantic models in backend/app/models/schemas.py
from app.models.schemas import (
    UserSessionCreate,
    ConversationThreadCreate,
    OrchestrationRequest,
    ModelResponse
)

# Example: Create a new session
session_data = UserSessionCreate(
    user_id="user123",
    max_iterations=5,
    settings={"preferred_models": ["gpt4", "claude"]}
)
```

#### Database Connection
```python
# Use the database configuration in backend/app/core/database.py
from app.core.database import get_database

db = await get_database()
sessions_collection = db.user_sessions
```

### 2. MongoDB Integration

#### Schema Validation
```javascript
// Apply schema validation using schema.js
const { userSessionsSchema } = require('./schema.js');

db.createCollection("user_sessions", {
    validator: userSessionsSchema
});
```

#### Index Creation
```javascript
// Create optimized indexes using indexes.js
const { createOrchestrateXIndexes } = require('./indexes.js');

createOrchestrateXIndexes(db);
```

### 3. Docker Integration

#### Environment Variables
```yaml
# docker-compose.yml configuration
environment:
  MONGO_INITDB_ROOT_USERNAME: project_admin
  MONGO_INITDB_ROOT_PASSWORD: project_password
  MONGO_INITDB_DATABASE: orchestratex
```

#### Volume Mounts
```yaml
volumes:
  - ./database/init_db.js:/docker-entrypoint-initdb.d/01-init_db.js:ro
  - ./init-scripts/init-users.js:/docker-entrypoint-initdb.d/02-init-users.js:ro
```

## 🚀 Quick Start

### 1. Initialize Database
```bash
# Start MongoDB container
docker compose up -d

# Connect to MongoDB
mongosh mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin
```

### 2. Create Collections with Validation
```javascript
// Run in MongoDB shell
load('/path/to/schema.js');
load('/path/to/indexes.js');

// Create collections with validation
db.createCollection("user_sessions", { validator: userSessionsSchema });
db.createCollection("conversation_threads", { validator: conversationThreadsSchema });
// ... repeat for other collections

// Create optimized indexes
createOrchestrateXIndexes(db);
```

### 3. Verify Setup
```javascript
// Check collections
show collections;

// Verify indexes
db.user_sessions.getIndexes();

// Test insertion
db.user_sessions.insertOne({
    user_id: "test_user",
    session_start: new Date(),
    max_iterations: 5,
    status: "active"
});
```

## 📊 Query Patterns

### Common Queries

#### 1. Find Active Sessions
```javascript
db.user_sessions.find({
    status: "active",
    session_start: { $gte: new Date(Date.now() - 24*60*60*1000) }
}).sort({ session_start: -1 });
```

#### 2. Get Thread Performance
```javascript
db.conversation_threads.aggregate([
    { $match: { domain: "coding" } },
    { $group: {
        _id: "$best_model_id",
        avg_quality: { $avg: "$final_quality_score" },
        avg_cost: { $avg: "$total_cost" },
        count: { $sum: 1 }
    }},
    { $sort: { avg_quality: -1 } }
]);
```

#### 3. Model Performance Analysis
```javascript
db.model_responses.aggregate([
    { $match: { is_selected_best: true } },
    { $group: {
        _id: "$model_name",
        avg_response_time: { $avg: "$response_time" },
        avg_selection_score: { $avg: "$selection_score" },
        total_responses: { $sum: 1 }
    }},
    { $sort: { avg_selection_score: -1 } }
]);
```

## 🔧 Maintenance

### Index Management
```javascript
// Analyze index usage
analyzeIndexUsage(db);

// Rebuild indexes if needed
db.collection.reIndex();

// Monitor slow queries
db.setProfilingLevel(2, { slowms: 100 });
db.system.profile.find().sort({ ts: -1 }).limit(5);
```

### Performance Optimization
```javascript
// Collection statistics
db.user_sessions.stats();

// Query performance
db.conversation_threads.explain("executionStats").find({
    domain: "coding",
    thread_status: "completed"
});
```

## 🔒 Security Considerations

### 1. Authentication
- Root admin user: `project_admin`
- Application user: `orchestratex_app` (read/write access)
- Read-only user: `orchestratex_readonly` (analytics access)

### 2. Data Validation
- Schema validation on all collections
- Required field enforcement
- Data type validation
- Range checks for numeric values

### 3. Access Control
```javascript
// Grant appropriate roles
db.grantRolesToUser("orchestratex_app", [
    { role: "readWrite", db: "orchestratex" }
]);
```

## 📈 Monitoring

### Key Metrics to Track
1. **Session Metrics**: Active sessions, completion rates, user satisfaction
2. **Performance Metrics**: Response times, token usage, API costs
3. **Quality Metrics**: Evaluation scores, improvement rates, user acceptance
4. **System Health**: Error rates, uptime, resource usage

### Monitoring Queries
```javascript
// Daily session summary
db.user_sessions.aggregate([
    { $match: { 
        session_start: { 
            $gte: new Date(Date.now() - 24*60*60*1000) 
        }
    }},
    { $group: {
        _id: null,
        total_sessions: { $sum: 1 },
        completed_sessions: { 
            $sum: { $cond: [{ $eq: ["$status", "completed"] }, 1, 0] }
        },
        total_cost: { $sum: "$total_cost" },
        avg_satisfaction: { $avg: "$user_satisfaction" }
    }}
]);
```

## 🔄 Migration Scripts

### Version Updates
When updating schema versions, use migration scripts:

```javascript
// Example migration for adding new fields
db.user_sessions.updateMany(
    { settings: { $exists: false } },
    { $set: { settings: {} } }
);
```

## 📞 Support

### Common Issues

1. **Connection Issues**: Check MongoDB container status and credentials
2. **Validation Errors**: Verify data against schema requirements
3. **Performance Issues**: Analyze index usage and query patterns
4. **Disk Space**: Monitor collection sizes and implement archiving

### Troubleshooting Commands
```javascript
// Check database status
db.runCommand({ serverStatus: 1 });

// Validate collections
db.user_sessions.validate();

// Check replication lag (if using replica sets)
rs.printReplicationInfo();
```

## 📝 Changelog

### Version 1.0 (Current)
- Initial schema design
- Core 9 collections implemented
- Comprehensive indexing strategy
- Schema validation rules
- User management system

### Planned Features
- Sharding configuration for horizontal scaling
- Time-series collections for metrics
- Advanced analytics collections
- Automated archiving system

---

**Note**: This schema is designed for a production-ready multi-AI orchestration system. For development environments, you may want to adjust validation rules and index strategies based on your specific use case.

For questions or support, refer to the detailed schema documentation in `enhanced_schema.md` or check the initialization scripts in the `init-scripts/` directory.
