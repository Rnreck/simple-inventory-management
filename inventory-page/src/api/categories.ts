import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const categoriesApi = {
  // 获取所有分类
  getCategories: async () => {
    const response = await axios.get(`${API_URL}/categories`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  // 创建分类
  createCategory: async (categoryData: { name: string }) => {
    const response = await axios.post(`${API_URL}/categories`, categoryData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  // 删除分类
  deleteCategory: async (id: number) => {
    const response = await axios.delete(`${API_URL}/categories/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  }
}; 