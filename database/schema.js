// MongoDB Schema Definitions for OrchestrateX
// Collection schemas with validation rules and structure definitions

// 1. User Sessions Schema
const userSessionsSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["user_id", "session_start", "max_iterations", "status"],
    properties: {
      _id: { bsonType: "objectId" },
      user_id: { 
        bsonType: "string",
        description: "Unique user identifier"
      },
      session_start: { 
        bsonType: "date",
        description: "Session start timestamp"
      },
      session_end: { 
        bsonType: "date",
        description: "Session end timestamp"
      },
      max_iterations: { 
        bsonType: "int",
        minimum: 1,
        maximum: 10,
        description: "Maximum orchestration iterations allowed"
      },
      status: {
        enum: ["active", "completed", "terminated", "error"],
        description: "Current session status"
      },
      total_cost: {
        bsonType: "double",
        minimum: 0,
        description: "Cumulative API costs for session"
      },
      user_satisfaction: {
        bsonType: "double",
        minimum: 1,
        maximum: 10,
        description: "Post-session user rating"
      },
      settings: {
        bsonType: "object",
        properties: {
          preferred_models: {
            bsonType: "array",
            items: { bsonType: "string" }
          },
          excluded_models: {
            bsonType: "array", 
            items: { bsonType: "string" }
          },
          cost_limit: { bsonType: "double" },
          quality_threshold: { bsonType: "double" }
        }
      },
      created_at: { bsonType: "date" },
      updated_at: { bsonType: "date" }
    }
  }
};

// 2. Conversation Threads Schema
const conversationThreadsSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["session_id", "original_prompt", "domain", "thread_status"],
    properties: {
      _id: { bsonType: "objectId" },
      session_id: { 
        bsonType: "objectId",
        description: "Reference to user_sessions collection"
      },
      original_prompt: { 
        bsonType: "string",
        minLength: 1,
        description: "User's initial question/task"
      },
      processed_prompt: { 
        bsonType: "string",
        description: "Cleaned/enhanced version of prompt"
      },
      domain: {
        enum: ["coding", "creative", "factual", "math", "translation", "sentiment", "general"],
        description: "Problem domain classification"
      },
      complexity_level: {
        enum: ["simple", "moderate", "complex", "expert"],
        description: "Estimated problem complexity"
      },
      estimated_difficulty: {
        bsonType: "double",
        minimum: 1,
        maximum: 10
      },
      language: { 
        bsonType: "string",
        description: "Language code (en, es, fr, etc.)"
      },
      context: { 
        bsonType: "string",
        description: "Additional context or requirements"
      },
      current_iteration: {
        bsonType: "int",
        minimum: 0,
        description: "Current orchestration round"
      },
      max_iterations_reached: { bsonType: "bool" },
      best_model_id: { 
        bsonType: "string",
        description: "Current best performing model"
      },
      best_response_id: { 
        bsonType: "objectId",
        description: "Current best response reference"
      },
      thread_status: {
        enum: ["initializing", "model_selection", "responding", "evaluating", "criticism", "refining", "completed", "failed"],
        description: "Current thread processing status"
      },
      failure_reason: { bsonType: "string" },
      final_response: { 
        bsonType: "string",
        description: "Best response shown to user"
      },
      final_quality_score: {
        bsonType: "double",
        minimum: 1,
        maximum: 10
      },
      user_accepted: { bsonType: "bool" },
      total_models_involved: { bsonType: "int" },
      total_tokens_used: { bsonType: "int" },
      total_cost: { bsonType: "double" },
      total_time_spent: { bsonType: "int" },
      created_at: { bsonType: "date" },
      updated_at: { bsonType: "date" },
      completed_at: { bsonType: "date" }
    }
  }
};

// 3. AI Model Profiles Schema
const aiModelProfilesSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["model_name", "provider", "specialties", "is_active"],
    properties: {
      _id: { bsonType: "objectId" },
      model_name: {
        enum: ["gpt4", "gpt4-turbo", "grok", "qwen", "claude", "llama", "mistral", "gemini"],
        description: "AI model identifier"
      },
      provider: {
        enum: ["openai", "anthropic", "xai", "alibaba", "meta", "google"],
        description: "AI service provider"
      },
      model_version: { 
        bsonType: "string",
        description: "Specific version identifier"
      },
      specialties: {
        bsonType: "array",
        items: {
          enum: ["coding", "creative", "math", "translation", "reasoning", "analysis"]
        },
        description: "Model specialty areas"
      },
      supported_languages: {
        bsonType: "array",
        items: { bsonType: "string" },
        description: "Programming and natural languages supported"
      },
      max_context_length: {
        bsonType: "int",
        minimum: 1000,
        description: "Maximum tokens in context"
      },
      strengths: { bsonType: "string" },
      weaknesses: { bsonType: "string" },
      best_use_cases: {
        bsonType: "array",
        items: { bsonType: "string" }
      },
      api_endpoint: { bsonType: "string" },
      api_key_required: { bsonType: "bool" },
      cost_per_input_token: { bsonType: "double" },
      cost_per_output_token: { bsonType: "double" },
      rate_limits: {
        bsonType: "object",
        properties: {
          requests_per_minute: { bsonType: "int" },
          tokens_per_minute: { bsonType: "int" }
        }
      },
      is_active: { bsonType: "bool" },
      is_available: { bsonType: "bool" },
      last_health_check: { bsonType: "date" },
      performance_metrics: {
        bsonType: "object",
        properties: {
          average_response_time: { bsonType: "double" },
          success_rate: { bsonType: "double" },
          average_quality_rating: { bsonType: "double" },
          total_requests: { bsonType: "int" },
          total_tokens_processed: { bsonType: "int" },
          uptime_percentage: { bsonType: "double" }
        }
      },
      created_at: { bsonType: "date" },
      updated_at: { bsonType: "date" }
    }
  }
};

// 4. Model Responses Schema
const modelResponsesSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["thread_id", "session_id", "model_name", "response_text", "iteration_number"],
    properties: {
      _id: { bsonType: "objectId" },
      thread_id: { 
        bsonType: "objectId",
        description: "Reference to conversation_threads"
      },
      session_id: { 
        bsonType: "objectId",
        description: "Reference to user_sessions"
      },
      iteration_number: {
        bsonType: "int",
        minimum: 1,
        description: "Which evaluation round"
      },
      model_name: { 
        bsonType: "string",
        description: "Responding model identifier"
      },
      role: {
        enum: ["primary", "evaluator", "critic", "refiner"],
        description: "Model's role in this response"
      },
      response_type: {
        enum: ["initial", "evaluation", "criticism", "improvement", "final"],
        description: "Type of response"
      },
      response_text: { 
        bsonType: "string",
        minLength: 1,
        description: "Actual response content"
      },
      prompt_sent: { 
        bsonType: "string",
        description: "Exact prompt sent to model"
      },
      context_provided: { bsonType: "string" },
      parent_response_id: { 
        bsonType: "objectId",
        description: "If responding to another response"
      },
      criticism_addressed: {
        bsonType: "array",
        items: { bsonType: "objectId" },
        description: "Criticisms this response addresses"
      },
      response_time: {
        bsonType: "double",
        minimum: 0,
        description: "Response time in milliseconds"
      },
      tokens_used: {
        bsonType: "object",
        properties: {
          input_tokens: { bsonType: "int" },
          output_tokens: { bsonType: "int" },
          total_tokens: { bsonType: "int" }
        }
      },
      cost: {
        bsonType: "double",
        minimum: 0,
        description: "API cost for this request"
      },
      confidence_score: {
        bsonType: "double",
        minimum: 1,
        maximum: 10,
        description: "Model's confidence in response"
      },
      self_assessment: { 
        bsonType: "string",
        description: "Model's own evaluation"
      },
      is_selected_best: { 
        bsonType: "bool",
        description: "Currently considered best response"
      },
      selection_score: {
        bsonType: "double",
        minimum: 0,
        maximum: 10,
        description: "Algorithm's scoring of this response"
      },
      status: {
        enum: ["pending", "completed", "failed", "superseded"],
        description: "Response processing status"
      },
      error_message: { bsonType: "string" },
      timestamp: { bsonType: "date" },
      processing_duration: {
        bsonType: "double",
        minimum: 0,
        description: "Total processing time"
      }
    }
  }
};

// Export schemas for use in database initialization
module.exports = {
  userSessionsSchema,
  conversationThreadsSchema,
  aiModelProfilesSchema,
  modelResponsesSchema,
  
  // Additional schemas for other collections
  modelEvaluationsSchema: {
    $jsonSchema: {
      bsonType: "object",
      required: ["thread_id", "evaluated_response_id", "evaluator_model", "overall_score"],
      properties: {
        _id: { bsonType: "objectId" },
        thread_id: { bsonType: "objectId" },
        session_id: { bsonType: "objectId" },
        evaluated_response_id: { bsonType: "objectId" },
        evaluator_model: { bsonType: "string" },
        iteration_number: { bsonType: "int" },
        evaluation_criteria: {
          bsonType: "object",
          properties: {
            accuracy: { bsonType: "double", minimum: 1, maximum: 10 },
            relevance: { bsonType: "double", minimum: 1, maximum: 10 },
            clarity: { bsonType: "double", minimum: 1, maximum: 10 },
            completeness: { bsonType: "double", minimum: 1, maximum: 10 },
            creativity: { bsonType: "double", minimum: 1, maximum: 10 },
            efficiency: { bsonType: "double", minimum: 1, maximum: 10 },
            safety: { bsonType: "double", minimum: 1, maximum: 10 },
            domain_expertise: { bsonType: "double", minimum: 1, maximum: 10 }
          }
        },
        overall_score: { bsonType: "double", minimum: 1, maximum: 10 },
        criticism_text: { bsonType: "string" },
        positive_aspects: { bsonType: "string" },
        suggested_improvements: { bsonType: "string" },
        timestamp: { bsonType: "date" }
      }
    }
  }
};
