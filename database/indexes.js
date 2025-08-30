// MongoDB Index Definitions for OrchestrateX
// Optimized indexes for query performance and data integrity

// Function to create all required indexes
function createOrchestrateXIndexes(db) {
    print("🔍 Creating OrchestrateX Database Indexes...");
    
    // ===========================================
    // 1. USER SESSIONS COLLECTION INDEXES
    // ===========================================
    print("📊 Creating user_sessions indexes...");
    
    // Primary indexes
    db.user_sessions.createIndex(
        { "user_id": 1, "session_start": -1 }, 
        { 
            name: "user_sessions_compound",
            background: true 
        }
    );
    
    db.user_sessions.createIndex(
        { "status": 1, "created_at": -1 }, 
        { 
            name: "user_sessions_status_time",
            background: true 
        }
    );
    
    // Performance indexes
    db.user_sessions.createIndex(
        { "session_start": -1 }, 
        { 
            name: "user_sessions_start_time",
            background: true 
        }
    );
    
    db.user_sessions.createIndex(
        { "total_cost": -1 }, 
        { 
            name: "user_sessions_cost",
            background: true 
        }
    );

    // ===========================================
    // 2. CONVERSATION THREADS COLLECTION INDEXES
    // ===========================================
    print("💬 Creating conversation_threads indexes...");
    
    // Primary lookup indexes
    db.conversation_threads.createIndex(
        { "session_id": 1, "created_at": -1 }, 
        { 
            name: "threads_session_time",
            background: true 
        }
    );
    
    db.conversation_threads.createIndex(
        { "domain": 1, "thread_status": 1 }, 
        { 
            name: "threads_domain_status",
            background: true 
        }
    );
    
    db.conversation_threads.createIndex(
        { "best_model_id": 1, "final_quality_score": -1 }, 
        { 
            name: "threads_best_model_quality",
            background: true 
        }
    );
    
    // Performance analytics indexes
    db.conversation_threads.createIndex(
        { "complexity_level": 1, "total_cost": -1 }, 
        { 
            name: "threads_complexity_cost",
            background: true 
        }
    );
    
    db.conversation_threads.createIndex(
        { "current_iteration": 1, "max_iterations_reached": 1 }, 
        { 
            name: "threads_iteration_tracking",
            background: true 
        }
    );

    // ===========================================
    // 3. AI MODEL PROFILES COLLECTION INDEXES
    // ===========================================
    print("🤖 Creating ai_model_profiles indexes...");
    
    // Primary lookup indexes
    db.ai_model_profiles.createIndex(
        { "model_name": 1 }, 
        { 
            unique: true,
            name: "model_profiles_name_unique",
            background: true 
        }
    );
    
    db.ai_model_profiles.createIndex(
        { "provider": 1, "is_active": 1 }, 
        { 
            name: "model_profiles_provider_active",
            background: true 
        }
    );
    
    db.ai_model_profiles.createIndex(
        { "specialties": 1, "is_available": 1 }, 
        { 
            name: "model_profiles_specialties_available",
            background: true 
        }
    );
    
    // Performance tracking indexes
    db.ai_model_profiles.createIndex(
        { "performance_metrics.average_quality_rating": -1 }, 
        { 
            name: "model_profiles_quality_rating",
            background: true 
        }
    );
    
    db.ai_model_profiles.createIndex(
        { "cost_per_input_token": 1, "cost_per_output_token": 1 }, 
        { 
            name: "model_profiles_cost_efficiency",
            background: true 
        }
    );

    // ===========================================
    // 4. MODEL RESPONSES COLLECTION INDEXES
    // ===========================================
    print("📝 Creating model_responses indexes...");
    
    // Primary lookup indexes
    db.model_responses.createIndex(
        { "thread_id": 1, "iteration_number": 1 }, 
        { 
            name: "responses_thread_iteration",
            background: true 
        }
    );
    
    db.model_responses.createIndex(
        { "session_id": 1, "timestamp": -1 }, 
        { 
            name: "responses_session_time",
            background: true 
        }
    );
    
    db.model_responses.createIndex(
        { "model_name": 1, "timestamp": -1 }, 
        { 
            name: "responses_model_time",
            background: true 
        }
    );
    
    // Quality and selection indexes
    db.model_responses.createIndex(
        { "is_selected_best": 1, "selection_score": -1 }, 
        { 
            name: "responses_best_selection",
            background: true 
        }
    );
    
    db.model_responses.createIndex(
        { "role": 1, "response_type": 1 }, 
        { 
            name: "responses_role_type",
            background: true 
        }
    );
    
    // Performance indexes
    db.model_responses.createIndex(
        { "response_time": 1, "cost": 1 }, 
        { 
            name: "responses_performance_cost",
            background: true 
        }
    );

    // ===========================================
    // 5. MODEL EVALUATIONS COLLECTION INDEXES
    // ===========================================
    print("🎯 Creating model_evaluations indexes...");
    
    // Primary lookup indexes
    db.model_evaluations.createIndex(
        { "thread_id": 1, "iteration_number": 1 }, 
        { 
            name: "evaluations_thread_iteration",
            background: true 
        }
    );
    
    db.model_evaluations.createIndex(
        { "evaluated_response_id": 1 }, 
        { 
            name: "evaluations_response_ref",
            background: true 
        }
    );
    
    db.model_evaluations.createIndex(
        { "evaluator_model": 1, "overall_score": -1 }, 
        { 
            name: "evaluations_evaluator_score",
            background: true 
        }
    );
    
    // Quality analysis indexes
    db.model_evaluations.createIndex(
        { "evaluation_criteria.accuracy": -1, "evaluation_criteria.relevance": -1 }, 
        { 
            name: "evaluations_criteria_compound",
            background: true 
        }
    );

    // ===========================================
    // 6. MODEL SELECTION HISTORY COLLECTION INDEXES
    // ===========================================
    print("📈 Creating model_selection_history indexes...");
    
    db.model_selection_history.createIndex(
        { "thread_id": 1, "iteration_number": 1 }, 
        { 
            name: "selection_history_thread_iteration",
            background: true 
        }
    );
    
    db.model_selection_history.createIndex(
        { "selected_model": 1, "selection_success": 1 }, 
        { 
            name: "selection_history_model_success",
            background: true 
        }
    );
    
    db.model_selection_history.createIndex(
        { "algorithm_version": 1, "timestamp": -1 }, 
        { 
            name: "selection_history_algorithm_time",
            background: true 
        }
    );

    // ===========================================
    // 7. CRITICISM RESPONSES COLLECTION INDEXES
    // ===========================================
    print("🔍 Creating criticism_responses indexes...");
    
    db.criticism_responses.createIndex(
        { "thread_id": 1, "iteration_number": 1 }, 
        { 
            name: "criticism_thread_iteration",
            background: true 
        }
    );
    
    db.criticism_responses.createIndex(
        { "original_response_id": 1 }, 
        { 
            name: "criticism_original_response",
            background: true 
        }
    );
    
    db.criticism_responses.createIndex(
        { "responding_model": 1, "improvement_quality": -1 }, 
        { 
            name: "criticism_model_quality",
            background: true 
        }
    );

    // ===========================================
    // 8. ORCHESTRATION LOGS COLLECTION INDEXES
    // ===========================================
    print("📋 Creating orchestration_logs indexes...");
    
    db.orchestration_logs.createIndex(
        { "session_id": 1, "timestamp": -1 }, 
        { 
            name: "logs_session_time",
            background: true 
        }
    );
    
    db.orchestration_logs.createIndex(
        { "thread_id": 1, "timestamp": -1 }, 
        { 
            name: "logs_thread_time",
            background: true 
        }
    );
    
    db.orchestration_logs.createIndex(
        { "log_level": 1, "component": 1 }, 
        { 
            name: "logs_level_component",
            background: true 
        }
    );
    
    db.orchestration_logs.createIndex(
        { "event_type": 1, "timestamp": -1 }, 
        { 
            name: "logs_event_time",
            background: true 
        }
    );

    // ===========================================
    // 9. ALGORITHM METRICS COLLECTION INDEXES
    // ===========================================
    print("📊 Creating algorithm_metrics indexes...");
    
    db.algorithm_metrics.createIndex(
        { "metric_date": -1, "time_period": 1 }, 
        { 
            name: "metrics_date_period",
            background: true 
        }
    );
    
    db.algorithm_metrics.createIndex(
        { "time_period": 1, "total_sessions": -1 }, 
        { 
            name: "metrics_period_sessions",
            background: true 
        }
    );

    // ===========================================
    // TEXT SEARCH INDEXES
    // ===========================================
    print("🔍 Creating text search indexes...");
    
    // Full-text search on conversation threads
    db.conversation_threads.createIndex(
        { 
            "original_prompt": "text", 
            "processed_prompt": "text",
            "final_response": "text"
        },
        { 
            name: "threads_text_search",
            background: true,
            default_language: "english"
        }
    );
    
    // Full-text search on responses
    db.model_responses.createIndex(
        { 
            "response_text": "text",
            "prompt_sent": "text"
        },
        { 
            name: "responses_text_search",
            background: true,
            default_language: "english"
        }
    );

    // ===========================================
    // COMPOUND INDEXES FOR COMPLEX QUERIES
    // ===========================================
    print("🔗 Creating compound indexes for complex queries...");
    
    // Session analysis compound index
    db.user_sessions.createIndex(
        { 
            "user_id": 1, 
            "status": 1, 
            "session_start": -1,
            "total_cost": -1
        },
        { 
            name: "sessions_analysis_compound",
            background: true 
        }
    );
    
    // Thread performance compound index
    db.conversation_threads.createIndex(
        { 
            "domain": 1,
            "complexity_level": 1,
            "final_quality_score": -1,
            "total_cost": 1
        },
        { 
            name: "threads_performance_compound",
            background: true 
        }
    );
    
    // Response evaluation compound index
    db.model_responses.createIndex(
        { 
            "model_name": 1,
            "role": 1,
            "is_selected_best": 1,
            "selection_score": -1,
            "timestamp": -1
        },
        { 
            name: "responses_evaluation_compound",
            background: true 
        }
    );

    print("✅ All OrchestrateX indexes created successfully!");
    
    // Print index statistics
    print("\n📈 Index Statistics:");
    print("user_sessions indexes: " + db.user_sessions.getIndexes().length);
    print("conversation_threads indexes: " + db.conversation_threads.getIndexes().length);
    print("ai_model_profiles indexes: " + db.ai_model_profiles.getIndexes().length);
    print("model_responses indexes: " + db.model_responses.getIndexes().length);
    print("model_evaluations indexes: " + db.model_evaluations.getIndexes().length);
    print("model_selection_history indexes: " + db.model_selection_history.getIndexes().length);
    print("criticism_responses indexes: " + db.criticism_responses.getIndexes().length);
    print("orchestration_logs indexes: " + db.orchestration_logs.getIndexes().length);
    print("algorithm_metrics indexes: " + db.algorithm_metrics.getIndexes().length);
}

// Function to drop all custom indexes (for maintenance)
function dropOrchestrateXIndexes(db) {
    print("🗑️ Dropping OrchestrateX custom indexes...");
    
    const collections = [
        'user_sessions',
        'conversation_threads', 
        'ai_model_profiles',
        'model_responses',
        'model_evaluations',
        'model_selection_history',
        'criticism_responses',
        'orchestration_logs',
        'algorithm_metrics'
    ];
    
    collections.forEach(function(collectionName) {
        try {
            const indexes = db[collectionName].getIndexes();
            indexes.forEach(function(index) {
                // Don't drop the default _id index
                if (index.name !== "_id_") {
                    db[collectionName].dropIndex(index.name);
                    print("Dropped index: " + index.name + " from " + collectionName);
                }
            });
        } catch (error) {
            print("Error dropping indexes from " + collectionName + ": " + error.message);
        }
    });
    
    print("✅ Custom indexes dropped successfully!");
}

// Function to analyze index usage
function analyzeIndexUsage(db) {
    print("📊 Analyzing index usage statistics...");
    
    const collections = [
        'user_sessions',
        'conversation_threads', 
        'ai_model_profiles',
        'model_responses',
        'model_evaluations'
    ];
    
    collections.forEach(function(collectionName) {
        print("\n--- " + collectionName + " ---");
        try {
            const stats = db[collectionName].aggregate([
                { $indexStats: {} }
            ]).toArray();
            
            stats.forEach(function(indexStat) {
                print("Index: " + indexStat.name);
                print("  Operations: " + indexStat.accesses.ops);
                print("  Since: " + indexStat.accesses.since);
            });
        } catch (error) {
            print("Error getting stats for " + collectionName + ": " + error.message);
        }
    });
}

// Export functions for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createOrchestrateXIndexes,
        dropOrchestrateXIndexes,
        analyzeIndexUsage
    };
}
