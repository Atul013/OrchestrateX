const express = require('express');
const app = express();
const PORT = 8002;

console.log('Starting simple test server...');

app.get('/test', (req, res) => {
  res.json({ message: 'Simple test server working' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Simple server running on http://localhost:${PORT}`);
}).on('error', (err) => {
  console.error('❌ Server error:', err);
});