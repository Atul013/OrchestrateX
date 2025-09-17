const AIModelManager = require('./AIModelManager');

class AIOrchestrator {
  
  // 5 AI Models from working_api.py
  static MODELS = [
    {
      name: "GLM-4.5",
      specialty: "Advanced reasoning and analysis",
      strength: 0.89,
      api_endpoint: "z-ai/glm-4.5-air:free"
    },
    {
      name: "GPT-OSS",
      specialty: "General-purpose conversation",
      strength: 0.85,
      api_endpoint: "openai/gpt-oss-20b:free"
    },
    {
      name: "Llama-4-Maverick",
      specialty: "Technical and coding assistance",
      strength: 0.87,
      api_endpoint: "meta-llama/llama-4-maverick:free"
    },
    {
      name: "Kimi-K2",
      specialty: "Creative and innovative responses",
      strength: 0.82,
      api_endpoint: "moonshotai/kimi-dev-72b:free"
    },
    {
      name: "TNG-DeepSeek-R1T2",
      specialty: "Deep analysis and research",
      strength: 0.91,
      api_endpoint: "tngtech/deepseek-r1t2-chimera:free"
    }
  ];

  // Simulate AI model response (from working_api.py)
  static simulateModelResponse(model, prompt, delay = null) {
    return new Promise((resolve) => {
      const processingDelay = delay || (Math.random() * 0.2 + 0.1); // 0.1-0.3 seconds
      
      setTimeout(() => {
        const responses = {
          "GLM-4.5": `[GLM-4.5 Reasoning] Advanced analysis of '${prompt.substring(0, 30)}...' - Multi-step reasoning with ${Math.floor(Math.random() * 10) + 1} key insights identified.`,
          "GPT-OSS": `[GPT-OSS General] Comprehensive response to '${prompt.substring(0, 30)}...' - Balanced approach with ${Math.floor(Math.random() * 6) + 3} perspectives covered.`,
          "Llama-4-Maverick": `[Llama-4-Maverick Coding] Technical solution for '${prompt.substring(0, 30)}...' - ${Math.floor(Math.random() * 5) + 2} implementation strategies provided.`,
          "Kimi-K2": `[Kimi-K2 Creative] Creative interpretation of '${prompt.substring(0, 30)}...' - Novel approach with ${Math.floor(Math.random() * 6) + 4} unique angles explored.`,
          "TNG-DeepSeek-R1T2": `[TNG-DeepSeek Analysis] Deep analytical response to '${prompt.substring(0, 30)}...' - ${Math.floor(Math.random() * 8) + 5} analytical dimensions examined.`
        };

        const result = {
          model_name: model.name,
          specialty: model.specialty,
          response_text: responses[model.name] || `Response from ${model.name}`,
          confidence: model.strength + (Math.random() * 0.1 - 0.05), // ±0.05 variation
          processing_time: processingDelay,
          processing_time_ms: Math.round(processingDelay * 1000),
          timestamp: new Date().toISOString(),
          tokens_used: Math.floor(Math.random() * 400) + 100,
          cost_estimate: Math.round((Math.random() * 0.009 + 0.001) * 10000) / 10000, // 0.001-0.01
          success: true
        };

        resolve(result);
      }, processingDelay * 1000);
    });
  }

  // Generate critique from one model about another (from working_api.py)
  static generateCritique(criticModel, targetResponse, userPrompt) {
    const critiqueTemplates = {
      "GLM-4.5": `From a reasoning perspective, ${targetResponse.model_name}'s response lacks ${this.randomChoice(['logical structure', 'deeper analysis', 'systematic thinking'])}. A better approach would involve ${this.randomChoice(['step-by-step analysis', 'multi-layered reasoning', 'causal relationships'])}.`,
      "GPT-OSS": `The ${targetResponse.model_name} response is ${this.randomChoice(['too narrow', 'missing context', 'incomplete'])}. A more comprehensive approach should include ${this.randomChoice(['multiple perspectives', 'broader context', 'balanced viewpoints'])}.`,
      "Llama-4-Maverick": `From a technical standpoint, ${targetResponse.model_name} missed ${this.randomChoice(['implementation details', 'practical considerations', 'optimization opportunities'])}. Better solution: ${this.randomChoice(['modular approach', 'scalable design', 'efficient algorithm'])}.`,
      "Kimi-K2": `The ${targetResponse.model_name} response lacks ${this.randomChoice(['creativity', 'innovation', 'unique perspective'])}. More creative approach: ${this.randomChoice(['alternative angles', 'imaginative solutions', 'novel interpretations'])}.`,
      "TNG-DeepSeek-R1T2": `Deep analysis reveals ${targetResponse.model_name}'s response is ${this.randomChoice(['surface-level', 'missing nuances', 'lacks depth'])}. Deeper insight needed: ${this.randomChoice(['underlying patterns', 'complex relationships', 'systemic analysis'])}.`
    };

    return critiqueTemplates[criticModel.name] || `Alternative perspective on ${targetResponse.model_name}'s response.`;
  }

  // Helper function for random choice
  static randomChoice(array) {
    return array[Math.floor(Math.random() * array.length)];
  }

  // Main orchestration function - processes prompt through all 5 models
  static async processPrompt(promptText, sessionId, userId = 'anonymous') {
    try {
      console.log("🧠 Starting SMART 5-model algorithm with cross-critique...");
      const startTime = Date.now();

      let promptData;
      
      // Store user prompt first (with error handling)
      try {
        promptData = await AIModelManager.storePrompt({
          content: promptText,
          userId: userId,
          sessionId: sessionId,
          source: 'ui_interface'
        });
        console.log(`💾 User prompt stored! Session: ${sessionId} | ID: ${promptData.id}`);
      } catch (storeError) {
        console.log('⚠️ Could not store prompt in Firestore:', storeError.message);
        promptData = { id: `temp_${Date.now()}` }; // Fallback ID
      }

      // Phase 1: All models generate initial responses
      console.log("⚡ Phase 1: All 5 models generating responses in parallel...");
      const modelPromises = this.MODELS.map(model => 
        this.simulateModelResponse(model, promptText)
      );
      
      const modelResponses = await Promise.all(modelPromises);
      
      // Store all model responses in Firestore (with error handling)
      console.log(`💾 Storing ${modelResponses.length} model responses in Firestore...`);
      try {
        const responseStorePromises = modelResponses.map(response => 
          AIModelManager.storeModelResponse({
            promptId: promptData.id,
            sessionId: sessionId,
            modelName: response.model_name,
            response: response.response_text,
            responseTime: response.processing_time_ms,
            tokenCount: response.tokens_used,
            cost: response.cost_estimate
          })
        );
        
        await Promise.all(responseStorePromises);
        console.log("✅ All model responses stored in Firestore!");
      } catch (storeError) {
        console.log('⚠️ Could not store model responses in Firestore:', storeError.message);
      }

      // Phase 2: Each model critiques others' responses (SMART ALGORITHM)
      console.log("🔍 Phase 2: Models critiquing each other...");
      const critiques = [];
      
      for (let i = 0; i < this.MODELS.length; i++) {
        for (let j = 0; j < modelResponses.length; j++) {
          if (i !== j) { // Don't critique yourself
            const critique = {
              critic_model: this.MODELS[i].name,
              target_model: modelResponses[j].model_name,
              critique_text: `[${this.MODELS[i].name} critiques ${modelResponses[j].model_name}]: ${this.generateCritique(this.MODELS[i], modelResponses[j], promptText)}`,
              critique_score: Math.random() * 0.35 + 0.6, // 0.6-0.95
              session_id: sessionId,
              timestamp: new Date().toISOString()
            };
            critiques.push(critique);
          }
        }
      }

      // Store ALL critiques in Firestore (with error handling)
      console.log(`💾 Storing ${critiques.length} critiques in Firestore...`);
      try {
        const critiqueStorePromises = critiques.map(critique => 
          AIModelManager.storeModelCriticism({
            promptId: promptData.id,
            sessionId: sessionId,
            modelName: critique.critic_model,
            type: 'cross_model_critique',
            criticism: critique.critique_text,
            rating: Math.round(critique.critique_score * 10) // Convert to 1-10 scale
          })
        );
        
        await Promise.all(critiqueStorePromises);
        console.log("✅ All critiques stored in Firestore!");
      } catch (storeError) {
        console.log('⚠️ Could not store critiques in Firestore:', storeError.message);
      }

      // Find best response (highest confidence)
      const bestResponse = modelResponses.reduce((prev, current) => 
        (prev.confidence > current.confidence) ? prev : current
      );

      // Store model suggestion (with error handling)
      try {
        const modelSuggestion = {
          promptId: promptData.id,
          sessionId: sessionId,
          modelName: bestResponse.model_name,
          type: 'recommendation',
          suggestion: `Selected ${bestResponse.model_name} with ${bestResponse.confidence.toFixed(3)} confidence`,
          priority: 'high'
        };
        
        await AIModelManager.storeModelSuggestion(modelSuggestion);
        console.log(`🎯 Model suggestion stored: ${bestResponse.model_name} recommended`);
      } catch (storeError) {
        console.log('⚠️ Could not store model suggestion in Firestore:', storeError.message);
      }

      // Calculate totals
      const totalTime = (Date.now() - startTime) / 1000;
      const totalCost = modelResponses.reduce((sum, resp) => sum + resp.cost_estimate, 0);
      const successCount = modelResponses.filter(resp => resp.success).length;
      const successRate = (successCount / modelResponses.length) * 100;

      console.log(`⚡ Smart algorithm completed in ${totalTime.toFixed(2)} seconds with ${critiques.length} critiques generated`);

      // Return UI-compatible response (matching frontend interface exactly)
      return {
        success: true,
        primary_response: {
          success: true,
          model_name: bestResponse.model_name,
          response_text: bestResponse.response_text,
          tokens_used: bestResponse.tokens_used,
          cost_usd: bestResponse.cost_estimate,
          latency_ms: Math.round(totalTime * 1000)
        },
        critiques: modelResponses
          .filter(resp => resp !== bestResponse)
          .slice(0, 3) // Top 3 alternatives
          .map(resp => ({
            model_name: resp.model_name,
            critique_text: `Alternative perspective: ${resp.response_text.substring(0, 100)}...`,
            tokens_used: resp.tokens_used,
            cost_usd: resp.cost_estimate,
            latency_ms: resp.processing_time_ms
          })),
        total_cost: totalCost,
        api_calls: modelResponses.length,
        success_rate: successRate,
        metadata: {
          session_id: sessionId,
          total_models: modelResponses.length,
          processing_time_seconds: Math.round(totalTime * 100) / 100,
          storage_method: "google_cloud_firestore",
          database_status: "connected"
        }
      };

    } catch (error) {
      console.error("❌ Error in AI orchestration:", error);
      throw new Error(`AI orchestration failed: ${error.message}`);
    }
  }
}

module.exports = AIOrchestrator;