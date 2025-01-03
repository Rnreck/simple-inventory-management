<template>
  <div class="shopping-cart">
    <el-popover
      placement="bottom"
      :width="400"
      trigger="click"
      popper-class="cart-popover"
    >
      <template #reference>
        <el-badge :value="cartStore.itemCount" :hidden="cartStore.itemCount === 0">
          <el-button type="primary" :icon="ShoppingCart">
            购物车
          </el-button>
        </el-badge>
      </template>

      <div class="cart-content">
        <div v-if="cartStore.items.length === 0" class="empty-cart">
          购物车是空的
        </div>
        <template v-else>
          <el-table :data="cartStore.items" size="small">
            <el-table-column prop="product_name" label="商品" />
            <el-table-column prop="price" label="单价" width="80">
              <template #default="scope">
                ¥{{ scope.row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="数量" width="120">
              <template #default="scope">
                <el-input-number
                  v-model="scope.row.quantity"
                  :min="1"
                  size="small"
                  @change="(val) => updateQuantity(scope.row.product_id, val)"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="60">
              <template #default="scope">
                <el-button
                  type="danger"
                  size="small"
                  circle
                  :icon="Delete"
                  @click="removeItem(scope.row.product_id)"
                />
              </template>
            </el-table-column>
          </el-table>

          <div class="cart-footer">
            <div class="total">
              总计: ¥{{ cartStore.total.toFixed(2) }}
            </div>
            <el-button type="primary" @click="checkout">
              结算
            </el-button>
          </div>
        </template>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ShoppingCart, Delete } from '@element-plus/icons-vue';
import { useCartStore } from '../store/cart';
import { ordersApi } from '../api/orders';
import { ElMessage } from 'element-plus';

const cartStore = useCartStore();

const updateQuantity = (productId: number, quantity: number) => {
  cartStore.updateQuantity(productId, quantity);
};

const removeItem = (productId: number) => {
  cartStore.removeFromCart(productId);
};

const checkout = async () => {
  try {
    const orderData = {
      items: cartStore.items.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity
      }))
    };

    await ordersApi.createOrder(orderData);
    ElMessage.success('订单创建成功');
    cartStore.clearCart();
  } catch (error) {
    ElMessage.error('创建订单失败');
  }
};
</script>

<style scoped>
.shopping-cart {
  margin-left: 16px;
}

.cart-content {
  padding: 8px;
}

.empty-cart {
  text-align: center;
  padding: 20px;
  color: #999;
}

.cart-footer {
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total {
  font-size: 16px;
  font-weight: bold;
}
</style> 