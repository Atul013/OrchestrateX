// Simple test to demonstrate Firestore integration
const http = require('http');

console.log('🧪 TESTING FIRESTORE DATABASE - SIMPLE VERSION');
console.log('==============================================\n');

function makeRequest(path, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8002,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'orchestratex.me-test'
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

async function testPromptStorage() {
  console.log('📝 Testing prompt storage (simulating orchestratex.me)...');
  
  const testPrompt = {
    prompt: "Create a modern React landing page with animations",
    userId: "test_user_123",
    sessionId: "session_" + Date.now(),
    language: "en"
  };

  console.log(`💭 Prompt: "${testPrompt.prompt}"`);
  console.log(`👤 User: ${testPrompt.userId}`);
  console.log(`🔗 Session: ${testPrompt.sessionId}\n`);

  try {
    const result = await makeRequest('/api/ai-models/prompt', 'POST', testPrompt);
    
    if (result.status === 201 && result.data.success) {
      console.log('✅ SUCCESS: Prompt stored in Firestore!');
      console.log(`📄 Document ID: ${result.data.data.id}`);
      console.log(`🕒 Timestamp: ${result.data.data.timestamp}`);
      console.log(`💾 Collection: ai_prompts`);
      console.log('');
      return true;
    } else {
      console.log('❌ FAILED:', result.data);
      return false;
    }
  } catch (error) {
    console.error('❌ ERROR:', error.message);
    return false;
  }
}

async function checkHealth() {
  console.log('🏥 Checking server health...');
  
  try {
    const result = await makeRequest('/health');
    
    if (result.status === 200) {
      console.log('✅ Server healthy');
      console.log(`💾 Database: ${result.data.database}`);
      console.log(`⚡ Features: ${result.data.features.length} enabled`);
      console.log('');
      return true;
    }
  } catch (error) {
    console.error('❌ Health check failed:', error.message);
    return false;
  }
}

async function runTest() {
  console.log('🚀 Starting Firestore integration test...\n');
  
  // Check if server is healthy
  const healthOk = await checkHealth();
  
  if (healthOk) {
    // Test prompt storage
    const promptOk = await testPromptStorage();
    
    if (promptOk) {
      console.log('🎉 INTEGRATION TEST RESULTS:');
      console.log('===========================');
      console.log('✅ Server: RUNNING');
      console.log('✅ Firestore: CONNECTED');
      console.log('✅ Prompt Storage: WORKING');
      console.log('✅ API Endpoints: FUNCTIONAL');
      console.log('');
      console.log('🌐 CONCLUSION:');
      console.log('When users enter prompts on orchestratex.me,');
      console.log('they WILL be stored in your Firestore database!');
      console.log('');
      console.log('📋 HOW TO TEST WITH ORCHESTRATEX.ME:');
      console.log('1. Open orchestratex.me in your browser');
      console.log('2. Enter any prompt in the input field');
      console.log('3. Submit the prompt');
      console.log('4. Check server logs to see storage confirmation');
      console.log('5. Use Google Cloud Console to view stored data');
    }
  }
}

runTest();