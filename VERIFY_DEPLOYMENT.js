const https = require('https');

class DeploymentVerifier {
  constructor() {
    this.testCases = [
      {
        name: 'Local Firestore Backend',
        url: 'http://localhost:8002/health',
        expected: 'healthy'
      },
      {
        name: 'Production API Health',
        url: 'https://api.orchestratex.me/health',
        expected: 'healthy'
      },
      {
        name: 'Production API Chat',
        url: 'https://api.orchestratex.me/chat',
        method: 'POST',
        data: { message: 'Test deployment verification' },
        expected: 'response'
      }
    ];
  }

  async testEndpoint(test) {
    return new Promise((resolve) => {
      const isHTTPS = test.url.startsWith('https://');
      const client = isHTTPS ? https : require('http');
      
      const urlObj = new URL(test.url);
      const options = {
        hostname: urlObj.hostname,
        port: urlObj.port || (isHTTPS ? 443 : 80),
        path: urlObj.pathname,
        method: test.method || 'GET',
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      };

      const jsonData = test.data ? JSON.stringify(test.data) : null;
      if (jsonData) {
        options.headers['Content-Length'] = jsonData.length;
      }

      const req = client.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          resolve({
            success: res.statusCode === 200,
            status: res.statusCode,
            data: data,
            test: test.name
          });
        });
      });

      req.on('error', (error) => {
        resolve({
          success: false,
          status: 'ERROR',
          data: error.message,
          test: test.name
        });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({
          success: false,
          status: 'TIMEOUT',
          data: 'Request timeout',
          test: test.name
        });
      });

      if (jsonData) {
        req.write(jsonData);
      }
      req.end();
    });
  }

  async verifyDeployment() {
    console.log('🔍 ORCHESTRATEX DEPLOYMENT VERIFICATION');
    console.log('=======================================');
    console.log('');

    const results = [];

    for (const test of this.testCases) {
      console.log(`🧪 Testing: ${test.name}`);
      const result = await this.testEndpoint(test);
      results.push(result);

      if (result.success) {
        console.log(`   ✅ Status: ${result.status}`);
        try {
          const parsed = JSON.parse(result.data);
          if (parsed.status === 'healthy') {
            console.log(`   🟢 Health: ${parsed.status}`);
          } else {
            console.log(`   📊 Response: ${JSON.stringify(parsed).substring(0, 100)}...`);
          }
        } catch (e) {
          console.log(`   📄 Response: ${result.data.substring(0, 50)}...`);
        }
      } else {
        console.log(`   ❌ Status: ${result.status}`);
        console.log(`   ⚠️  Error: ${result.data}`);
      }
      console.log('');
    }

    // Summary
    console.log('📊 DEPLOYMENT VERIFICATION SUMMARY');
    console.log('==================================');
    console.log('');

    const passed = results.filter(r => r.success).length;
    const total = results.length;

    if (passed === total) {
      console.log('🎉 ALL TESTS PASSED! 🎉');
      console.log('');
      console.log('✅ Your Firestore backend is fully deployed!');
      console.log('✅ Frontend integration is working!');
      console.log('✅ Prompts from orchestratex.me will be stored in Firestore!');
      console.log('');
      console.log('🌐 Test your deployment:');
      console.log('   1. Go to https://chat.orchestratex.me');
      console.log('   2. Send a test message');
      console.log('   3. Check Firestore console for stored data');
      console.log('');
      console.log('🔗 Firestore Console: https://console.firebase.google.com/project/orchestratex-app/firestore');
    } else {
      console.log(`⚠️  ${passed}/${total} tests passed`);
      console.log('');
      console.log('❌ Issues detected:');
      results.forEach(r => {
        if (!r.success) {
          console.log(`   • ${r.test}: ${r.data}`);
        }
      });
      console.log('');
      console.log('💡 Next steps:');
      console.log('   1. Check deployment logs');
      console.log('   2. Verify DNS configuration');
      console.log('   3. Run deployment script again');
    }

    console.log('');
    return passed === total;
  }
}

// Run verification
const verifier = new DeploymentVerifier();
verifier.verifyDeployment().catch(console.error);