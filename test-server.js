const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8004;

// Add error handling
process.on('unhandledRejection', (reason, promise) => {
  console.log('❌ Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
  console.log('❌ Uncaught Exception thrown:', error);
  process.exit(1);
});

// Basic middleware
app.use(cors());
app.use(express.json());

// Simple test endpoint
app.get('/test', (req, res) => {
  console.log('📡 Test endpoint called');
  res.json({ 
    message: 'Server is working!',
    timestamp: new Date().toISOString()
  });
});

// Health check
app.get('/health', (req, res) => {
  console.log('🔍 Health check called');
  res.json({ 
    status: 'healthy',
    message: 'Test server is running'
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Test Server running on port ${PORT}`);
  console.log(`📡 Server ready for testing`);
}).on('error', (err) => {
  console.error('❌ Server error:', err);
}).on('listening', () => {
  console.log(`✅ Server is listening on port ${PORT}`);
});

module.exports = app;