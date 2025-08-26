# Enhanced Database Schema for OrchestrateX Multi-AI Orchestration System

## System Overview
This schema supports an orchestrated multi-AI system where:
1. Algorithm selects the best model based on prompt domain/specialty
2. Selected model provides initial response
3. Other models evaluate and criticize the response
4. Best model responds to criticism and improves answer
5. Process iterates up to user-defined limit (max 10 rounds)
6. User only sees final best responses

## Core Collections

### 1. User Sessions Collection
```javascript
// user_sessions
{
  _id: ObjectId,
  user_id: "String - unique user identifier",
  session_start: "Date",
  session_end: "Date",
  max_iterations: "Number - user-defined limit (max 10)",
  status: "String - active|completed|terminated|error",
  total_cost: "Number - cumulative API costs",
  user_satisfaction: "Number 1-10 - post-session rating",
  settings: {
    preferred_models: ["Array of model names"],
    excluded_models: ["Array of model names"],
    cost_limit: "Number - maximum spending per session",
    quality_threshold: "Number - minimum acceptable score"
  },
  created_at: "Date",
  updated_at: "Date"
}
```

### 2. Conversation Threads Collection
```javascript
// conversation_threads
{
  _id: ObjectId,
  session_id: "ObjectId - reference to user_sessions",
  original_prompt: "String - user's initial question/task",
  processed_prompt: "String - cleaned/enhanced version",
  domain: "String - coding|creative|factual|math|translation|sentiment|general",
  complexity_level: "String - simple|moderate|complex|expert",
  estimated_difficulty: "Number 1-10",
  language: "String - en|es|fr|de|etc",
  context: "String - additional context or requirements",
  
  // Orchestration tracking
  current_iteration: "Number - current round of evaluation",
  max_iterations_reached: "Boolean",
  best_model_id: "String - current best performing model",
  best_response_id: "ObjectId - current best response",
  
  // Thread lifecycle
  thread_status: "String - initializing|model_selection|responding|evaluating|criticism|refining|completed|failed",
  failure_reason: "String - if status is failed",
  
  // Final output
  final_response: "String - best response shown to user",
  final_quality_score: "Number 1-10",
  user_accepted: "Boolean - did user accept the final response",
  
  // Metadata
  total_models_involved: "Number",
  total_tokens_used: "Number",
  total_cost: "Number",
  total_time_spent: "Number - milliseconds",
  
  created_at: "Date",
  updated_at: "Date",
  completed_at: "Date"
}
```

### 3. AI Model Profiles Collection
```javascript
// ai_model_profiles
{
  _id: ObjectId,
  model_name: "String - gpt4|gpt4-turbo|grok|qwen|claude|llama|mistral|gemini",
  provider: "String - openai|anthropic|xai|alibaba|meta|google",
  model_version: "String - specific version identifier",
  
  // Capabilities
  specialties: ["Array - coding, creative, math, translation, reasoning, analysis"],
  supported_languages: ["Array - programming and natural languages"],
  max_context_length: "Number - maximum tokens in context",
  
  // Performance characteristics
  strengths: "String - detailed description of model strengths",
  weaknesses: "String - known limitations",
  best_use_cases: ["Array of specific scenarios"],
  
  // API configuration
  api_endpoint: "String",
  api_key_required: "Boolean",
  cost_per_input_token: "Number",
  cost_per_output_token: "Number",
  rate_limits: {
    requests_per_minute: "Number",
    tokens_per_minute: "Number"
  },
  
  // Operational status
  is_active: "Boolean",
  is_available: "Boolean - current availability status",
  last_health_check: "Date",
  
  // Performance metrics (updated periodically)
  performance_metrics: {
    average_response_time: "Number - milliseconds",
    success_rate: "Number 0-1",
    average_quality_rating: "Number 1-10",
    total_requests: "Number",
    total_tokens_processed: "Number",
    uptime_percentage: "Number 0-100"
  },
  
  created_at: "Date",
  updated_at: "Date"
}
```

### 4. Model Responses Collection
```javascript
// model_responses
{
  _id: ObjectId,
  thread_id: "ObjectId - reference to conversation_threads",
  session_id: "ObjectId - reference to user_sessions",
  iteration_number: "Number - which evaluation round",
  
  // Response details
  model_name: "String - responding model",
  role: "String - primary|evaluator|critic|refiner",
  response_type: "String - initial|evaluation|criticism|improvement|final",
  response_text: "String - actual response content",
  
  // Context for this response
  prompt_sent: "String - exact prompt sent to model",
  context_provided: "String - additional context given",
  parent_response_id: "ObjectId - if responding to another response",
  criticism_addressed: ["Array of ObjectIds - criticisms this response addresses"],
  
  // Performance data
  response_time: "Number - milliseconds",
  tokens_used: {
    input_tokens: "Number",
    output_tokens: "Number",
    total_tokens: "Number"
  },
  cost: "Number - API cost for this request",
  
  // Quality metrics
  confidence_score: "Number 1-10 - model's confidence in response",
  self_assessment: "String - model's own evaluation of response",
  is_selected_best: "Boolean - currently considered best response",
  selection_score: "Number - algorithm's scoring of this response",
  
  // Status tracking
  status: "String - pending|completed|failed|superseded",
  error_message: "String - if status is failed",
  
  timestamp: "Date",
  processing_duration: "Number - total time from request to completion"
}
```

### 5. Model Evaluations Collection
```javascript
// model_evaluations
{
  _id: ObjectId,
  thread_id: "ObjectId",
  session_id: "ObjectId",
  evaluated_response_id: "ObjectId - response being evaluated",
  evaluator_model: "String - model performing the evaluation",
  iteration_number: "Number",
  
  // Evaluation criteria (customizable based on domain)
  evaluation_criteria: {
    accuracy: "Number 1-10 - factual correctness",
    relevance: "Number 1-10 - addresses the prompt",
    clarity: "Number 1-10 - easy to understand",
    completeness: "Number 1-10 - thorough coverage",
    creativity: "Number 1-10 - innovative approach",
    efficiency: "Number 1-10 - optimal solution",
    safety: "Number 1-10 - no harmful content",
    domain_expertise: "Number 1-10 - demonstrates field knowledge"
  },
  
  // Overall assessment
  overall_score: "Number 1-10 - weighted average of criteria",
  scoring_weights: "Object - weights used for criteria",
  
  // Detailed feedback
  criticism_text: "String - specific criticisms and issues",
  positive_aspects: "String - what was done well",
  suggested_improvements: "String - concrete improvement suggestions",
  alternative_approaches: "String - different ways to solve the problem",
  
  // Evaluator metadata
  evaluator_confidence: "Number 1-10 - how confident evaluator is",
  evaluator_speciality_match: "Number 1-10 - how well evaluator knows this domain",
  evaluation_prompt_used: "String - exact prompt sent to evaluator",
  
  // Processing details
  evaluation_time: "Number - milliseconds to complete evaluation",
  tokens_used: "Number",
  cost: "Number",
  
  timestamp: "Date"
}
```

### 6. Model Selection History Collection
```javascript
// model_selection_history
{
  _id: ObjectId,
  thread_id: "ObjectId",
  session_id: "ObjectId",
  iteration_number: "Number",
  selection_phase: "String - initial|refinement|final",
  
  // Selection algorithm details
  algorithm_version: "String - version of selection algorithm used",
  selection_strategy: "String - domain_match|performance|cost|hybrid",
  
  // Candidate analysis
  candidates_considered: [{
    model_name: "String",
    domain_match_score: "Number 1-10",
    historical_performance: "Number 1-10",
    cost_efficiency: "Number 1-10",
    availability_score: "Number 1-10",
    specialty_alignment: "Number 1-10",
    final_score: "Number 1-10",
    selection_reasoning: "String"
  }],
  
  // Final selection
  selected_model: "String - chosen model",
  selection_confidence: "Number 1-10",
  runner_up_model: "String - second choice",
  selection_margin: "Number - score difference between top 2",
  
  // Decision factors
  primary_selection_factors: ["Array of key decision factors"],
  override_reasons: "String - any manual overrides applied",
  
  // Outcome tracking
  selection_success: "Boolean - was this a good choice in hindsight",
  actual_performance: "Number 1-10 - how well selected model performed",
  selection_accuracy_score: "Number - accuracy of selection algorithm",
  
  timestamp: "Date",
  selection_time: "Number - milliseconds to make selection"
}
```

### 7. Criticism Responses Collection
```javascript
// criticism_responses
{
  _id: ObjectId,
  thread_id: "ObjectId",
  session_id: "ObjectId",
  original_response_id: "ObjectId - response that was criticized",
  criticism_evaluation_ids: ["Array of ObjectIds - criticisms being addressed"],
  responding_model: "String - model responding to criticism",
  iteration_number: "Number",
  
  // Response to criticism
  acknowledgment: "String - what criticisms model accepts",
  disagreement: "String - what criticisms model disputes",
  clarifications: "String - explanations of original intent",
  
  // Improvements made
  specific_improvements: [{
    criticism_point: "String",
    improvement_made: "String",
    justification: "String"
  }],
  
  // Enhanced response
  revised_answer: "String - improved version of original response",
  explanation_of_changes: "String - what was changed and why",
  confidence_in_revision: "Number 1-10",
  
  // Defensive elements
  rebuttal_points: "String - defense of original approach",
  alternative_interpretations: "String - different ways to understand prompt",
  
  // Processing details
  criticism_processing_time: "Number - time to analyze criticism",
  response_generation_time: "Number - time to generate improved response",
  total_tokens_used: "Number",
  cost: "Number",
  
  // Quality assessment
  improvement_score: "Number 1-10 - how much better than original",
  addresses_criticism: "Boolean - does it address the main points",
  maintains_strengths: "Boolean - keeps good parts of original",
  
  timestamp: "Date"
}
```

### 8. Orchestration Logs Collection
```javascript
// orchestration_logs
{
  _id: ObjectId,
  session_id: "ObjectId",
  thread_id: "ObjectId",
  log_level: "String - info|warning|error|debug",
  component: "String - selector|evaluator|orchestrator|api",
  event_type: "String - model_selected|response_generated|evaluation_completed|error_occurred",
  
  // Event details
  message: "String - human readable description",
  details: "Object - structured event data",
  error_stack: "String - if error occurred",
  
  // Context
  iteration_number: "Number",
  model_involved: "String",
  processing_time: "Number - milliseconds",
  
  // System state
  memory_usage: "Number - MB",
  active_requests: "Number",
  queue_length: "Number",
  
  timestamp: "Date"
}
```

### 9. Algorithm Performance Metrics Collection
```javascript
// algorithm_metrics
{
  _id: ObjectId,
  metric_date: "Date",
  time_period: "String - hourly|daily|weekly|monthly",
  
  // Session statistics
  total_sessions: "Number",
  successful_sessions: "Number",
  failed_sessions: "Number",
  average_session_duration: "Number - minutes",
  
  // Thread statistics
  total_threads: "Number",
  average_iterations_per_thread: "Number",
  max_iterations_reached_count: "Number",
  early_termination_count: "Number",
  
  // Model usage and performance
  model_usage_stats: {
    "gpt4": {
      times_selected: "Number",
      success_rate: "Number",
      average_score: "Number",
      total_cost: "Number"
    },
    "grok": { /* same structure */ },
    "qwen": { /* same structure */ },
    "claude": { /* same structure */ },
    "llama": { /* same structure */ },
    "mistral": { /* same structure */ }
  },
  
  // Domain performance
  domain_performance: {
    "coding": {
      total_requests: "Number",
      average_satisfaction: "Number",
      preferred_models: ["Array of top performing models"],
      average_iterations: "Number"
    },
    "creative": { /* same structure */ },
    "math": { /* same structure */ },
    "translation": { /* same structure */ },
    "general": { /* same structure */ }
  },
  
  // System efficiency
  cost_efficiency: {
    total_cost: "Number",
    cost_per_session: "Number",
    cost_per_successful_response: "Number",
    most_cost_effective_model: "String"
  },
  
  // Quality metrics
  quality_metrics: {
    average_final_score: "Number",
    user_satisfaction_rate: "Number",
    criticism_improvement_rate: "Number",
    selection_accuracy: "Number"
  },
  
  // System health
  system_health: {
    average_response_time: "Number",
    error_rate: "Number",
    uptime_percentage: "Number",
    peak_concurrent_sessions: "Number"
  }
}
```

## Additional Indexes for Performance

```javascript
// Recommended indexes for optimal query performance

// user_sessions
db.user_sessions.createIndex({ "user_id": 1, "session_start": -1 })
db.user_sessions.createIndex({ "status": 1, "created_at": -1 })

// conversation_threads  
db.conversation_threads.createIndex({ "session_id": 1, "created_at": -1 })
db.conversation_threads.createIndex({ "domain": 1, "thread_status": 1 })
db.conversation_threads.createIndex({ "best_model_id": 1, "final_quality_score": -1 })

// model_responses
db.model_responses.createIndex({ "thread_id": 1, "iteration_number": 1 })
db.model_responses.createIndex({ "model_name": 1, "timestamp": -1 })
db.model_responses.createIndex({ "is_selected_best": 1, "selection_score": -1 })

// model_evaluations
db.model_evaluations.createIndex({ "thread_id": 1, "iteration_number": 1 })
db.model_evaluations.createIndex({ "evaluator_model": 1, "overall_score": -1 })
db.model_evaluations.createIndex({ "evaluated_response_id": 1 })

// model_selection_history
db.model_selection_history.createIndex({ "thread_id": 1, "iteration_number": 1 })
db.model_selection_history.createIndex({ "selected_model": 1, "selection_success": 1 })

// criticism_responses
db.criticism_responses.createIndex({ "thread_id": 1, "iteration_number": 1 })
db.criticism_responses.createIndex({ "original_response_id": 1 })
```

## Schema Features Summary

### ✅ **Supports Your System Requirements:**
1. **Multi-AI Orchestration**: Tracks model selection, responses, and evaluations
2. **Iterative Improvement**: Supports up to 10 rounds of criticism and refinement
3. **Model Specialization**: Tracks model strengths and domain expertise
4. **Cost Management**: Monitors API costs across all interactions
5. **Quality Assessment**: Comprehensive evaluation and scoring system
6. **User Experience**: Only shows final best responses to users
7. **Performance Analytics**: Detailed metrics for system optimization

### 🔧 **Key Capabilities:**
- Real-time orchestration tracking
- Model performance comparison
- Cost optimization analytics
- Quality improvement measurement
- User satisfaction monitoring
- System health and performance metrics
- Detailed audit trails for all interactions

This schema provides the foundation for your sophisticated multi-AI orchestration system with full support for iterative evaluation, criticism handling, and performance optimization.
