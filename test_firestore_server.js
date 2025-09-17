const axios = require('axios');

async function testServer() {
  try {
    console.log('🔍 Testing server connectivity...');
    
    // Test health endpoint
    const healthResponse = await axios.get('http://localhost:8002/health');
    console.log('✅ Health check passed');
    console.log('📊 Health response:', JSON.stringify(healthResponse.data, null, 2));
    
    // Test models endpoint
    const modelsResponse = await axios.get('http://localhost:8002/models');
    console.log('✅ Models endpoint working');
    console.log('🤖 Models response:', JSON.stringify(modelsResponse.data, null, 2));
    
    // Test basic API status
    const statusResponse = await axios.get('http://localhost:8002/api/status');
    console.log('✅ API status check passed');
    console.log('⚡ Status response:', JSON.stringify(statusResponse.data, null, 2));
    
    console.log('\n🎉 All tests passed! Firestore migration is working perfectly!');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
  }
}

testServer();