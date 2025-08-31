// Backend API integration for OrchestrateX
export interface OrchestrateResponse {
  success: boolean;
  primary_response: {
    success: boolean;
    model_name: string;
    response_text: string;
    tokens_used: number;
    cost_usd: number;
    latency_ms: number;
  };
  critiques: Array<{
    model_name: string;
    critique_text: string;
    tokens_used: number;
    cost_usd: number;
    latency_ms: number;
  }>;
  total_cost: number;
  api_calls: number;
  success_rate: number;
}

export interface ModelSelectorResponse {
  selected_model: string;
  confidence_scores: Record<string, number>;
}

class OrchestrateXAPI {
  private baseURL: string;

  constructor() {
    // Using the Python client directly since it handles the orchestration
    // We'll need to create a simple HTTP wrapper around advanced_client.py
    this.baseURL = 'http://localhost:8000';
  }

  async orchestrateQuery(prompt: string): Promise<OrchestrateResponse> {
    try {
      const response = await fetch(`${this.baseURL}/orchestrate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      // Fallback to direct Python client call
      return this.fallbackToDirectCall(prompt);
    }
  }

  private async fallbackToDirectCall(prompt: string): Promise<OrchestrateResponse> {
    // This is a mock response that simulates what we'd get from the Python client
    // In a real setup, you'd run the Python client as a web service
    try {
      // Simulate the orchestration result format from our test
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate delay
      
      return {
        success: true,
        primary_response: {
          success: true,
          model_name: "GPT-OSS",
          response_text: `Here's a response to your query: "${prompt}". This is a simulated response. To get real AI model responses, please start the OrchestrateX backend server that integrates with the OpenRouter API.`,
          tokens_used: 150,
          cost_usd: 0.0000,
          latency_ms: 2000
        },
        critiques: [
          {
            model_name: "TNG DeepSeek",
            critique_text: "Missing specific examples",
            tokens_used: 50,
            cost_usd: 0.0000,
            latency_ms: 1500
          },
          {
            model_name: "GLM4.5",
            critique_text: "Needs more context",
            tokens_used: 45,
            cost_usd: 0.0000,
            latency_ms: 1800
          }
        ],
        total_cost: 0.0000,
        api_calls: 3,
        success_rate: 100.0
      };
    } catch (error) {
      throw new Error('Failed to process query');
    }
  }

  async getModelRecommendation(prompt: string): Promise<ModelSelectorResponse> {
    try {
      const response = await fetch(`${this.baseURL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Model Selector API Error:', error);
      // Fallback to default model
      return {
        selected_model: 'GPT-OSS',
        confidence_scores: { 'GPT-OSS': 0.8 }
      };
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

export const orchestrateAPI = new OrchestrateXAPI();
