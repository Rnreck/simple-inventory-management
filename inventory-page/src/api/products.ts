import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

interface Product {
  id: number;
  name: string;
  category_id: number | null;
  category_name?: string;
  inventory: number;
  price: number;
  description?: string;
}

interface SearchParams {
  name?: string;
  category_id?: number | null;
  inventory?: number | null;
  price_min?: number | null;
  price_max?: number | null;
}

export const productsApi = {
  // 获取所有产品
  getProducts: async (params?: { category_id?: number | null }) => {
    const response = await axios.get<{ products: Product[] }>(`${API_URL}/products`, {
      params,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  // 搜索产品
  searchProducts: async (params: SearchParams) => {
    // 移除null值，转换为undefined
    const cleanParams = Object.fromEntries(
      Object.entries(params).filter(([_, value]) => value != null)
    );
    
    const response = await axios.get<{ products: Product[] }>(`${API_URL}/products/query`, {
      params: cleanParams,
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  // 添加产品
  addProduct: async (product: Omit<Product, 'id'>) => {
    const response = await axios.post<{ message: string }>(`${API_URL}/products`, product, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  // 更新产品
  updateProduct: async (id: number, product: Partial<Omit<Product, 'id'>>) => {
    const response = await axios.put<{ message: string }>(`${API_URL}/products/${id}`, product, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  },

  // 删除产品
  deleteProduct: async (id: number) => {
    const response = await axios.delete<{ message: string }>(`${API_URL}/products/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  }
};