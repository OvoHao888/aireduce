<template>
  <div :class="['glass-card', { 'card-hover': hoverable }]" :style="customStyle">
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  hoverable: {
    type: Boolean,
    default: false
  },
  padding: {
    type: String,
    default: '24px'
  },
  borderRadius: {
    type: String,
    default: '16px'
  },
  blur: {
    type: String,
    default: '20px'
  },
  bg: {
    type: String,
    default: 'rgba(255, 255, 255, 0.75)'
  },
  shadow: {
    type: String,
    default: '0 8px 32px rgba(230, 126, 34, 0.1)'
  }
})

const customStyle = computed(() => ({
  padding: props.padding,
  borderRadius: props.borderRadius,
  backdropFilter: `blur(${props.blur})`,
  WebkitBackdropFilter: `blur(${props.blur})`,
  background: props.bg,
  boxShadow: props.shadow
}))
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(230, 126, 34, 0.1);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(230, 126, 34, 0.2);
}
</style>
