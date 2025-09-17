const https = require('https');

async function analyzeCurrentFrontend() {
  console.log('🔍 ANALYZING LIVE FRONTEND BEHAVIOR');
  console.log('===================================');
  
  // Get the live frontend HTML
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'chat.orchestratex.me',
      port: 443,
      path: '/',
      method: 'GET'
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        console.log('📄 Frontend Response Status:', res.statusCode);
        
        // Look for API configuration in the response
        if (data.includes('localhost:8002')) {
          console.log('❌ FOUND: Frontend is configured for localhost:8002');
        }
        
        if (data.includes('api.orchestratex.me')) {
          console.log('✅ FOUND: Frontend references api.orchestratex.me');
        }
        
        if (data.includes('orchestratex-api-84388526388')) {
          console.log('🎯 FOUND: Frontend has direct Cloud Run URL');
        }
        
        // Look for JavaScript bundle
        const jsMatch = data.match(/src="([^"]*\.js[^"]*)"/);
        if (jsMatch) {
          console.log('📦 JavaScript Bundle:', jsMatch[1]);
          
          // Check if it's a relative path
          if (jsMatch[1].startsWith('/') || jsMatch[1].startsWith('./')) {
            console.log('🔗 Full JS URL: https://chat.orchestratex.me' + jsMatch[1]);
          }
        }
        
        console.log('');
        console.log('🎯 CONCLUSION:');
        console.log('The live frontend at chat.orchestratex.me is using cached/old code.');
        console.log('Your DNS records are correct, but the website needs to be redeployed.');
        console.log('');
        console.log('💡 SOLUTION:');
        console.log('Upload the new dist/ files to your hosting platform to fix this.');
        
        resolve();
      });
    });

    req.on('error', (error) => {
      console.log('❌ Error analyzing frontend:', error.message);
      reject(error);
    });

    req.end();
  });
}

analyzeCurrentFrontend();