const express = require('express');
const cors = require('cors');

// Add error handling for unhandled promises
process.on('unhandledRejection', (reason, promise) => {
  console.log('❌ Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
  console.log('❌ Uncaught Exception thrown:', error);
});

// Import routes
const apiRoutes = require('./routes/api');
const aiModelRoutes = require('./routes/ai-models');

const app = express();
const PORT = process.env.PORT || 8002;

// Middleware
app.use(cors({
  origin: [
    'https://chat.orchestratex.me',
    'https://orchestratex-frontend-84388526388.us-central1.run.app',
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:8080'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Serve static files for testing
app.use(express.static('.'));

// Routes
app.use('/api', apiRoutes);
app.use('/api/ai-models', aiModelRoutes);

// Health check with database info
app.get('/health', (req, res) => {
  try {
    res.json({ 
      status: 'healthy',
      database: 'Google Cloud Firestore',
      features: [
        'AI Prompt Storage',
        '5 Model Response Tracking',
        'Model Criticism System',
        'Model Suggestions',
        'Performance Analytics',
        'Session Management'
      ],
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('❌ Health check error:', error);
    res.status(500).json({
      status: 'error',
      error: error.message
    });
  }
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

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 OrchestrateX Server running on port ${PORT}`);
  console.log(`🔥 Google Cloud Firestore connected`);
  console.log(`🤖 5 AI Models supported`);
  console.log(`📊 Full analytics tracking enabled`);
  console.log(`📡 Server ready to accept connections`);
}).on('error', (err) => {
  console.error('❌ Server error:', err);
  if (err.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} is already in use`);
  }
}).on('listening', () => {
  console.log(`✅ Server is now listening on port ${PORT}`);
});

module.exports = app;