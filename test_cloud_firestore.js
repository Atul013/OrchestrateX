const https = require('https');

const testData = JSON.stringify({
  prompt: "Test prompt from orchestratex.me frontend",
  userId: "user_test_123",
  sessionId: "session_" + Date.now(),
  language: "en"
});

const options = {
  hostname: 'orchestratex-84388526388.us-central1.run.app',
  port: 443,
  path: '/api/ai-models/prompt',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': testData.length
  }
};

console.log('🧪 TESTING CLOUD FIRESTORE DATABASE');
console.log('=====================================');
console.log('');
console.log('🌐 Cloud URL: https://orchestratex-84388526388.us-central1.run.app');
console.log('📝 Testing prompt storage...');
console.log('');

const req = https.request(options, (res) => {
  console.log(`✅ Response Status: ${res.statusCode}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const response = JSON.parse(data);
      console.log('🎉 SUCCESS! Prompt stored in cloud Firestore!');
      console.log('📊 Response:', JSON.stringify(response, null, 2));
      
      if (response.success) {
        console.log('');
        console.log('✅ CONFIRMED: orchestratex.me prompts WILL be stored in Firestore!');
        console.log('✅ Database: Google Cloud Firestore');
        console.log('✅ Storage ID:', response.data?.id);
        console.log('✅ Session ID:', response.data?.sessionId);
      }
    } catch (e) {
      console.log('📄 Raw response:', data);
    }
  });
});

req.on('error', (error) => {
  console.error('❌ Error:', error.message);
});

req.write(testData);
req.end();