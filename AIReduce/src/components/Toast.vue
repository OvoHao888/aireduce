<template>
  <Teleport to="body">
    <div class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`, { enter: toast.enter, leave: toast.leave }]"
      >
        <span class="toast-icon">{{ getIcon(toast.type) }}</span>
        <span class="toast-message">{{ toast.message }}</span>
        <button class="toast-close" @click="removeToast(toast.id)">✕</button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { onUnmounted } from 'vue'
import { toasts, removeToast, getIcon, cleanup } from '../utils/toast'

onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  max-width: 400px;
  opacity: 0;
  transform: translateX(100%);
  transition: all 0.3s ease;
}

.toast.enter {
  opacity: 1;
  transform: translateX(0);
}

.toast.leave {
  opacity: 0;
  transform: translateX(100%);
}

.toast-success {
  border-left: 4px solid #22c55e;
}

.toast-error {
  border-left: 4px solid #ef4444;
}

.toast-warning {
  border-left: 4px solid #f59e0b;
}

.toast-info {
  border-left: 4px solid #3b82f6;
}

.toast-icon {
  font-size: 1.3rem;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  font-size: 0.95rem;
  color: var(--text-primary);
  line-height: 1.5;
}

.toast-close {
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--text-secondary);
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.08);
}

@media (max-width: 640px) {
  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
  }

  .toast {
    min-width: auto;
    max-width: none;
  }
}
</style>
