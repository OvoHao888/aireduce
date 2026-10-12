<template>
  <div class="logo-icon-wrapper">
    <svg viewBox="0 0 32 32" class="logo-svg">
      <defs>
        <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#e67e22;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#f39c12;stop-opacity:1" />
        </linearGradient>
      </defs>
      <!-- 笔的形状 -->
      <path 
        d="M4 28 L12 28 L16 20 L20 28 L28 28" 
        fill="none" 
        stroke="url(#logo-gradient)" 
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <path 
        d="M16 20 L16 8 L24 4" 
        fill="none" 
        stroke="url(#logo-gradient)" 
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <!-- 纸张形状 -->
      <rect 
        x="6" 
        y="12" 
        width="20" 
        height="14" 
        rx="2" 
        fill="none" 
        stroke="url(#logo-gradient)" 
        stroke-width="2"
      />
      <path 
        d="M10 16 L22 16 M10 20 L18 20" 
        fill="none" 
        stroke="url(#logo-gradient)" 
        stroke-width="1.5"
        stroke-linecap="round"
        opacity="0.6"
      />
    </svg>
  </div>
</template>

<script setup>
</script>

<style scoped>
.logo-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-svg {
  width: 2rem;
  height: 2rem;
}

@media (max-width: 768px) {
  .logo-svg {
    width: 1.5rem;
    height: 1.5rem;
  }
}
</style>
