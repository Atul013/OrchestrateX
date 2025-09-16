const axios = require('axios');

async function testMigration() {
  const API_URL = 'https://orchestratex-84388526388.us-central1.run.app/api';
  
  console.log('🧪 Testing MongoDB → Google Cloud migration...');
  
  try {
    // Test health endpoint
    console.log('🏥 Testing health endpoint...');
    const healthResponse = await axios.get(`${API_URL}/../health`);
    console.log('✅ Health check passed:', healthResponse.data);
    
    // Test prompt storage
    console.log('📝 Testing prompt storage...');
    const promptResponse = await axios.post(`${API_URL}/ai-models/prompt`, {
      prompt: 'Test: Migration from MongoDB to Google Cloud',
      userId: 'migration-test',
      language: 'en'
    });
    
    console.log('✅ Prompt stored in Google Cloud:', promptResponse.data);
    
    // Test model response storage
    console.log('🤖 Testing model response storage...');
    const responseData = {
      promptId: promptResponse.data.data.id,
      sessionId: promptResponse.data.data.sessionId,
      modelName: 'GLM45',
      response: 'Test response from Google Cloud Firestore',
      responseTime: 1500,
      tokenCount: 45,
      temperature: 0.7
    };
    
    const modelResponse = await axios.post(`${API_URL}/ai-models/response`, responseData);
    console.log('✅ Model response stored:', modelResponse.data);
    
    console.log('🎉 Migration test successful!');
    console.log('📈 Your system is now using Google Cloud Firestore instead of MongoDB');
    
  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

// Install axios if needed
const { spawn } = require('child_process');
const installAxios = spawn('npm', ['install', 'axios'], { stdio: 'inherit' });

installAxios.on('close', (code) => {
  if (code === 0) {
    testMigration();
  } else {
    console.error('Failed to install axios');
  }
});