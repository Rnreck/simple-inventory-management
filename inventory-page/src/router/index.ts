import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Inventory from '../views/Inventory.vue';
import Orders from '../views/Orders.vue';
import Categories from '../views/Categories.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/inventory',
      name: 'Inventory',
      component: Inventory,
      meta: { 
        requiresAuth: true,
        keepAlive: false
      }
    },
    {
      path: '/orders',
      name: 'Orders',
      component: Orders,
      meta: { 
        requiresAuth: true,
        keepAlive: false
      }
    },
    {
      path: '/categories',
      name: 'Categories',
      component: Categories,
      meta: { 
        requiresAuth: true,
        keepAlive: false
      }
    }
  ]
});

// 路由守卫
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    if (!token || !user) {
      next('/login');
    } else {
      try {
        JSON.parse(user); // 验证用户数据是否有效
        next();
      } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        next('/login');
      }
    }
  } else {
    next();
  }
});

export default router; 