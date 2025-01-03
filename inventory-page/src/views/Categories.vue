<template>
  <div class="categories-page">
    <h1>分类管理</h1>
    <CategoryList :isAdmin="isAdmin" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import CategoryList from '../components/CategoryList.vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const isAdmin = ref(false);

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

// 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/categories') {
      checkUserRole();
    }
  }
);

onMounted(() => {
  checkUserRole();
});
</script>

<style scoped>
.categories-page {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style> 