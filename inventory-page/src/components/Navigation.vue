<template>
  <div class="nav-container">
    <el-menu
      :default-active="activeRoute"
      class="nav-menu"
      mode="horizontal"
      router
      @select="handleSelect"
    >
      <el-menu-item index="/inventory">库存管理</el-menu-item>
      <el-menu-item index="/orders">订单管理</el-menu-item>
      <el-menu-item index="/categories">分类管理</el-menu-item>
      <div class="flex-grow" />
      <el-menu-item>
        <el-dropdown @command="handleCommand">
          <span class="user-menu">
            {{ username }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ArrowDown } from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();

const activeRoute = computed(() => route.path);

const username = computed(() => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    const user = JSON.parse(userStr);
    return user.username;
  }
  return '';
});

const handleSelect = (path: string) => {
  // 强制重新加载组件
  router.replace({ path: path, force: true });
};

const handleCommand = (command: string) => {
  if (command === 'logout') {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/login');
  }
};
</script>

<style scoped>
.nav-container {
  border-bottom: solid 1px #e6e6e6;
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: white;
}

.nav-menu {
  padding: 0 20px;
  display: flex;
  align-items: center;
}

.flex-grow {
  flex-grow: 1;
}

.user-menu {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 4px;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}
</style> 