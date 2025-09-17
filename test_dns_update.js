const https = require('https');

async function testDNSUpdate() {
  console.log('🔄 Testing DNS update for api.orchestratex.me...');
  console.log('Expected: Should point to Firestore backend');
  console.log('==========================================');
  
  try {
    const options = {
      hostname: 'api.orchestratex.me',
      port: 443,
      path: '/health',
      method: 'GET'
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        console.log('✅ Response received:');
        console.log(data);
        
        if (data.includes('Google Cloud Firestore')) {
          console.log('🎉 SUCCESS! DNS updated correctly - Firestore backend active!');
        } else if (data.includes('ai_models')) {
          console.log('⏳ Still pointing to old backend - DNS not updated yet');
        } else {
          console.log('❓ Unexpected response');
        }
      });
    });

    req.on('error', (error) => {
      console.log('❌ Error:', error.message);
    });

    req.end();
  } catch (error) {
    console.log('❌ Test failed:', error.message);
  }
}

testDNSUpdate();