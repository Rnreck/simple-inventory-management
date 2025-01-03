<template>
  <div class="inventory-page">
    <h1>库存管理</h1>
    
    <ProductTable
      ref="productTableRef"
      :products="products"
      :isAdmin="isAdmin"
      @update="loadProducts"
      @categoryChange="handleCategoryChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { productsApi } from '../api/products';
import ProductTable from '../components/ProductTable.vue';
import { ElMessage } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const products = ref([]);
const isAdmin = ref(false);
const productTableRef = ref<any>(null);
const currentCategoryId = ref(null);

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

const loadProducts = async (queryResults?: any[]) => {
  if (!checkUserRole()) return;

  try {
    if (queryResults) {
      products.value = queryResults;
    } else {
      const params: any = {};
      if (currentCategoryId.value) {
        params.category_id = currentCategoryId.value;
      }
      const response = await productsApi.getProducts(params);
      products.value = response.products;
    }
  } catch (error) {
    products.value = [];
    ElMessage.error('获取产品列表失败');
    console.error('Error loading products:', error);
  }
};

const handleCategoryChange = (categoryId: number | null) => {
  currentCategoryId.value = categoryId;
  loadProducts();
};

// 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/inventory') {
      loadProducts();
    }
  }
);

onMounted(async () => {
  if (checkUserRole()) {
    await loadProducts();
  }
});
</script>

<style scoped>
.inventory-page {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style> 