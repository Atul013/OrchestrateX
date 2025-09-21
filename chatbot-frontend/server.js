const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// Serve static files from the dist directory
app.use(express.static(path.join(__dirname, 'dist')));

// Proxy API requests to the backend
app.use('/api', createProxyMiddleware({
  target: 'https://orchestratex-api-84388526388.us-central1.run.app',
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
  console.log(`🔗 API Proxy: http://localhost:${PORT}/api -> https://orchestratex-api-84388526388.us-central1.run.app/api`);
});