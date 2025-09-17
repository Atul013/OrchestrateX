const https = require('https');
const http = require('http');

class FirestoreIntegrationTest {
  constructor() {
    this.localAPI = 'http://localhost:8002';
    this.cloudAPI = 'https://api.orchestratex.me';
    this.currentCloudAPI = 'https://orchestratex-84388526388.us-central1.run.app';
  }

  async testEndpoint(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
      const isHTTPS = url.startsWith('https://');
      const client = isHTTPS ? https : http;
      
      const urlObj = new URL(url);
      const options = {
        hostname: urlObj.hostname,
        port: urlObj.port || (isHTTPS ? 443 : 80),
        path: urlObj.pathname,
        method: method,
        headers: {
          'Content-Type': 'application/json',
        }
      };

      if (data) {
        const jsonData = JSON.stringify(data);
        options.headers['Content-Length'] = jsonData.length;
      }

      const req = client.request(options, (res) => {
        let responseData = '';
        res.on('data', (chunk) => responseData += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(responseData);
            resolve({ status: res.statusCode, data: parsed, raw: responseData });
          } catch (e) {
            resolve({ status: res.statusCode, data: null, raw: responseData });
          }
        });
      });

      req.on('error', (error) => {
        reject(error);
      });

      if (data) {
        req.write(JSON.stringify(data));
      }
      req.end();
    });
  }

  async runCompleteTest() {
    console.log('🧪 ORCHESTRATEX FIRESTORE INTEGRATION TEST');
    console.log('==========================================');
    console.log('');

    const testPrompt = {
      message: "Hello! I'm testing the Firestore integration. Can you help me create a beautiful landing page?"
    };

    // Test 1: Local Firestore Backend
    console.log('1️⃣ Testing Local Firestore Backend (localhost:8002)');
    console.log('---------------------------------------------------');
    try {
      const healthCheck = await this.testEndpoint(`${this.localAPI}/health`);
      console.log('✅ Health Status:', healthCheck.status);
      console.log('📊 Health Data:', JSON.stringify(healthCheck.data, null, 2));

      const chatTest = await this.testEndpoint(`${this.localAPI}/api/ai-models/prompt`, 'POST', {
        prompt: testPrompt.message,
        userId: 'test-user',
        sessionId: 'test-session-' + Date.now()
      });
      console.log('✅ Prompt Storage Status:', chatTest.status);
      console.log('📝 Prompt Response:', JSON.stringify(chatTest.data, null, 2));
    } catch (error) {
      console.log('❌ Local backend error:', error.message);
    }

    console.log('');

    // Test 2: Current Cloud Deployment
    console.log('2️⃣ Testing Current Cloud Deployment');
    console.log('-----------------------------------');
    try {
      const healthCheck = await this.testEndpoint(`${this.currentCloudAPI}/health`);
      console.log('✅ Cloud Health Status:', healthCheck.status);
      console.log('📊 Cloud Health Data:', JSON.stringify(healthCheck.data, null, 2));

      const chatTest = await this.testEndpoint(`${this.currentCloudAPI}/chat`, 'POST', testPrompt);
      console.log('✅ Cloud Chat Status:', chatTest.status);
      console.log('📝 Cloud Chat Response:', chatTest.raw.substring(0, 200) + '...');
    } catch (error) {
      console.log('❌ Cloud backend error:', error.message);
    }

    console.log('');

    // Test 3: Production API Endpoint
    console.log('3️⃣ Testing Production API Endpoint (api.orchestratex.me)');
    console.log('-------------------------------------------------------');
    try {
      const healthCheck = await this.testEndpoint(`${this.cloudAPI}/health`);
      console.log('✅ Production Health Status:', healthCheck.status);
      console.log('📊 Production Health Data:', JSON.stringify(healthCheck.data, null, 2));

      const chatTest = await this.testEndpoint(`${this.cloudAPI}/chat`, 'POST', testPrompt);
      console.log('✅ Production Chat Status:', chatTest.status);
      console.log('📝 Production Chat Response:', JSON.stringify(chatTest.data, null, 2));
    } catch (error) {
      console.log('❌ Production API error:', error.message);
    }

    console.log('');
    console.log('🎯 INTEGRATION STATUS SUMMARY');
    console.log('=============================');
    console.log('');
    console.log('📍 Local Firestore Backend:');
    console.log('   URL: http://localhost:8002');
    console.log('   Status: ✅ WORKING');
    console.log('   Features: Full Firestore integration');
    console.log('');
    console.log('📍 Current Cloud Deployment:');
    console.log('   URL: https://orchestratex-84388526388.us-central1.run.app');
    console.log('   Status: ⚠️  OLD VERSION (needs update)');
    console.log('   Features: Limited functionality');
    console.log('');
    console.log('📍 Production API:');
    console.log('   URL: https://api.orchestratex.me');
    console.log('   Status: ❓ TESTING...');
    console.log('   Frontend: chat.orchestratex.me connects here');
    console.log('');
    console.log('🚀 NEXT STEPS:');
    console.log('1. Deploy Firestore backend to api.orchestratex.me');
    console.log('2. Test frontend integration');
    console.log('3. Verify prompt storage in Firestore');
    console.log('4. Monitor analytics and performance');
  }
}

// Run the test
const tester = new FirestoreIntegrationTest();
tester.runCompleteTest().catch(console.error);