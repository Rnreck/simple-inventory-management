<template>
  <div class="orders-page">
    <h1>订单管理</h1>
    <OrderList
      :orders="orders"
      :isAdmin="isAdmin"
      @update="loadOrders"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onActivated } from 'vue';
import { ordersApi } from '../api/orders';
import OrderList from '../components/OrderList.vue';
import { ElMessage } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const orders = ref<any[]>([]);
const isAdmin = ref(false);
const loading = ref(false);

const checkUserRole = () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) {
    router.push('/login');
    return false;
  }
  try {
    const user = JSON.parse(userStr);
    isAdmin.value = user.role === 'admin';
    return true;
  } catch (error) {
    console.error('Error parsing user data:', error);
    router.push('/login');
    return false;
  }
};

const loadOrders = async () => {
  if (!checkUserRole() || loading.value) return;
  
  loading.value = true;
  try {
    const response = await ordersApi.getOrders();
    if (response && Array.isArray(response.orders)) {
      orders.value = response.orders;
    } else {
      orders.value = [];
      console.error('Invalid orders data:', response);
    }
  } catch (error) {
    orders.value = [];
    ElMessage.error('获取订单列表失败');
    console.error('Error loading orders:', error);
  } finally {
    loading.value = false;
  }
};

// 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/orders') {
      loadOrders();
    }
  }
);

// 组件被激活时重新加载数据
onActivated(() => {
  if (route.path === '/orders') {
    loadOrders();
  }
});

onMounted(async () => {
  if (checkUserRole()) {
    await loadOrders();
  }
});
</script>

<style scoped>
.orders-page {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style> 