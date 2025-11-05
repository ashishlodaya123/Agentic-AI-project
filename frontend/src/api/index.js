import axios from 'axios';

// Check if environment variables are defined
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const apiKey = import.meta.env.VITE_API_KEY || 'triage_secret_key';

const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-KEY': apiKey
  }
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export const startTriage = (patientData) => {
  return apiClient.post('/api/triage', patientData);
};

export const uploadImage = (formData) => {
  return apiClient.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const getTaskResult = (taskId) => {
  return apiClient.get(`/api/results/${taskId}`);
};

export const getMetrics = () => {
  return apiClient.get('/metrics');
};

export const checkBackendStatus = () => {
  return apiClient.get('/');
}