const db = require('../config/firestore');

class AIModelManager {
  
  // Collections for different data types
  static collections = {
    prompts: 'ai_prompts',
    userPrompts: 'user_prompts', // Added user_prompts collection
    responses: 'model_responses',
    criticism: 'model_critiques', // Updated to use the correct collection
    suggestions: 'model_suggestions',
    sessions: 'ai_sessions',
    analytics: 'model_analytics'
  };

  // IP-based storage limits
  static MAX_ENTRIES_PER_IP = 5;
  
  // Supported models from your config
  static models = {
    GLM45: 'z-ai/glm-4.5-air:free',
    GPTOSS: 'openai/gpt-oss-20b:free',
    LLAMA4: 'meta-llama/llama-4-maverick:free',
    KIMI: 'moonshotai/kimi-dev-72b:free',
    QWEN3: 'qwen/Qwen3-coder:free',
    FALCON: 'tngtech/deepseek-r1t2-chimera:free'
  };

  // Helper method to maintain IP-based entry limits for model_critiques format
  static async maintainIPLimit(collectionName, ipAddress) {
    try {
      let query;
      
      // For model_critiques, check if documents have metadata.ip or are legacy "no-ip"
      if (collectionName === this.collections.criticism) {
        // Get documents by metadata.ip if exists, otherwise check for legacy documents
        const snapshot = await db.collection(collectionName).get();
        
        const docs = [];
        snapshot.forEach(doc => {
          const data = doc.data();
          const docIP = data.metadata?.ip || data.ip || 'no-ip';
          
          if (docIP === ipAddress || (ipAddress === 'no-ip' && docIP === 'no-ip')) {
            docs.push({ 
              id: doc.id, 
              data: data,
              timestamp: data.timestamp
            });
          }
        });

        console.log(`📊 Found ${docs.length} existing entries for IP: ${ipAddress} in ${collectionName}`);

        // If we have MAX_ENTRIES_PER_IP or more, delete the oldest ones
        if (docs.length >= this.MAX_ENTRIES_PER_IP) {
          // Sort by timestamp manually (oldest first)
          docs.sort((a, b) => {
            const timeA = new Date(a.timestamp?.toDate ? a.timestamp.toDate() : a.timestamp);
            const timeB = new Date(b.timestamp?.toDate ? b.timestamp.toDate() : b.timestamp);
            return timeA - timeB;
          });
          
          // Calculate how many to delete (keep only MAX_ENTRIES_PER_IP - 1 to make room for new one)
          const deleteCount = docs.length - this.MAX_ENTRIES_PER_IP + 1;
          const docsToDelete = docs.slice(0, deleteCount);
          
          console.log(`🗑️  Will delete ${deleteCount} oldest entries to maintain limit of ${this.MAX_ENTRIES_PER_IP}`);
          
          const batch = db.batch();
          docsToDelete.forEach(doc => {
            batch.delete(db.collection(collectionName).doc(doc.id));
          });
          
          await batch.commit();
          console.log(`✅ Deleted ${deleteCount} old entries from ${collectionName} for IP: ${ipAddress}`);
        } else {
          console.log(`✅ IP ${ipAddress} has ${docs.length} entries, within limit of ${this.MAX_ENTRIES_PER_IP}`);
        }
      } else {
        // For other collections, use the standard metadata.ip approach
        const snapshot = await db.collection(collectionName)
          .where('metadata.ip', '==', ipAddress)
          .get();

        const docs = [];
        snapshot.forEach(doc => docs.push({ 
          id: doc.id, 
          data: doc.data(),
          timestamp: doc.data().timestamp
        }));

        console.log(`📊 Found ${docs.length} existing entries for IP: ${ipAddress} in ${collectionName}`);

        // If we have MAX_ENTRIES_PER_IP or more, delete the oldest ones
        if (docs.length >= this.MAX_ENTRIES_PER_IP) {
          // Sort by timestamp manually (oldest first)
          docs.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
          
          // Calculate how many to delete (keep only MAX_ENTRIES_PER_IP - 1 to make room for new one)
          const deleteCount = docs.length - this.MAX_ENTRIES_PER_IP + 1;
          const docsToDelete = docs.slice(0, deleteCount);
          
          console.log(`🗑️  Will delete ${deleteCount} oldest entries to maintain limit of ${this.MAX_ENTRIES_PER_IP}`);
          
          const batch = db.batch();
          docsToDelete.forEach(doc => {
            batch.delete(db.collection(collectionName).doc(doc.id));
          });
          
          await batch.commit();
          console.log(`✅ Deleted ${deleteCount} old entries from ${collectionName} for IP: ${ipAddress}`);
        } else {
          console.log(`✅ IP ${ipAddress} has ${docs.length} entries, within limit of ${this.MAX_ENTRIES_PER_IP}`);
        }
      }
    } catch (error) {
      console.warn(`⚠️  Could not maintain IP limit for ${collectionName}: ${error.message}`);
      // If IP limit check fails, we still want to store the new entry
      // but warn that the limit might not be enforced
    }
  }

  // 1. Store User Prompt (from frontend)
  static async storePrompt(promptData) {
    try {
      const userIP = promptData.ip || 'unknown';
      
      // Maintain IP limit before adding new entry
      await this.maintainIPLimit(this.collections.prompts, userIP);
      
      const prompt = {
        content: promptData.content,
        userId: promptData.userId || 'anonymous',
        sessionId: promptData.sessionId,
        timestamp: new Date().toISOString(),
        source: 'frontend',
        metadata: {
          userAgent: promptData.userAgent || 'unknown',
          ip: userIP,
          promptLength: promptData.content ? promptData.content.length : 0,
          language: promptData.language || 'en'
        }
      };

      const docRef = await db.collection(this.collections.prompts).add(prompt);
      console.log(`✅ Prompt stored in cloud: ${docRef.id} (IP: ${userIP})`);
      
      return { id: docRef.id, ...prompt };
    } catch (error) {
      console.error('❌ Error storing prompt:', error);
      throw new Error(`Failed to store prompt: ${error.message}`);
    }
  }

  // 1.5. Store User Prompt (user_prompts collection with IP limit)
  static async storeUserPrompt(userPromptData) {
    try {
      const userIP = userPromptData.ip || 'unknown';
      
      // Maintain IP limit before adding new entry
      await this.maintainIPLimit(this.collections.userPrompts, userIP);
      
      const userPrompt = {
        user_message: userPromptData.message || userPromptData.content,
        session_id: userPromptData.sessionId,
        hash: userPromptData.hash || `hash_${userPromptData.sessionId}`,
        source: userPromptData.source || 'ui_interface',
        status: userPromptData.status || 'processing',
        user: userPromptData.user || 'anonymous',
        timestamp: new Date(),
        metadata: {
          ip: userIP,
          messageLength: userPromptData.message ? userPromptData.message.length : 0,
          language: userPromptData.language || 'en'
        }
      };

      const docRef = await db.collection(this.collections.userPrompts).add(userPrompt);
      console.log(`✅ User prompt stored: ${docRef.id} (IP: ${userIP})`);
      
      return { id: docRef.id, ...userPrompt };
    } catch (error) {
      console.error('❌ Error storing user prompt:', error);
      throw new Error(`Failed to store user prompt: ${error.message}`);
    }
  }

  // 2. Store Model Response
  static async storeModelResponse(responseData) {
    try {
      const userIP = responseData.ip || 'unknown';
      
      // Maintain IP limit before adding new entry
      await this.maintainIPLimit(this.collections.responses, userIP);
      
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
          cost: responseData.cost || 0,
          ip: userIP
        },
        quality: {
          coherence: null,
          relevance: null,
          accuracy: null,
          rating: null
        }
      };

      const docRef = await db.collection(this.collections.responses).add(response);
      console.log(`✅ Model response stored: ${responseData.modelName} - ${docRef.id} (IP: ${userIP})`);
      
      return { id: docRef.id, ...response };
    } catch (error) {
      console.error('❌ Error storing model response:', error);
      throw new Error(`Failed to store model response: ${error.message}`);
    }
  }

  // 3. Store Model Criticism (critic_model → target_model format)
  static async storeModelCriticism(criticismData) {
    try {
      const userIP = criticismData.ip || 'unknown';
      
      // Get conversation history (last 5 entries) from prompts collection for this IP
      const conversationHistory = await this.getConversationHistory(userIP, 5);
      
      // Maintain IP limit before adding new entry - ONLY LAST 5 CRITIQUES PER IP
      await this.maintainIPLimit(this.collections.criticism, userIP);
      
      const criticism = {
        // Using model_critiques format: critic_model → target_model
        critic_model: criticismData.criticModel || criticismData.reviewer || 'system',
        target_model: criticismData.targetModel || criticismData.modelName,
        critique_text: `[${criticismData.criticModel || 'system'} critiques ${criticismData.targetModel || criticismData.modelName}]: ${criticismData.criticism}`,
        critique_score: criticismData.rating || 7, // 1-10 scale
        session_id: criticismData.sessionId,
        timestamp: new Date(),
        // Include full conversation context for better critique analysis
        conversationContext: {
          totalEntries: conversationHistory.length,
          conversationHistory: conversationHistory,
          contextNote: `Full conversation history from IP ${userIP} for better critique context`
        },
        metadata: {
          responseId: criticismData.responseId,
          promptId: criticismData.promptId,
          criticismType: criticismData.type || 'general', // 'accuracy', 'relevance', 'coherence', 'safety'
          criticalPoints: criticismData.criticalPoints || [],
          improvementSuggestions: criticismData.improvements || [],
          severity: criticismData.severity || 'medium',
          ip: userIP
        }
      };

      const docRef = await db.collection(this.collections.criticism).add(criticism);
      console.log(`✅ Model critique stored: ${criticism.critic_model} → ${criticism.target_model} - ${docRef.id} (IP: ${userIP}) [Last 5 only] [Context: ${conversationHistory.length} entries]`);
      
      return { id: docRef.id, ...criticism };
    } catch (error) {
      console.error('❌ Error storing critique:', error);
      throw new Error(`Failed to store critique: ${error.message}`);
    }
  }

  // Helper method to get conversation history for context
  static async getConversationHistory(ipAddress, limit = 5) {
    try {
      // Simple approach: Get all prompts for this IP, then filter and sort manually
      const snapshot = await db.collection(this.collections.prompts)
        .where('metadata.ip', '==', ipAddress)
        .get();

      const allPrompts = [];
      snapshot.forEach(doc => {
        const data = doc.data();
        allPrompts.push({
          content: data.content,
          timestamp: data.timestamp,
          sessionId: data.sessionId,
          userId: data.userId
        });
      });

      // Sort by timestamp manually (newest first)
      allPrompts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      
      // Take the most recent 'limit' entries
      const recentPrompts = allPrompts.slice(0, limit);
      
      // Return in chronological order (oldest first) for context
      return recentPrompts.reverse();
    } catch (error) {
      console.warn(`⚠️  Could not fetch conversation history for IP ${ipAddress}:`, error.message);
      return []; // Return empty array if can't fetch history
    }
  }

  // 4. Store Model Suggestions
  static async storeModelSuggestion(suggestionData) {
    try {
      const userIP = suggestionData.ip || 'unknown';
      
      // Maintain IP limit before adding new entry
      await this.maintainIPLimit(this.collections.suggestions, userIP);
      
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
          tags: suggestionData.tags || [],
          ip: userIP
        }
      };

      const docRef = await db.collection(this.collections.suggestions).add(suggestion);
      console.log(`✅ Model suggestion stored: ${suggestionData.modelName} - ${docRef.id} (IP: ${userIP})`);
      
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
      const userIP = sessionData.ip || 'unknown';
      
      // Maintain IP limit before adding new entry
      await this.maintainIPLimit(this.collections.sessions, userIP);
      
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
          ip: userIP,
          totalTokens: sessionData.totalTokens || 0,
          totalCost: sessionData.totalCost || 0
        }
      };

      const docRef = await db.collection(this.collections.sessions).add(session);
      console.log(`✅ AI session stored: ${sessionData.sessionId} - ${docRef.id} (IP: ${userIP})`);
      
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