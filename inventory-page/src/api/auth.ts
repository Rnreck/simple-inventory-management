import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const authApi = {
  login: async (credentials: { username: string; password: string }) => {
    const response = await axios.post(`${API_URL}/users/login`, credentials);
    return response.data;
  },

  register: async (userData: { username: string; password: string; role?: string }) => {
    const response = await axios.post(`${API_URL}/users/register`, userData);
    return response.data;
  }
}; 