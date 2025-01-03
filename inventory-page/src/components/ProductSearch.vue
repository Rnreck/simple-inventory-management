<template>
  <div class="search-form">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="产品名称">
        <el-input v-model="searchForm.name" placeholder="输入产品名称"></el-input>
      </el-form-item>
      <el-form-item label="最小库存">
        <el-input-number v-model="searchForm.inventory" :min="0"></el-input-number>
      </el-form-item>
      <el-form-item label="价格区间">
        <el-input-number v-model="searchForm.price_min" :min="0"></el-input-number>
        <span class="mx-2">-</span>
        <el-input-number v-model="searchForm.price_max" :min="0"></el-input-number>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">搜索</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const searchForm = ref({
  name: '',
  inventory: null,
  price_min: null,
  price_max: null
});

const emit = defineEmits(['search']);

const onSearch = () => {
  emit('search', searchForm.value);
};

const onReset = () => {
  searchForm.value = {
    name: '',
    inventory: null,
    price_min: null,
    price_max: null
  };
  emit('search', searchForm.value);
};
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
}
.mx-2 {
  margin: 0 8px;
}
</style> 