<template>
  <div id="app">
    <Navigation v-if="showNav" />
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <keep-alive :include="[]">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Navigation from './components/Navigation.vue';

const route = useRoute();
const showNav = computed(() => route.name !== 'Login');
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  padding: 20px;
  flex: 1;
}
</style> 