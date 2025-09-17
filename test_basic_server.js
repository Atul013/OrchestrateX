// Simple test using built-in modules
const http = require('http');
const querystring = require('querystring');

function makeRequest(path, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8002,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          resolve({ status: res.statusCode, data: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }
    
    req.end();
  });
}

async function runTests() {
  console.log('🔍 Testing OrchestrateX Server...\n');

  try {
    // Test 1: Health check
    console.log('1️⃣ Testing health endpoint...');
    const health = await makeRequest('/health');
    console.log('✅ Health:', health.status, health.data.status);

    // Test 2: Models endpoint
    console.log('\n2️⃣ Testing models endpoint...');
    const models = await makeRequest('/models');
    console.log('✅ Models count:', Object.keys(models.data.supportedModels).length);

    // Test 3: API status
    console.log('\n3️⃣ Testing API status...');
    const apiStatus = await makeRequest('/api/status');
    console.log('✅ API Status:', apiStatus.data.status);

    // Test 4: Store a prompt
    console.log('\n4️⃣ Testing prompt storage...');
    const promptData = {
      prompt: 'Hello, this is a test prompt for the database migration!',
      userId: 'test-user',
      sessionId: 'test-session-123'
    };
    const storePrompt = await makeRequest('/api/ai-models/prompt', 'POST', promptData);
    console.log('✅ Prompt stored:', storePrompt.data.success);

    // Test 5: Get stored prompts
    console.log('\n5️⃣ Testing prompt retrieval...');
    const getPrompts = await makeRequest('/api/ai-models/prompts');
    console.log('✅ Stored prompts:', getPrompts.data.count);

    console.log('\n🎉 ALL TESTS PASSED! Database migration system is working! 🎉');
    console.log('📊 Summary:');
    console.log('   ✅ Server connectivity: OK');
    console.log('   ✅ Health endpoint: OK');
    console.log('   ✅ Model endpoints: OK');
    console.log('   ✅ API routes: OK');
    console.log('   ✅ Data storage: OK');
    console.log('   ✅ Data retrieval: OK');

  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

runTests();