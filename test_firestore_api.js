const https = require('https');

async function testFirestoreAPI() {
  console.log('🔥 TESTING FIRESTORE API DIRECTLY');
  console.log('=================================');
  
  const testData = {
    prompt: 'Hello from DNS update test!',
    userId: 'dns-test-user',
    sessionId: 'dns-test-' + Date.now()
  };

  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(testData);
    
    const options = {
      hostname: 'api.orchestratex.me',
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
        console.log('📊 Response Status:', res.statusCode);
        console.log('📄 Response Data:', data);
        
        if (data.includes('Google Cloud')) {
          console.log('🎉 SUCCESS! Firestore backend is active!');
        } else if (res.statusCode === 201 || data.includes('success')) {
          console.log('✅ API working - checking response format...');
        } else {
          console.log('⚠️ Unexpected response format');
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

testFirestoreAPI();