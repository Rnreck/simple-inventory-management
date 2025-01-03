<template>
  <div class="product-table">
    <div class="table-header">
      <div class="left">
        <el-button v-if="isAdmin" type="primary" @click="openDialog">
          添加产品
        </el-button>
        <el-select
          v-model="selectedCategory"
          placeholder="选择分类"
          clearable
          @change="handleCategoryChange"
        >
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
      </div>
      <div class="right">
        <ShoppingCart />
      </div>
    </div>

    <!-- 查询表单 -->
    <div class="search-form">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="产品名称">
          <el-input v-model="searchForm.name" placeholder="请输入产品名称" clearable />
        </el-form-item>
        <el-form-item label="最小库存">
          <el-input-number v-model="searchForm.inventory" :min="0" placeholder="最小库存" />
        </el-form-item>
        <el-form-item label="价格区间">
          <el-input-number v-model="searchForm.price_min" :min="0" :precision="2" placeholder="最低价格" />
          <span class="mx-2">-</span>
          <el-input-number v-model="searchForm.price_max" :min="0" :precision="2" placeholder="最高价格" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="products" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="产品名称" />
      <el-table-column prop="category_name" label="分类" width="120" />
      <el-table-column prop="inventory" label="库存" width="100" />
      <el-table-column prop="price" label="价格" width="120">
        <template #default="scope">
          ¥{{ scope.row.price.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column label="操作" width="250" fixed="right">
        <template #default="scope">
          <el-button-group>
            <el-button size="small" @click="addToCart(scope.row)">
              加入购物车
            </el-button>
            <template v-if="isAdmin">
              <el-button size="small" @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleDelete(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingProduct.id ? '编辑产品' : '添加产品'"
    >
      <el-form :model="editingProduct" label-width="80px">
        <el-form-item label="产品名称">
          <el-input v-model="editingProduct.name" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="editingProduct.category_id" placeholder="选择分类">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="editingProduct.inventory" :min="0" />
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number
            v-model="editingProduct.price"
            :min="0"
            :precision="2"
            :step="0.1"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="editingProduct.description"
            type="textarea"
            rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { productsApi } from '../api/products';
import { useCartStore } from '../store/cart';
import ShoppingCart from './ShoppingCart.vue';
import { categoriesApi } from '../api/categories';

interface Product {
  id: number;
  name: string;
  category_id: number | null;
  category_name?: string;
  inventory: number;
  price: number;
  description?: string;
}

interface Category {
  id: number;
  name: string;
}

interface SearchForm {
  name: string;
  inventory: number | null;
  price_min: number | null;
  price_max: number | null;
  category_id: number | null;
}

const props = defineProps({
  products: {
    type: Array as () => Product[],
    required: true
  },
  isAdmin: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update', 'categoryChange']);

const dialogVisible = ref(false);
const editingProduct = ref<Product>({
  id: 0,
  name: '',
  category_id: null,
  inventory: 0,
  price: 0,
  description: ''
});

const cartStore = useCartStore();

const categories = ref<Category[]>([]);
const selectedCategory = ref<number | null>(null);

const searchForm = ref<SearchForm>({
  name: '',
  inventory: null,
  price_min: null,
  price_max: null,
  category_id: null
});

const loadCategories = async () => {
  try {
    const response = await categoriesApi.getCategories();
    categories.value = response.categories;
  } catch (error) {
    ElMessage.error('获取分类列表失败');
  }
};

const handleCategoryChange = (categoryId: number | null) => {
  emit('categoryChange', categoryId);
};

const handleEdit = (row: any) => {
  editingProduct.value = { ...row };
  dialogVisible.value = true;
};

const handleDelete = async (row: any) => {
  try {
    await productsApi.deleteProduct(row.id);
    ElMessage.success('删除成功');
    emit('update');
  } catch (error) {
    ElMessage.error('删除失败');
  }
};

const handleSave = async () => {
  try {
    if (editingProduct.value.id) {
      await productsApi.updateProduct(
        editingProduct.value.id,
        editingProduct.value
      );
    } else {
      await productsApi.addProduct(editingProduct.value);
    }
    dialogVisible.value = false;
    ElMessage.success('保存成功');
    emit('update');
  } catch (error) {
    ElMessage.error('保存失败');
  }
};

const openDialog = () => {
  editingProduct.value = {
    id: 0,
    name: '',
    category_id: null,
    inventory: 0,
    price: 0,
    description: ''
  };
  dialogVisible.value = true;
};

const addToCart = (product: any) => {
  if (product.inventory > 0) {
    cartStore.addToCart(product);
    ElMessage.success('已添加到购物车');
  } else {
    ElMessage.warning('商品库存不足');
  }
};

const handleSearch = async () => {
  try {
    const params: Partial<SearchForm> = { 
      ...searchForm.value,
      category_id: selectedCategory.value 
    };
    // 移除空值
    Object.keys(params).forEach((key) => {
      const k = key as keyof SearchForm;
      if (params[k] === null || params[k] === '') {
        delete params[k];
      }
    });
    const response = await productsApi.searchProducts(params);
    if (response.products) {
      emit('update', response.products);
    } else {
      ElMessage.warning('未找到匹配的产品');
    }
  } catch (error) {
    console.error('查询失败:', error);
    ElMessage.error('查询失败');
  }
};

const resetSearch = () => {
  searchForm.value = {
    name: '',
    inventory: null,
    price_min: null,
    price_max: null,
    category_id: null
  };
  selectedCategory.value = null;
  // 重置后重新获取所有产品
  productsApi.getProducts().then(response => {
    if (response.products) {
      emit('update', response.products);
    }
  }).catch(error => {
    console.error('重置查询失败:', error);
    ElMessage.error('重置查询失败');
  });
};

onMounted(() => {
  loadCategories();
});

defineExpose({
  openDialog
});
</script>

<style scoped>
.product-table {
  padding: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-form {
  margin: 20px 0;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.mx-2 {
  margin: 0 8px;
}

.el-form-item {
  margin-bottom: 0;
  margin-right: 20px;
}

.el-input-number {
  width: 120px;
}

.left {
  display: flex;
  gap: 16px;
  align-items: center;
}
</style> 