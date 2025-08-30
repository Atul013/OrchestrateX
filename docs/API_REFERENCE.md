# OrchestrateX API Documentation

## Overview
OrchestrateX is a multi-AI orchestration system that intelligently routes prompts to the most suitable AI model and uses iterative improvement through multi-model evaluation.

## Authentication
Currently, the API uses project-level authentication for MongoDB. In production, implement proper JWT or API key authentication.

## Base URL
- Development: `http://localhost:8000`
- Production: TBD

## Common Response Format
All API responses follow this structure:
```json
{
  "_id": "ObjectId",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp",
  // ... endpoint-specific fields
}
```

## Error Responses
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

---

## Sessions API

### Create Session
**POST** `/api/sessions/`

Creates a new user session for AI orchestration.

**Request Body:**
```json
{
  "user_id": "string",
  "max_iterations": 5,
  "settings": {
    "preferred_models": ["gpt4", "claude"],
    "cost_limit": 10.0
  }
}
```

**Response (201):**
```json
{
  "_id": "68b2c9faa82de4230e87701c",
  "user_id": "test_user_123",
  "session_start": "2025-08-30T09:52:58.278000",
  "session_end": null,
  "max_iterations": 5,
  "status": "active",
  "total_cost": 0.0,
  "settings": {
    "preferred_models": ["gpt4", "claude"],
    "cost_limit": 10.0
  },
  "created_at": "2025-08-30T09:52:58.278000"
}
```

### Get Session
**GET** `/api/sessions/{session_id}`

Retrieves a specific session by ID.

**Response (200):**
```json
{
  "_id": "68b2c9faa82de4230e87701c",
  "user_id": "test_user_123",
  "status": "active",
  // ... other session fields
}
```

### List User Sessions
**GET** `/api/sessions/user/{user_id}`

Lists all sessions for a specific user.

**Response (200):**
```json
[
  {
    "_id": "68b2c9faa82de4230e87701c",
    "user_id": "test_user_123",
    "status": "active",
    // ... other session fields
  }
]
```

### Update Session Status
**PATCH** `/api/sessions/{session_id}/status`

Updates the status of a session.

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response (200):**
```json
{
  "_id": "68b2c9faa82de4230e87701c",
  "status": "completed",
  // ... other session fields
}
```

---

## Threads API

### Create Thread
**POST** `/api/threads/`

Creates a new conversation thread within a session.

**Request Body:**
```json
{
  "session_id": "68b2c9faa82de4230e87701c",
  "original_prompt": "Write a Python function to calculate fibonacci numbers",
  "domain": "coding",
  "context": "This is for a beginner programming tutorial"
}
```

### Get Thread
**GET** `/api/threads/{thread_id}`

Retrieves a specific thread by ID.

### List Session Threads
**GET** `/api/threads/session/{session_id}`

Lists all threads for a specific session.

---

## Orchestration API

### Start Orchestration
**POST** `/api/orchestration/start`

Starts the AI orchestration process for a thread.

**Request Body:**
```json
{
  "thread_id": "68b2c9faa82de4230e87701c",
  "prompt": "Write a Python function to calculate fibonacci numbers",
  "settings": {
    "max_iterations": 5,
    "preferred_models": ["gpt4", "claude"],
    "evaluation_threshold": 8.0
  }
}
```

### Get Orchestration Status
**GET** `/api/orchestration/status/{orchestration_id}`

Retrieves the status and results of an orchestration process.

---

## Models API

### List Available Models
**GET** `/api/models/`

Lists all available AI models and their configurations.

**Response (200):**
```json
[
  {
    "name": "gpt4",
    "provider": "openai",
    "version": "gpt-4-0125-preview",
    "specialties": ["coding", "analysis", "general"],
    "cost_per_1k_tokens": 0.03,
    "context_window": 128000,
    "status": "active"
  }
]
```

### Get Model Profile
**GET** `/api/models/{model_name}`

Retrieves detailed information about a specific model.

---

## Analytics API

### Get Session Analytics
**GET** `/api/analytics/session/{session_id}`

Retrieves analytics for a specific session.

### Get User Analytics
**GET** `/api/analytics/user/{user_id}`

Retrieves analytics for a specific user.

---

## WebSocket Events

### Connection
Connect to: `ws://localhost:8000/ws/{session_id}`

### Event Types

#### Orchestration Started
```json
{
  "type": "orchestration_started",
  "thread_id": "...",
  "timestamp": "2025-08-30T09:52:58.278000"
}
```

#### Model Selected
```json
{
  "type": "model_selected",
  "model_name": "gpt4",
  "reasoning": "Best for coding tasks",
  "timestamp": "2025-08-30T09:52:58.278000"
}
```

#### Response Generated
```json
{
  "type": "response_generated",
  "model_name": "gpt4",
  "response_preview": "def fibonacci(n):",
  "tokens_used": 150,
  "timestamp": "2025-08-30T09:52:58.278000"
}
```

#### Evaluation Completed
```json
{
  "type": "evaluation_completed",
  "evaluator_model": "claude",
  "score": 8.5,
  "feedback": "Good implementation, could use better error handling",
  "timestamp": "2025-08-30T09:52:58.278000"
}
```

#### Orchestration Completed
```json
{
  "type": "orchestration_completed",
  "final_response": "...",
  "iterations": 3,
  "final_score": 9.2,
  "total_cost": 0.15,
  "timestamp": "2025-08-30T09:52:58.278000"
}
```

---

## Rate Limits
- 100 requests per minute per session
- 10 concurrent orchestrations per user
- 5 MB maximum request size

## Response Times
- Sessions API: < 100ms
- Orchestration: 10-60 seconds (depending on iterations)
- Analytics: < 500ms

## Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Validation Error
- 429: Rate Limited
- 500: Internal Server Error
