const db = require('../config/firestore');

class AIModelManager {
  
  // Collections for different data types
  static collections = {
    prompts: 'ai_prompts',
    responses: 'model_responses',
    criticism: 'model_criticism',
    suggestions: 'model_suggestions',
    sessions: 'ai_sessions',
    analytics: 'model_analytics'
  };
  
  // Supported models from your config
  static models = {
    GLM45: 'z-ai/glm-4.5-air:free',
    GPTOSS: 'openai/gpt-oss-20b:free',
    LLAMA4: 'meta-llama/llama-4-maverick:free',
    KIMI: 'moonshotai/kimi-dev-72b:free',
    QWEN3: 'qwen/Qwen3-coder:free',
    FALCON: 'tngtech/deepseek-r1t2-chimera:free'
  };

  // 1. Store User Prompt (from frontend)
  static async storePrompt(promptData) {
    try {
      const prompt = {
        content: promptData.content,
        userId: promptData.userId || 'anonymous',
        sessionId: promptData.sessionId,
        timestamp: new Date().toISOString(),
        source: 'frontend',
        metadata: {
          userAgent: promptData.userAgent || 'unknown',
          ip: promptData.ip || 'unknown',
          promptLength: promptData.content ? promptData.content.length : 0,
          language: promptData.language || 'en'
        }
      };

      const docRef = await db.collection(this.collections.prompts).add(prompt);
      console.log(`✅ Prompt stored in cloud: ${docRef.id}`);
      
      return { id: docRef.id, ...prompt };
    } catch (error) {
      console.error('❌ Error storing prompt:', error);
      throw new Error(`Failed to store prompt: ${error.message}`);
    }
  }

  // 2. Store Model Response
  static async storeModelResponse(responseData) {
    try {
      const response = {
        promptId: responseData.promptId,
        sessionId: responseData.sessionId,
        modelName: responseData.modelName,
        modelId: this.models[responseData.modelName] || responseData.modelName,
        response: responseData.response,
        timestamp: new Date().toISOString(),
        metadata: {
          responseTime: responseData.responseTime,
          tokenCount: responseData.tokenCount,
          temperature: responseData.temperature,
          maxTokens: responseData.maxTokens,
          cost: responseData.cost || 0
        },
        quality: {
          coherence: null,
          relevance: null,
          accuracy: null,
          rating: null
        }
      };

      const docRef = await db.collection(this.collections.responses).add(response);
      console.log(`✅ Model response stored: ${responseData.modelName} - ${docRef.id}`);
      
      return { id: docRef.id, ...response };
    } catch (error) {
      console.error('❌ Error storing model response:', error);
      throw new Error(`Failed to store model response: ${error.message}`);
    }
  }

  // 3. Store Model Criticism
  static async storeModelCriticism(criticismData) {
    try {
      const criticism = {
        responseId: criticismData.responseId,
        promptId: criticismData.promptId,
        sessionId: criticismData.sessionId,
        modelName: criticismData.modelName,
        criticismType: criticismData.type, // 'accuracy', 'relevance', 'coherence', 'safety'
        criticismText: criticismData.criticism,
        rating: criticismData.rating, // 1-10 scale
        reviewer: criticismData.reviewer || 'system',
        timestamp: new Date().toISOString(),
        metadata: {
          criticalPoints: criticismData.criticalPoints || [],
          improvementSuggestions: criticismData.improvements || [],
          severity: criticismData.severity || 'medium'
        }
      };

      const docRef = await db.collection(this.collections.criticism).add(criticism);
      console.log(`✅ Model criticism stored: ${criticismData.modelName} - ${docRef.id}`);
      
      return { id: docRef.id, ...criticism };
    } catch (error) {
      console.error('❌ Error storing criticism:', error);
      throw new Error(`Failed to store criticism: ${error.message}`);
    }
  }

  // 4. Store Model Suggestions
  static async storeModelSuggestion(suggestionData) {
    try {
      const suggestion = {
        responseId: suggestionData.responseId,
        promptId: suggestionData.promptId,
        sessionId: suggestionData.sessionId,
        modelName: suggestionData.modelName,
        suggestionType: suggestionData.type, // 'improvement', 'alternative', 'optimization'
        suggestion: suggestionData.suggestion,
        priority: suggestionData.priority || 'medium', // low, medium, high
        implementation: suggestionData.implementation || 'pending',
        timestamp: new Date().toISOString(),
        metadata: {
          expectedImprovement: suggestionData.expectedImprovement,
          effort: suggestionData.effort, // low, medium, high
          impact: suggestionData.impact, // low, medium, high
          tags: suggestionData.tags || []
        }
      };

      const docRef = await db.collection(this.collections.suggestions).add(suggestion);
      console.log(`✅ Model suggestion stored: ${suggestionData.modelName} - ${docRef.id}`);
      
      return { id: docRef.id, ...suggestion };
    } catch (error) {
      console.error('❌ Error storing suggestion:', error);
      throw new Error(`Failed to store suggestion: ${error.message}`);
    }
  }

  // 5. Get All Responses for 6 Models by Session
  static async getSessionModelResponses(sessionId) {
    try {
      const snapshot = await db.collection(this.collections.responses)
        .where('sessionId', '==', sessionId)
        .orderBy('timestamp', 'desc')
        .get();

      const responses = [];
      snapshot.forEach(doc => {
        responses.push({ id: doc.id, ...doc.data() });
      });

      // Group by model
      const modelResponses = {};
      responses.forEach(response => {
        if (!modelResponses[response.modelName]) {
          modelResponses[response.modelName] = [];
        }
        modelResponses[response.modelName].push(response);
      });

      console.log(`📊 Retrieved responses for ${Object.keys(modelResponses).length} models in session ${sessionId}`);
      return modelResponses;
    } catch (error) {
      console.error('❌ Error retrieving session responses:', error);
      throw new Error(`Failed to retrieve session responses: ${error.message}`);
    }
  }

  // 6. Compare All 6 Models Performance
  static async compareModelsPerformance(promptId) {
    try {
      // Get all responses for this prompt
      const responsesSnapshot = await db.collection(this.collections.responses)
        .where('promptId', '==', promptId)
        .get();

      // Get criticism for these responses
      const criticismSnapshot = await db.collection(this.collections.criticism)
        .where('promptId', '==', promptId)
        .get();

      const responses = [];
      const criticisms = [];

      responsesSnapshot.forEach(doc => responses.push({ id: doc.id, ...doc.data() }));
      criticismSnapshot.forEach(doc => criticisms.push({ id: doc.id, ...doc.data() }));

      // Combine data
      const modelComparison = {};
      responses.forEach(response => {
        const modelCriticisms = criticisms.filter(c => c.responseId === response.id);
        const avgRating = modelCriticisms.length > 0 
          ? modelCriticisms.reduce((sum, c) => sum + c.rating, 0) / modelCriticisms.length 
          : 0;

        modelComparison[response.modelName] = {
          response: response,
          criticisms: modelCriticisms,
          averageRating: avgRating,
          responseTime: response.metadata.responseTime,
          tokenCount: response.metadata.tokenCount
        };
      });

      console.log(`📈 Model comparison completed for prompt ${promptId}`);
      return modelComparison;
    } catch (error) {
      console.error('❌ Error comparing models:', error);
      throw new Error(`Failed to compare models: ${error.message}`);
    }
  }

  // 7. Store Complete AI Session
  static async storeAISession(sessionData) {
    try {
      const session = {
        sessionId: sessionData.sessionId,
        userId: sessionData.userId,
        startTime: sessionData.startTime || new Date().toISOString(),
        endTime: sessionData.endTime,
        totalPrompts: sessionData.totalPrompts || 0,
        modelsUsed: sessionData.modelsUsed || [],
        status: sessionData.status || 'active', // active, completed, failed
        metadata: {
          userAgent: sessionData.userAgent,
          ip: sessionData.ip,
          totalTokens: sessionData.totalTokens || 0,
          totalCost: sessionData.totalCost || 0
        }
      };

      const docRef = await db.collection(this.collections.sessions).add(session);
      console.log(`✅ AI session stored: ${sessionData.sessionId} - ${docRef.id}`);
      
      return { id: docRef.id, ...session };
    } catch (error) {
      console.error('❌ Error storing session:', error);
      throw new Error(`Failed to store session: ${error.message}`);
    }
  }

  // 8. Get Analytics for All Models
  static async getModelAnalytics(timeRange = '7d') {
    try {
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - parseInt(timeRange));

      const snapshot = await db.collection(this.collections.responses)
        .where('timestamp', '>=', cutoffDate.toISOString())
        .get();

      const analytics = {};
      
      snapshot.forEach(doc => {
        const data = doc.data();
        const model = data.modelName;
        
        if (!analytics[model]) {
          analytics[model] = {
            totalResponses: 0,
            avgResponseTime: 0,
            totalTokens: 0,
            avgRating: 0,
            responseTimeSum: 0,
            ratingSum: 0,
            ratingCount: 0
          };
        }
        
        analytics[model].totalResponses++;
        analytics[model].responseTimeSum += data.metadata.responseTime || 0;
        analytics[model].totalTokens += data.metadata.tokenCount || 0;
        
        if (data.quality.rating) {
          analytics[model].ratingSum += data.quality.rating;
          analytics[model].ratingCount++;
        }
      });

      // Calculate averages
      Object.keys(analytics).forEach(model => {
        const data = analytics[model];
        data.avgResponseTime = data.responseTimeSum / data.totalResponses;
        data.avgRating = data.ratingCount > 0 ? data.ratingSum / data.ratingCount : 0;
        
        delete data.responseTimeSum;
        delete data.ratingSum;
        delete data.ratingCount;
      });

      console.log(`📊 Analytics retrieved for ${Object.keys(analytics).length} models`);
      return analytics;
    } catch (error) {
      console.error('❌ Error retrieving analytics:', error);
      throw new Error(`Failed to retrieve analytics: ${error.message}`);
    }
  }
}

module.exports = AIModelManager;