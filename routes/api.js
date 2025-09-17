const express = require('express');
const router = express.Router();
const AIModelManager = require('../models/AIModelManager');

// Basic API routes
router.get('/status', (req, res) => {
  try {
    res.json({
      status: 'healthy',
      service: 'OrchestrateX API',
      database: 'Google Cloud Firestore',
      storage_method: 'google_cloud_firestore',
      database_connected: true,
      models_available: [
        'GLM-4.5',
        'GPT-OSS', 
        'Llama-4-Maverick',
        'Kimi-K2',
        'TNG-DeepSeek-R1T2'
      ],
      database_info: 'Google Cloud Firestore',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Status endpoint error:', error);
    res.status(500).json({
      status: 'error',
      service: 'OrchestrateX API',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Analytics endpoint
router.get('/analytics', async (req, res) => {
  try {
    const analytics = await AIModelManager.getModelAnalytics('7d');
    
    // Get basic counts
    const promptsSnapshot = await require('../config/firestore').collection('ai_prompts').get();
    const responsesSnapshot = await require('../config/firestore').collection('model_responses').get();
    
    // Get recent prompts
    const recentPromptsSnapshot = await require('../config/firestore')
      .collection('ai_prompts')
      .orderBy('timestamp', 'desc')
      .limit(5)
      .get();
    
    const recentPrompts = [];
    recentPromptsSnapshot.forEach(doc => {
      const data = doc.data();
      recentPrompts.push({
        content: data.content,
        timestamp: data.timestamp,
        userId: data.userId
      });
    });
    
    res.json({
      total_user_prompts: promptsSnapshot.size,
      total_model_responses: responsesSnapshot.size,
      model_usage: analytics,
      recent_prompts: recentPrompts,
      storage_info: {
        database_connected: true,
        storage_method: 'google_cloud_firestore'
      }
    });
  } catch (error) {
    res.status(500).json({
      error: 'Failed to retrieve analytics',
      message: error.message
    });
  }
});

// Test endpoint
router.get('/test', (req, res) => {
  res.json({
    message: 'OrchestrateX API is working',
    database: 'Google Cloud Firestore',
    migration: 'MongoDB → Google Cloud Complete'
  });
});

module.exports = router;