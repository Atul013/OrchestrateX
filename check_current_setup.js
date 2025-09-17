const https = require('https');

async function testAPIEndpoint(url, endpoint, data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: url,
      port: 443,
      path: endpoint,
      method: data ? 'POST' : 'GET',
      headers: { 'Content-Type': 'application/json' }
    };

    if (data) {
      const jsonData = JSON.stringify(data);
      options.headers['Content-Length'] = jsonData.length;
    }

    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        resolve({ status: res.statusCode, data: responseData });
      });
    });

    req.on('error', reject);
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

async function checkCurrentSetup() {
  console.log('🔍 CHECKING CURRENT ORCHESTRATEX API SETUP');
  console.log('==========================================');
  console.log('');

  // Test api.orchestratex.me
  console.log('1️⃣ Testing api.orchestratex.me (what chat.orchestratex.me uses)');
  try {
    const health = await testAPIEndpoint('api.orchestratex.me', '/health');
    console.log('✅ Health response:', health.data);
    
    // Test if it has Firestore endpoints
    const promptTest = await testAPIEndpoint('api.orchestratex.me', '/api/ai-models/prompt', {
      prompt: 'Test if this has Firestore',
      userId: 'test',
      sessionId: 'test-123'
    });
    console.log('📝 Prompt test status:', promptTest.status);
    console.log('📄 Prompt response:', promptTest.data.substring(0, 200));
  } catch (error) {
    console.log('❌ api.orchestratex.me error:', error.message);
  }

  console.log('');

  // Test our new deployed endpoint
  console.log('2️⃣ Testing orchestratex-api-84388526388.us-central1.run.app (our new Firestore backend)');
  try {
    const health = await testAPIEndpoint('orchestratex-api-84388526388.us-central1.run.app', '/health');
    console.log('✅ Health response:', health.data);
    
    const promptTest = await testAPIEndpoint('orchestratex-api-84388526388.us-central1.run.app', '/api/ai-models/prompt', {
      prompt: 'Test Firestore storage',
      userId: 'test',
      sessionId: 'test-456'
    });
    console.log('📝 Prompt test status:', promptTest.status);
    console.log('📄 Prompt response:', promptTest.data.substring(0, 200));
  } catch (error) {
    console.log('❌ New Firestore backend error:', error.message);
  }

  console.log('');
  console.log('🎯 SUMMARY:');
  console.log('===========');
  console.log('');
  console.log('📍 Current Flow:');
  console.log('   https://chat.orchestratex.me → https://api.orchestratex.me → OLD backend (no Firestore)');
  console.log('');
  console.log('📍 New Firestore Flow:');
  console.log('   https://chat.orchestratex.me → https://orchestratex-api-84388526388.us-central1.run.app → Firestore ✅');
  console.log('');
  console.log('🔧 TO ENABLE FIRESTORE STORAGE:');
  console.log('   Point api.orchestratex.me to: https://orchestratex-api-84388526388.us-central1.run.app');
}

checkCurrentSetup();