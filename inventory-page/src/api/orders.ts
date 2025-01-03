import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

interface OrderItem {
  product_id: number;
  quantity: number;
}

interface OrderData {
  items: OrderItem[];
}

export const ordersApi = {
  // 获取订单列表
  getOrders: async () => {
    try {
      const response = await axios.get(`${API_URL}/orders`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      // 确保返回的数据格式正确
      if (response.data && Array.isArray(response.data.orders)) {
        return {
          orders: response.data.orders
        };
      }
      return { orders: [] };
    } catch (error) {
      console.error('Error fetching orders:', error);
      throw error;
    }
  },

  // 创建订单
  createOrder: async (orderData: OrderData) => {
    try {
      const response = await axios.post(`${API_URL}/orders`, orderData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating order:', error);
      throw error;
    }
  },

  // 更新订单状态
  updateOrderStatus: async (orderId: number, status: string) => {
    try {
      const response = await axios.put(
        `${API_URL}/orders/${orderId}/status`,
        { status },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error updating order status:', error);
      throw error;
    }
  }
}; 