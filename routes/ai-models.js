const express = require('express');
const router = express.Router();
const AIModelManager = require('../models/AIModelManager');
const { v4: uuidv4 } = require('uuid');

// 1. Store prompt from frontend
router.post('/prompt', async (req, res) => {
  try {
    const promptData = {
      content: req.body.prompt,
      userId: req.body.userId || 'anonymous',
      sessionId: req.body.sessionId || uuidv4(),
      userAgent: req.get('User-Agent'),
      ip: req.ip,
      language: req.body.language
    };

    const result = await AIModelManager.storePrompt(promptData);
    
    res.status(201).json({
      success: true,
      message: 'Prompt stored in Google Cloud',
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to store prompt',
      error: error.message
    });
  }
});

// 2. Store model responses (called by AI processing)
router.post('/response', async (req, res) => {
  try {
    const responseData = {
      promptId: req.body.promptId,
      sessionId: req.body.sessionId,
      modelName: req.body.modelName,
      response: req.body.response,
      responseTime: req.body.responseTime,
      tokenCount: req.body.tokenCount,
      temperature: req.body.temperature,
      maxTokens: req.body.maxTokens,
      cost: req.body.cost
    };

    const result = await AIModelManager.storeModelResponse(responseData);
    
    res.status(201).json({
      success: true,
      message: `${req.body.modelName} response stored in Google Cloud`,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to store model response',
      error: error.message
    });
  }
});

// 3. Store model criticism
router.post('/criticism', async (req, res) => {
  try {
    const criticismData = {
      responseId: req.body.responseId,
      promptId: req.body.promptId,
      sessionId: req.body.sessionId,
      modelName: req.body.modelName,
      type: req.body.type,
      criticism: req.body.criticism,
      rating: req.body.rating,
      reviewer: req.body.reviewer,
      criticalPoints: req.body.criticalPoints,
      improvements: req.body.improvements,
      severity: req.body.severity
    };

    const result = await AIModelManager.storeModelCriticism(criticismData);
    
    res.status(201).json({
      success: true,
      message: 'Model criticism stored in Google Cloud',
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to store criticism',
      error: error.message
    });
  }
});

// 4. Store model suggestions
router.post('/suggestion', async (req, res) => {
  try {
    const suggestionData = {
      responseId: req.body.responseId,
      promptId: req.body.promptId,
      sessionId: req.body.sessionId,
      modelName: req.body.modelName,
      type: req.body.type,
      suggestion: req.body.suggestion,
      priority: req.body.priority,
      implementation: req.body.implementation,
      expectedImprovement: req.body.expectedImprovement,
      effort: req.body.effort,
      impact: req.body.impact,
      tags: req.body.tags
    };

    const result = await AIModelManager.storeModelSuggestion(suggestionData);
    
    res.status(201).json({
      success: true,
      message: 'Model suggestion stored in Google Cloud',
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to store suggestion',
      error: error.message
    });
  }
});

// 5. Get all model responses for a session
router.get('/session/:sessionId/responses', async (req, res) => {
  try {
    const responses = await AIModelManager.getSessionModelResponses(req.params.sessionId);
    
    res.status(200).json({
      success: true,
      message: 'Session model responses retrieved from Google Cloud',
      sessionId: req.params.sessionId,
      modelsCount: Object.keys(responses).length,
      data: responses
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve session responses',
      error: error.message
    });
  }
});

// 6. Compare all 6 models for a prompt
router.get('/compare/:promptId', async (req, res) => {
  try {
    const comparison = await AIModelManager.compareModelsPerformance(req.params.promptId);
    
    res.status(200).json({
      success: true,
      message: 'Model comparison retrieved from Google Cloud',
      promptId: req.params.promptId,
      modelsCompared: Object.keys(comparison).length,
      data: comparison
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to compare models',
      error: error.message
    });
  }
});

// 7. Get model analytics
router.get('/analytics/:timeRange?', async (req, res) => {
  try {
    const timeRange = req.params.timeRange || '7d';
    const analytics = await AIModelManager.getModelAnalytics(timeRange);
    
    res.status(200).json({
      success: true,
      message: 'Model analytics retrieved from Google Cloud',
      timeRange: timeRange,
      modelsAnalyzed: Object.keys(analytics).length,
      data: analytics
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve analytics',
      error: error.message
    });
  }
});

// 8. Process prompt with all 6 models (main orchestration endpoint)
router.post('/orchestrate', async (req, res) => {
  try {
    const { prompt, userId, sessionId } = req.body;
    const newSessionId = sessionId || uuidv4();
    
    // Store the prompt
    const promptResult = await AIModelManager.storePrompt({
      content: prompt,
      userId: userId || 'anonymous',
      sessionId: newSessionId,
      userAgent: req.get('User-Agent'),
      ip: req.ip
    });

    // This would trigger processing with all 6 models
    // (You'll implement the actual AI model calls here)
    
    res.status(202).json({
      success: true,
      message: 'Prompt orchestration started - processing with all 6 models',
      promptId: promptResult.id,
      sessionId: newSessionId,
      modelsToProcess: Object.keys(AIModelManager.models),
      status: 'processing'
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to orchestrate prompt processing',
      error: error.message
    });
  }
});

module.exports = router;