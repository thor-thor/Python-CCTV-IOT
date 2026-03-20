import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  getMe: () => api.get('/api/auth/me'),
};

// Videos API
export const videosAPI = {
  getVideos: (params) => api.get('/api/videos', { params }),
  getVideo: (id) => api.get(`/api/videos/${id}`),
  createVideo: (data) => api.post('/api/videos', data),
};

// Dashboard API
export const dashboardAPI = {
  getSummary: () => api.get('/api/dashboard/summary'),
};

// Alerts API
export const alertsAPI = {
  getAlerts: (params) => api.get('/api/alerts', { params }),
  createAlert: (data) => api.post('/api/alerts', data),
  resolveAlert: (id) => api.post(`/api/alerts/${id}/resolve`),
};

// Trains API
export const trainsAPI = {
  getTrains: (params) => api.get('/api/trains', { params }),
  getTrain: (id) => api.get(`/api/trains/${id}`),
  createTrain: (data) => api.post('/api/trains', data),
  getTrainCameras: (id) => api.get(`/api/trains/${id}/cameras`),
};

// Cameras API
export const camerasAPI = {
  createCamera: (data) => api.post('/api/cameras', data),
};

export default api;
