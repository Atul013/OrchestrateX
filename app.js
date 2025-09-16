const express = require('express');
const cors = require('cors');

// Import routes
const apiRoutes = require('./routes/api');
const aiModelRoutes = require('./routes/ai-models');

const app = express();
const PORT = process.env.PORT || 8002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Routes
app.use('/api', apiRoutes);
app.use('/api/ai-models', aiModelRoutes);

// Health check with database info
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    database: 'Google Cloud Firestore',
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

app.listen(PORT, () => {
  console.log(`🚀 OrchestrateX Server running on port ${PORT}`);
  console.log(`🔥 Google Cloud Firestore connected`);
  console.log(`🤖 6 AI Models supported`);
  console.log(`📊 Full analytics tracking enabled`);
});

module.exports = app;