# Database Setup Scripts - Usage Guide

## Overview
This folder contains MongoDB initialization scripts for the OrchestrateX multi-AI orchestration system.

## Fixed Issues
✅ **init_db.js** - Now includes all 6 AI models with complete profiles
✅ **setup_database.js** - Added error handling, validation, and comprehensive indexes
✅ **test_db_scripts.js** - New validation script to test setup

## Files Description

### 1. init_db.js (Quick Setup)
- **Purpose**: Minimal database initialization
- **Contains**: All 6 AI models with full profiles, essential indexes
- **Use when**: Quick setup for development

### 2. setup_database.js (Full Setup)
- **Purpose**: Comprehensive database setup with validation
- **Contains**: All collections, 6 AI models, comprehensive indexes, error handling
- **Use when**: Production setup or detailed initialization

### 3. test_db_scripts.js (Validation)
- **Purpose**: Test and validate database setup
- **Contains**: Connection tests, collection validation, model verification
- **Use when**: Verifying setup is correct

## How to Use

### Prerequisites
1. **Docker Desktop** running
2. **MongoDB container** running on port 27018
3. **Authentication**: project_admin/project_password

### Option 1: MongoDB Compass (Recommended)
1. Open MongoDB Compass
2. Connect using: `mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin`
3. Open the MongoSH tab
4. Copy and paste content from `setup_database.js`
5. Press Enter to execute

### Option 2: MongoDB Shell (mongosh)
```powershell
# Connect to MongoDB
mongosh "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin"

# Load and run setup script
load("C:/Users/kalad/OrchestrateX/database/setup_database.js")
```

### Option 3: Quick Setup (init_db.js)
```powershell
# For minimal setup
mongosh "mongodb://project_admin:project_password@localhost:27018/orchestratex?authSource=admin" < init_db.js
```

### Option 4: Validate Setup
```powershell
# First install mongodb dependency
npm install mongodb

# Run validation test
node test_db_scripts.js
```

## Expected Output

### Successful Setup Should Show:
```
=== OrchestrateX Database Setup Complete ===
Collections created:
- user_sessions
- conversation_threads
- ai_model_profiles
- model_responses
- model_evaluations
- model_selection_history
- criticism_responses
- orchestration_logs
- algorithm_metrics

AI Models configured:
- gpt4 (openai) - coding, reasoning, general
- claude (anthropic) - creative, analysis, safety
- grok (xai) - humor, current_events, general
- qwen (alibaba) - multilingual, math, coding
- llama (meta) - coding, reasoning, general
- mistral (mistral) - coding, reasoning, efficiency

Validating setup...
Total collections: 9
Total AI models: 6
Active models: 6

🎉 Database ready for OrchestrateX multi-AI orchestration system!
```

## Collections Created

1. **user_sessions** - User session management
2. **conversation_threads** - Individual conversation tracking
3. **ai_model_profiles** - AI model configurations and metadata
4. **model_responses** - Responses from different AI models
5. **model_evaluations** - Quality evaluations of responses
6. **model_selection_history** - Track which models were selected
7. **criticism_responses** - Criticism and feedback from other models
8. **orchestration_logs** - System orchestration logs
9. **algorithm_metrics** - Performance metrics and analytics

## AI Models Configured

| Model | Provider | Specialties | Context Length |
|-------|----------|-------------|----------------|
| GPT-4 | OpenAI | Coding, Reasoning, General | 128,000 |
| Claude | Anthropic | Creative, Analysis, Safety | 200,000 |
| Grok | X.AI | Humor, Current Events | 128,000 |
| Qwen | Alibaba | Multilingual, Math, Coding | 32,000 |
| LLaMA | Meta | Coding, Reasoning, General | 128,000 |
| Mistral | Mistral | Coding, Reasoning, Efficiency | 128,000 |

## Troubleshooting

### Connection Issues
- Ensure Docker Desktop is running
- Check MongoDB container is on port 27018
- Verify credentials: project_admin/project_password

### Script Errors
- Use MongoDB Compass for better error reporting
- Check MongoDB version compatibility (8.0+)
- Ensure proper authentication

### Performance Issues
- All collections have optimized indexes
- Use compound indexes for complex queries
- Monitor using MongoDB Compass performance tab

## Next Steps
After successful database setup:
1. Start FastAPI backend: `uvicorn backend.main:app --reload`
2. Test API endpoints at `http://localhost:8000/docs`
3. Begin implementing orchestration algorithms
