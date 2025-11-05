import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-KEY': import.meta.env.VITE_API_KEY
  }
});

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
