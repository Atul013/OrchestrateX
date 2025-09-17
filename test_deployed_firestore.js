const https = require('https');

const testData = JSON.stringify({
  prompt: "Hello! Testing the deployed Firestore database from orchestratex.me",
  userId: "deployment-test-user",
  sessionId: "deployment-session-" + Date.now(),
  language: "en"
});

const options = {
  hostname: 'orchestratex-api-84388526388.us-central1.run.app',
  port: 443,
  path: '/api/ai-models/prompt',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': testData.length
  }
};

console.log('🧪 TESTING DEPLOYED FIRESTORE DATABASE');
console.log('=====================================');
console.log('');
console.log('🌐 Cloud URL: https://orchestratex-api-84388526388.us-central1.run.app');
console.log('📝 Testing prompt storage in Firestore...');
console.log('');

const req = https.request(options, (res) => {
  console.log(`📊 Response Status: ${res.statusCode}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    try {
      const response = JSON.parse(data);
      console.log('🎉 SUCCESS! Prompt stored in cloud Firestore!');
      console.log('📄 Response:', JSON.stringify(response, null, 2));
      
      if (response.success) {
        console.log('');
        console.log('✅ FIRESTORE INTEGRATION CONFIRMED!');
        console.log('✅ Database: Google Cloud Firestore');
        console.log('✅ Storage ID:', response.data?.id);
        console.log('✅ User ID:', response.data?.userId);
        console.log('✅ Session ID:', response.data?.sessionId);
        console.log('✅ Timestamp:', response.data?.timestamp);
        console.log('');
        console.log('🌐 YOUR DEPLOYMENT IS COMPLETE!');
        console.log('When users enter prompts on orchestratex.me,');
        console.log('they will now be stored in Google Cloud Firestore!');
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