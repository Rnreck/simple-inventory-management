<template>
  <div class="category-list">
    <div class="header">
      <h3>分类管理</h3>
      <el-button
        v-if="isAdmin"
        type="primary"
        size="small"
        @click="showAddDialog"
      >
        添加分类
      </el-button>
    </div>

    <el-table :data="categories" style="width: 100%" size="small">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column label="操作" width="120" v-if="isAdmin">
        <template #default="scope">
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加分类对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="添加分类"
      width="30%"
    >
      <el-form :model="categoryForm" label-width="80px">
        <el-form-item label="分类名称">
          <el-input v-model="categoryForm.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAdd">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { categoriesApi } from '../api/categories';

const props = defineProps({
  isAdmin: {
    type: Boolean,
    default: false
  }
});

const categories = ref([]);
const dialogVisible = ref(false);
const categoryForm = ref({
  name: ''
});

const loadCategories = async () => {
  try {
    const response = await categoriesApi.getCategories();
    categories.value = response.categories;
  } catch (error) {
    ElMessage.error('获取分类列表失败');
  }
};

const showAddDialog = () => {
  categoryForm.value.name = '';
  dialogVisible.value = true;
};

const handleAdd = async () => {
  try {
    await categoriesApi.createCategory(categoryForm.value);
    ElMessage.success('添加分类成功');
    dialogVisible.value = false;
    loadCategories();
  } catch (error) {
    ElMessage.error('添加分类失败');
  }
};

const handleDelete = async (category: any) => {
  try {
    await categoriesApi.deleteCategory(category.id);
    ElMessage.success('删除分类成功');
    loadCategories();
  } catch (error) {
    ElMessage.error('删除分类失败');
  }
};

onMounted(() => {
  loadCategories();
});
</script>

<style scoped>
.category-list {
  margin-top: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

h3 {
  margin: 0;
}
</style> 