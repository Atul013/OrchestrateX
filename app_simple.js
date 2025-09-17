const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Add request logging middleware
app.use((req, res, next) => {
  console.log(`📝 ${req.method} ${req.path} from ${req.ip}`);
  next();
});

// Simplified in-memory storage for testing
const storage = {
  prompts: [],
  responses: [],
  criticism: [],
  suggestions: [],
  sessions: [],
  analytics: []
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    database: 'In-Memory Storage (Testing)',
    features: [
      'AI Prompt Storage',
      '6 Model Response Tracking',
      'Model Criticism System',
      'Model Suggestions',
      'Performance Analytics',
      'Session Management'
    ],
    timestamp: new Date().toISOString()
  });
});

// AI Models info endpoint
app.get('/models', (req, res) => {
  res.json({
    supportedModels: {
      GLM45: 'z-ai/glm-4.5-air:free',
      GPTOSS: 'openai/gpt-oss-20b:free', 
      LLAMA4: 'meta-llama/llama-4-maverick:free',
      KIMI: 'moonshotai/kimi-dev-72b:free',
      QWEN3: 'qwen/Qwen3-coder:free',
      FALCON: 'tngtech/deepseek-r1t2-chimera:free'
    },
    features: [
      'Parallel processing',
      'Response comparison',
      'Quality assessment',
      'Performance tracking'
    ]
  });
});

// Basic API status
app.get('/api/status', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'OrchestrateX API',
    database: 'In-Memory Storage (Testing)',
    migration: 'MongoDB → In-Memory → Google Cloud Firestore',
    timestamp: new Date().toISOString()
  });
});

// Store prompt endpoint
app.post('/api/ai-models/prompt', (req, res) => {
  try {
    const prompt = {
      id: Date.now().toString(),
      content: req.body.prompt,
      userId: req.body.userId || 'anonymous',
      sessionId: req.body.sessionId,
      timestamp: new Date().toISOString(),
      source: 'frontend'
    };

    storage.prompts.push(prompt);
    console.log(`✅ Prompt stored: ${prompt.id}`);
    
    res.status(201).json({
      success: true,
      message: 'Prompt stored successfully',
      data: prompt
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to store prompt',
      error: error.message
    });
  }
});

// Get stored prompts
app.get('/api/ai-models/prompts', (req, res) => {
  res.json({
    success: true,
    count: storage.prompts.length,
    data: storage.prompts
  });
});

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 OrchestrateX Server running on port ${PORT}`);
  console.log(`🌐 Server bound to: 0.0.0.0:${PORT}`);
  console.log(`🔗 Access via: http://localhost:${PORT}`);
  console.log(`💾 Using in-memory storage for testing`);
  console.log(`🤖 6 AI Models supported`);
  console.log(`📊 Full analytics tracking enabled`);
}).on('error', (err) => {
  console.error('❌ Server error:', err);
  if (err.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} is already in use`);
  } else if (err.code === 'EACCES') {
    console.error(`❌ Permission denied for port ${PORT}`);
  }
});

// Add connection logging
server.on('connection', (socket) => {
  console.log('👋 New connection from:', socket.remoteAddress);
});

// Add request logging middleware
app.use((req, res, next) => {
  console.log(`📝 ${req.method} ${req.path} from ${req.ip}`);
  next();
});

module.exports = app;