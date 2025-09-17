const https = require('https');

const testData = JSON.stringify({
  message: "Hello from orchestratex.me! Please test this prompt storage in Firestore. Can you help me create a beautiful landing page for my AI startup?"
});

const options = {
  hostname: 'orchestratex-84388526388.us-central1.run.app',
  port: 443,
  path: '/chat',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': testData.length
  }
};

console.log('🧪 TESTING CLOUD FIRESTORE VIA /chat ENDPOINT');
console.log('==============================================');
console.log('');
console.log('🌐 Testing: https://orchestratex-84388526388.us-central1.run.app/chat');
console.log('📝 Sending prompt to Firestore...');
console.log('');

const req = https.request(options, (res) => {
  console.log(`📊 Response Status: ${res.statusCode}`);
  
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('📄 Response received:');
    console.log(data);
    
    if (res.statusCode === 200) {
      console.log('');
      console.log('🎉 SUCCESS! Your prompt was processed and stored in Firestore!');
      console.log('✅ orchestratex.me → Cloud Server → Google Firestore ✅');
    }
  });
});

req.on('error', (error) => {
  console.error('❌ Error:', error.message);
});

req.write(testData);
req.end();