// API Configuration for OrchestrateX Frontend
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000', // Updated to use Python backend
  ENDPOINTS: {
    CHAT: '/chat',
    ORCHESTRATE: '/orchestrate',
    MODELS: '/models',
    HEALTH: '/health'
  }
};

// API Service functions
export const apiService = {
  async sendMessage(message: string) {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: message  // Updated to use 'message' key for Python backend
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return {
        response: data.primary_response?.response_text || data.message || 'Response received',
        model: data.primary_response?.model_name || 'auto-selected',
        status: 'success',
        critiques: data.critiques || [],
        metadata: data.metadata || {},
        backend: 'python',
        totalCost: data.total_cost || 0,
        apiCalls: data.api_calls || 0,
        successRate: data.success_rate || 0
      };
    } catch (error) {
      console.error('API call failed:', error);
      // Fallback to mock response
      return {
        response: `Thank you for your message: "${message}". I'm processing this and will route it to the most appropriate model for the best response. (Note: Backend connection failed, using fallback)`,
        model: 'fallback-mock',
        status: 'mock',
        backend: 'fallback',
        error: (error as Error).message
      };
    }
  },

  async getModels() {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.MODELS}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch models:', error);
      return [];
    }
  },

  async checkHealth() {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
};
