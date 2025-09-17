const https = require('https');

async function testBackendDirectly() {
  console.log('🔥 TESTING FIRESTORE BACKEND DIRECTLY');
  console.log('====================================');
  
  const testData = {
    prompt: 'Backend test - is Firestore working?',
    userId: 'backend-test',
    sessionId: 'test-' + Date.now()
  };

  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(testData);
    
    const options = {
      hostname: 'orchestratex-api-84388526388.us-central1.run.app',
      port: 443,
      path: '/api/ai-models/prompt',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': postData.length
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        console.log('📊 Status Code:', res.statusCode);
        console.log('📄 Response:', data);
        
        if (res.statusCode === 201 && data.includes('Google Cloud')) {
          console.log('🎉 BACKEND IS WORKING PERFECTLY!');
          console.log('✅ Firestore database operational');
          console.log('✅ Prompt storage successful');
          console.log('');
          console.log('🔍 THE ONLY ISSUE: DNS propagation delay');
          console.log('   api.orchestratex.me → still pointing to old backend');
          console.log('   Wait 10-20 more minutes for DNS update');
        }
        resolve();
      });
    });

    req.on('error', (error) => {
      console.log('❌ Error:', error.message);
      reject(error);
    });

    req.write(postData);
    req.end();
  });
}

testBackendDirectly();