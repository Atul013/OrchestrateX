// Quick test to verify what the orchestrateAPI is returning
import { orchestrateAPI } from './src/services/orchestrateAPI.js';

async function testAPIResponse() {
  console.log('Testing orchestrateAPI response...');
  
  try {
    const response = await orchestrateAPI.orchestrateQuery("test prompt");
    console.log('Full response:', JSON.stringify(response, null, 2));
    console.log('Primary response text:', response.primary_response.response_text);
    console.log('Critiques:', response.critiques);
  } catch (error) {
    console.error('Error:', error);
  }
}

testAPIResponse();
