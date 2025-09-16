const express = require('express');
const router = express.Router();

// Basic API routes
router.get('/status', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'OrchestrateX API',
    database: 'Google Cloud Firestore',
    timestamp: new Date().toISOString()
  });
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