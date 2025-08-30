// Switch to orchestratex database
// use orchestratex; // Removed: not valid in JavaScript files

// Create collections
db.createCollection("user_sessions");
db.createCollection("conversation_threads");
db.createCollection("ai_model_profiles");
db.createCollection("model_responses");
db.createCollection("model_evaluations");
db.createCollection("model_selection_history");
db.createCollection("criticism_responses");
db.createCollection("orchestration_logs");
db.createCollection("algorithm_metrics");

// Insert AI model profiles
db.ai_model_profiles.insertMany([
  {
    model_name: "gpt4",
    provider: "openai",
    model_version: "gpt-4-turbo",
    specialties: ["coding", "reasoning", "general"],
    supported_languages: ["en", "es", "fr", "de", "python", "javascript", "java"],
    max_context_length: 128000,
    strengths: "Excellent reasoning, coding, and general knowledge",
    weaknesses: "Higher cost, slower response time",
    best_use_cases: ["complex coding", "detailed analysis", "reasoning tasks"],
    api_endpoint: "https://api.openai.com/v1/chat/completions",
    api_key_required: true,
    cost_per_input_token: 0.01,
    cost_per_output_token: 0.03,
    is_active: true,
    is_available: true,
    performance_metrics: {
      average_response_time: 2500,
      success_rate: 0.98,
      average_quality_rating: 9.2,
      total_requests: 0,
      total_tokens_processed: 0,
      uptime_percentage: 99.5
    },
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    model_name: "claude",
    provider: "anthropic",
    model_version: "claude-3.5-sonnet",
    specialties: ["creative", "analysis", "safety"],
    supported_languages: ["en", "es", "fr", "de", "python", "javascript"],
    max_context_length: 200000,
    strengths: "Creative writing, ethical reasoning, safe responses",
    weaknesses: "Limited real-time data, coding less optimal",
    best_use_cases: ["creative writing", "analysis", "ethical discussions"],
    api_endpoint: "https://api.anthropic.com/v1/messages",
    api_key_required: true,
    cost_per_input_token: 0.015,
    cost_per_output_token: 0.075,
    is_active: true,
    is_available: true,
    performance_metrics: {
      average_response_time: 3000,
      success_rate: 0.97,
      average_quality_rating: 8.8,
      total_requests: 0,
      total_tokens_processed: 0,
      uptime_percentage: 98.2
    },
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    model_name: "grok",
    provider: "xai",
    model_version: "grok-1",
    specialties: ["humor", "current_events", "general"],
    supported_languages: ["en", "python", "javascript"],
    max_context_length: 128000,
    strengths: "Current events, humor, conversational",
    weaknesses: "Less formal, newer model",
    best_use_cases: ["current events", "casual conversation", "humor"],
    api_endpoint: "https://api.x.ai/v1/chat/completions",
    api_key_required: true,
    cost_per_input_token: 0.01,
    cost_per_output_token: 0.02,
    is_active: true,
    is_available: true,
    performance_metrics: {
      average_response_time: 2000,
      success_rate: 0.95,
      average_quality_rating: 8.0,
      total_requests: 0,
      total_tokens_processed: 0,
      uptime_percentage: 96.8
    },
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    model_name: "qwen",
    provider: "alibaba",
    model_version: "qwen-max",
    specialties: ["multilingual", "math", "coding"],
    supported_languages: ["en", "zh", "es", "fr", "python", "javascript", "java"],
    max_context_length: 32000,
    strengths: "Multilingual capabilities, mathematics, efficient",
    weaknesses: "Smaller context window, less known",
    best_use_cases: ["multilingual tasks", "mathematics", "efficient processing"],
    api_endpoint: "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
    api_key_required: true,
    cost_per_input_token: 0.008,
    cost_per_output_token: 0.02,
    is_active: true,
    is_available: true,
    performance_metrics: {
      average_response_time: 1800,
      success_rate: 0.94,
      average_quality_rating: 8.3,
      total_requests: 0,
      total_tokens_processed: 0,
      uptime_percentage: 97.5
    },
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    model_name: "llama",
    provider: "meta",
    model_version: "llama-3.1-70b",
    specialties: ["coding", "reasoning", "general"],
    supported_languages: ["en", "es", "fr", "python", "javascript", "cpp"],
    max_context_length: 128000,
    strengths: "Open source, good coding, reasoning",
    weaknesses: "Requires more setup, hosting costs",
    best_use_cases: ["open source projects", "coding", "custom deployment"],
    api_endpoint: "https://api.groq.com/openai/v1/chat/completions",
    api_key_required: true,
    cost_per_input_token: 0.0006,
    cost_per_output_token: 0.0006,
    is_active: true,
    is_available: true,
    performance_metrics: {
      average_response_time: 1500,
      success_rate: 0.93,
      average_quality_rating: 8.1,
      total_requests: 0,
      total_tokens_processed: 0,
      uptime_percentage: 95.2
    },
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    model_name: "mistral",
    provider: "mistral",
    model_version: "mistral-large",
    specialties: ["coding", "reasoning", "efficiency"],
    supported_languages: ["en", "fr", "es", "python", "javascript"],
    max_context_length: 128000,
    strengths: "Fast, efficient, good coding",
    weaknesses: "Less creative, newer provider",
    best_use_cases: ["fast processing", "coding", "efficiency focused tasks"],
    api_endpoint: "https://api.mistral.ai/v1/chat/completions",
    api_key_required: true,
    cost_per_input_token: 0.008,
    cost_per_output_token: 0.024,
    is_active: true,
    is_available: true,
    performance_metrics: {
      average_response_time: 1200,
      success_rate: 0.96,
      average_quality_rating: 8.4,
      total_requests: 0,
      total_tokens_processed: 0,
      uptime_percentage: 98.1
    },
    created_at: new Date(),
    updated_at: new Date()
  }
]);

// Create comprehensive indexes for performance optimization
db.user_sessions.createIndex({ "user_id": 1, "session_start": -1 });
db.user_sessions.createIndex({ "status": 1, "created_at": -1 });

db.conversation_threads.createIndex({ "session_id": 1, "created_at": -1 });
db.conversation_threads.createIndex({ "domain": 1, "thread_status": 1 });
db.conversation_threads.createIndex({ "best_model_id": 1, "final_quality_score": -1 });

db.model_responses.createIndex({ "thread_id": 1, "iteration_number": 1 });
db.model_responses.createIndex({ "model_name": 1, "timestamp": -1 });
db.model_responses.createIndex({ "is_selected_best": 1, "selection_score": -1 });

db.model_evaluations.createIndex({ "thread_id": 1, "iteration_number": 1 });
db.model_evaluations.createIndex({ "evaluator_model": 1, "overall_score": -1 });
db.model_evaluations.createIndex({ "evaluated_response_id": 1 });

db.model_selection_history.createIndex({ "thread_id": 1, "iteration_number": 1 });
db.model_selection_history.createIndex({ "selected_model": 1, "selection_success": 1 });

db.criticism_responses.createIndex({ "thread_id": 1, "iteration_number": 1 });
db.criticism_responses.createIndex({ "original_response_id": 1 });

db.orchestration_logs.createIndex({ "session_id": 1, "timestamp": -1 });
db.orchestration_logs.createIndex({ "log_level": 1, "timestamp": -1 });

db.algorithm_metrics.createIndex({ "metric_name": 1, "timestamp": -1 });
db.algorithm_metrics.createIndex({ "session_id": 1, "timestamp": -1 });

db.ai_model_profiles.createIndex({ "model_name": 1 });
db.ai_model_profiles.createIndex({ "specialties": 1 });
db.ai_model_profiles.createIndex({ "is_active": 1, "is_available": 1 });

// Verify setup
print("=== OrchestrateX Database Initialization Complete ===");
print("Collections created:");
db.getCollectionNames().forEach(function(collection) {
    print("- " + collection);
});

print("\nAI Models configured:");
db.ai_model_profiles.find({}, {model_name: 1, provider: 1, specialties: 1}).forEach(function(model) {
    print("- " + model.model_name + " (" + model.provider + ") - " + model.specialties.join(", "));
});

print("\nIndexes created for optimal performance.");
print("Database setup complete!");
print("Collections created: " + db.getCollectionNames().length);
