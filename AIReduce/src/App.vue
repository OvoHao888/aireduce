<template>
  <div class="app-layout">
    <ParticleBackground v-if="showBackground" />
    <AppHeader v-if="showHeader" />
    <main class="main-content" :class="{ 'landing-content': !showHeader }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Toast />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ParticleBackground from './components/ParticleBackground.vue'
import AppHeader from './components/AppHeader.vue'
import Toast from './components/Toast.vue'

const router = useRouter()
const showHeader = ref(false)
const showBackground = ref(false)

const updateLayout = () => {
  const currentName = router.currentRoute.value.name
  const authPages = ['LoginPage', 'RegisterPage']
  showHeader.value = !authPages.includes(currentName) && currentName !== 'LandingPage'
  showBackground.value = currentName !== 'LoginPage' && currentName !== 'RegisterPage'
}

onMounted(() => {
  updateLayout()
})

watch(
  () => router.currentRoute.value.name,
  () => {
    updateLayout()
  }
)
</script>

<style scoped>
.app-layout {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, #fdf6e3 0%, #fef9f3 50%, #fff8f0 100%);
}

.main-content {
  position: relative;
  z-index: 1;
  padding-top: 90px;
  padding-bottom: 40px;
  min-height: 100vh;
}

.main-content.landing-content {
  padding-top: 0;
  padding-bottom: 0;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
