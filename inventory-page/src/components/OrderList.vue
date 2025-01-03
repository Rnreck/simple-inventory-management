<template>
  <div class="order-list">
    <el-table
      v-loading="loading"
      :data="orders"
      style="width: 100%"
      :empty-text="emptyText"
      border
    >
      <el-table-column prop="id" label="订单ID" width="80" align="center" />
      <el-table-column prop="total_amount" label="总金额" width="120" align="right">
        <template #default="scope">
          <span class="price">¥{{ Number(scope.row.total_amount).toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="items_count" label="商品数量" width="100" align="center">
        <template #default="scope">
          <el-tag size="small" effect="plain">{{ scope.row.items_count }}件</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100" align="center">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" align="center">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200" align="center">
        <template #default="scope">
          <el-button-group>
            <el-button 
              size="small"
              type="primary"
              plain
              @click="showOrderDetails(scope.row)"
            >
              查看详情
            </el-button>
            <el-button 
              v-if="isAdmin && scope.row.status === 'pending'"
              size="small"
              type="success"
              @click="handleComplete(scope.row)"
            >
              完成订单
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 订单详情对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      title="订单详情" 
      width="600px"
      destroy-on-close
    >
      <div v-loading="detailsLoading">
        <el-descriptions :column="1" border v-if="currentOrder">
          <el-descriptions-item label="订单ID">{{ currentOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(currentOrder.status)">
              {{ getStatusText(currentOrder.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="总金额">
            <span class="price">¥{{ Number(currentOrder.total_amount).toFixed(2) }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="商品数量">
            {{ currentOrder.items_count }}件
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDate(currentOrder.created_at) }}
          </el-descriptions-item>
        </el-descriptions>

        <h4 class="items-title">订单商品明细</h4>
        <el-table :data="currentOrder?.items || []" style="width: 100%" border>
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="product_name" label="商品名称" min-width="120" />
          <el-table-column prop="quantity" label="数量" width="80" align="center" />
          <el-table-column prop="price" label="单价" width="120" align="right">
            <template #default="scope">
              <span class="price">¥{{ Number(scope.row.price).toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="小计" width="120" align="right">
            <template #default="scope">
              <span class="price">¥{{ (Number(scope.row.price) * scope.row.quantity).toFixed(2) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { ordersApi } from '../api/orders';

const props = defineProps({
  orders: {
    type: Array,
    required: true
  },
  isAdmin: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update']);

const loading = ref(false);
const detailsLoading = ref(false);
const dialogVisible = ref(false);
const currentOrder = ref<any>(null);

const emptyText = computed(() => {
  return loading.value ? '加载中...' : '暂无数据';
});

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'warning',
    completed: 'success',
    cancelled: 'danger'
  };
  return types[status] || 'info';
};

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待处理',
    completed: '已完成',
    cancelled: '已取消'
  };
  return texts[status] || status;
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

const showOrderDetails = async (order: any) => {
  detailsLoading.value = true;
  try {
    // 如果需要获取详细信息，可以在这里调用API
    currentOrder.value = { ...order };
  } catch (error) {
    ElMessage.error('获取订单详情失败');
    console.error('Error loading order details:', error);
  } finally {
    detailsLoading.value = false;
    dialogVisible.value = true;
  }
};

const handleComplete = async (order: any) => {
  loading.value = true;
  try {
    await ordersApi.updateOrderStatus(order.id, 'completed');
    ElMessage.success('订单已完成');
    emit('update');
  } catch (error) {
    ElMessage.error('操作失败');
    console.error('Error completing order:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.order-list {
  margin-top: 20px;
}

.items-title {
  margin: 20px 0 10px;
  color: #606266;
  font-weight: bold;
}

:deep(.el-descriptions) {
  margin-bottom: 20px;
}

:deep(.el-button-group) {
  display: flex;
  gap: 8px;
}

.price {
  font-family: monospace;
  color: #67c23a;
  font-weight: bold;
}

:deep(.el-tag) {
  text-transform: capitalize;
}

:deep(.el-descriptions__label) {
  width: 120px;
  justify-content: flex-end;
}
</style> 