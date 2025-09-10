import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 300000, // 5 minutes timeout for AI workflows (real workflows can take 60-300 seconds)
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.config?.url, error.response?.status);
    
    // Handle common error scenarios
    if (error.response?.status === 422) {
      console.error('Validation Error:', error.response.data);
    } else if (error.response?.status === 500) {
      console.error('Server Error:', error.response.data);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request Timeout');
    }
    
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/api/health');
    return response.data;
  },

  // Get available workflows
  async getWorkflows() {
    const response = await api.get('/api/workflows');
    return response.data;
  },

  // Get agent types information
  async getAgentTypes() {
    const response = await api.get('/api/agent-types');
    return response.data;
  },

  // Workflow endpoints
  async runAdvancedWorkflow(leadData) {
    const response = await api.post('/api/agents/advanced', leadData);
    return response.data;
  },

  async runIntermediateWorkflow(leadData) {
    const response = await api.post('/api/agents/intermediate', leadData);
    return response.data;
  },

  async runBasicWorkflow(leadData) {
    const response = await api.post('/api/agents/basic', leadData);
    return response.data;
  },

  async runEnhancedWorkflow(leadData) {
    const response = await api.post('/api/agents/enhanced', leadData);
    return response.data;
  },

  // Streaming workflow endpoints using fetch with ReadableStream
  async createWorkflowStream(endpoint, leadData, onMessage, onError, onComplete) {
    try {
      // Map frontend field names to backend expected names
      const backendData = {
        company_name: leadData.company_name,
        contact_name: leadData.contact_name,
        contact_email: leadData.contact_email,
        company_size: leadData.company_size,
        industry: leadData.industry,
        location: leadData.location || "",
        annual_revenue: leadData.annual_revenue || null,
        pain_points: leadData.pain_points || [],
        tech_stack: leadData.tech_stack || []
      };

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify(backendData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      const readStream = async () => {
        try {
          while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
              onComplete();
              break;
            }

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6));
                  onMessage(data);
                } catch (parseError) {
                  console.warn('Error parsing SSE data:', parseError, line);
                }
              }
            }
          }
        } catch (streamError) {
          onError(streamError);
        }
      };

      readStream();

      // Return an object with a close method for cleanup
      return {
        close: () => {
          reader.cancel();
        }
      };
    } catch (error) {
      onError(error);
      return null;
    }
  },

  async runAdvancedWorkflowStream(leadData, onMessage, onError, onComplete) {
    return await this.createWorkflowStream('/api/agents/advanced/stream', leadData, onMessage, onError, onComplete);
  },

  async runIntermediateWorkflowStream(leadData, onMessage, onError, onComplete) {
    return await this.createWorkflowStream('/api/agents/intermediate/stream', leadData, onMessage, onError, onComplete);
  },

  async runBasicWorkflowStream(leadData, onMessage, onError, onComplete) {
    return await this.createWorkflowStream('/api/agents/basic/stream', leadData, onMessage, onError, onComplete);
  },
};

// Export axios instance for custom requests
export default api;