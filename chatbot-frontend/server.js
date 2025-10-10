const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// Serve static files from the dist directory
app.use(express.static(path.join(__dirname, 'dist')));

// Proxy API requests to the Python backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8000',  // Updated to use Python backend
  changeOrigin: true,
  logLevel: 'debug'
}));

// Direct proxy for chat endpoint
app.use('/chat', createProxyMiddleware({
  target: 'http://localhost:8000',  // Python backend
  changeOrigin: true,
  logLevel: 'debug'
}));

// Direct proxy for orchestrate endpoint
app.use('/orchestrate', createProxyMiddleware({
  target: 'http://localhost:8000',  // Python backend
  changeOrigin: true,
  logLevel: 'debug'
}));

// Handle React Router (SPA) - serve index.html for all non-API routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Frontend server running on port ${PORT}`);
  console.log(`📱 Frontend: http://localhost:${PORT}`);
  console.log(`🔗 API Proxy: http://localhost:${PORT}/api -> http://localhost:8000/api`);
  console.log(`💬 Chat Proxy: http://localhost:${PORT}/chat -> http://localhost:8000/chat`);
  console.log(`🎭 Orchestrate Proxy: http://localhost:${PORT}/orchestrate -> http://localhost:8000/orchestrate`);
  console.log(`🐍 Using Python Backend (Real AI APIs)`);
});