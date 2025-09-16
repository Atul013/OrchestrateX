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
    success: boolean;
  }>;
  total_cost: number;
  api_calls: number;
  success_rate: number;
}

export interface ModelSelectorResponse {
  selected_model: string;
  confidence_scores: Record<string, number>;
}

export interface RefinementRequest {
  original_result: OrchestrateResponse;
  selected_critique_index: number;
}

class OrchestrateXAPI {
  private baseURL: string;

  constructor() {
    // Detect if we're running in production (Cloud Run) or development
    const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1';
    
    if (isProduction) {
      // In production, use the same origin (Cloud Run URL)
      this.baseURL = window.location.origin;
    } else {
      // In development, use localhost
      this.baseURL = 'http://localhost:8002';
    }
  }

  async orchestrateQuery(prompt: string): Promise<OrchestrateResponse> {
    console.log('🚀 [DEBUG] orchestrateQuery called with prompt:', prompt);
    console.log('🚀 [DEBUG] baseURL:', this.baseURL);
    
    try {
      console.log('🚀 [DEBUG] Calling backend API at:', `${this.baseURL}/chat`);
      
      const requestBody = { message: prompt };
      console.log('🚀 [DEBUG] Request body:', requestBody);
      
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('🚀 [DEBUG] Response status:', response.status);
      console.log('🚀 [DEBUG] Response ok:', response.ok);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ [DEBUG] Backend response received:', data);
      console.log('✅ [DEBUG] Response type:', typeof data);
      console.log('✅ [DEBUG] Response keys:', Object.keys(data));
      
      return data;
    } catch (error) {
      console.error('❌ [DEBUG] API Error:', error);
      console.error('❌ [DEBUG] Error type:', typeof error);
      console.error('❌ [DEBUG] Error message:', error instanceof Error ? error.message : String(error));
      
      // Return a simple error response instead of trying fallback
      const errorResponse = {
        success: false,
        primary_response: {
          success: false,
          model_name: 'Error',
          response_text: `❌ Unable to connect to backend. Please ensure the backend API is running on port 8002. Error: ${error}`,
          tokens_used: 0,
          cost_usd: 0,
          latency_ms: 0
        },
        critiques: [],
        total_cost: 0,
        api_calls: 0,
        success_rate: 0
      };
      
      console.log('❌ [DEBUG] Returning error response:', errorResponse);
      return errorResponse;
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
