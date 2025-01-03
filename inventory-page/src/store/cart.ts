import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

interface CartItem {
  product_id: number;
  product_name: string;
  quantity: number;
  price: number;
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([]);

  const total = computed(() => {
    return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0);
  });

  const itemCount = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantity, 0);
  });

  function addToCart(product: any, quantity: number = 1) {
    const existingItem = items.value.find(item => item.product_id === product.id);
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      items.value.push({
        product_id: product.id,
        product_name: product.name,
        quantity,
        price: product.price
      });
    }
  }

  function removeFromCart(productId: number) {
    const index = items.value.findIndex(item => item.product_id === productId);
    if (index > -1) {
      items.value.splice(index, 1);
    }
  }

  function clearCart() {
    items.value = [];
  }

  function updateQuantity(productId: number, quantity: number) {
    const item = items.value.find(item => item.product_id === productId);
    if (item) {
      item.quantity = quantity;
    }
  }

  return {
    items,
    total,
    itemCount,
    addToCart,
    removeFromCart,
    clearCart,
    updateQuantity
  };
}); 