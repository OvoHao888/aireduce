<template>
  <header class="app-header glass">
    <div class="header-left">
      <div class="logo" @click="goHome">
        <img src="/favicon.png" alt="迅文" class="logo-image">
        <span class="logo-text">迅文</span>
      </div>
    </div>

    <nav class="header-nav">
      <router-link to="/workspace" class="nav-item" active-class="active">
        <span class="nav-icon">🏠</span>
        <span class="nav-text">工作台</span>
      </router-link>
      <router-link to="/token-card" class="nav-item" active-class="active">
        <span class="nav-icon">💎</span>
        <span class="nav-text">密卡中心</span>
      </router-link>
      <router-link to="/records" class="nav-item" active-class="active">
        <span class="nav-icon">📊</span>
        <span class="nav-text">使用记录</span>
      </router-link>
    </nav>

    <div class="header-right">
      <div class="user-dropdown">
        <div class="user-info glass" @click="goPersonal">
          <div class="avatar">
            {{ userAvatar }}
          </div>
          <div class="user-details">
            <div class="username">{{ username }}</div>
            <div class="user-balance">
              <span class="balance-icon">🎫</span>
              <span class="balance-text">{{ remainingTime }}</span>
            </div>
          </div>
        </div>
        <button class="logout-btn" @click="logout" title="退出登录">
          <span class="logout-icon">&#x1F6AA;</span>
          <span class="logout-text">退出</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../utils/api'

const router = useRouter()

const username = ref('游客用户')
const expireDate = ref('2026-12-31 23:59:59')

const userAvatar = computed(() => {
  return username.value.charAt(0).toUpperCase()
})

const remainingTime = computed(() => {
  const expire = new Date(expireDate.value)
  const now = new Date()
  
  if (isNaN(expire.getTime())) {
    return '会员已过期'
  }
  
  const diff = expire.getTime() - now.getTime()
  
  if (diff <= 0) {
    return '会员已过期'
  }
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  
  if (days > 30) {
    const months = Math.floor(days / 30)
    return `${months}个月${days % 30}天`
  } else if (days > 0) {
    return `${days}天${hours}小时`
  } else {
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    return `${hours}小时${minutes}分钟`
  }
})

const isAuthPage = () => {
  const publicPages = ['/login', '/register', '/']
  return publicPages.includes(window.location.pathname)
}

const loadUserInfo = async () => {
  // 公共页面不请求用户信息，避免循环跳转
  if (isAuthPage()) return

  // 无 token 时直接用本地数据
  const token = localStorage.getItem('token')
  if (!token) {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        username.value = user.username || '游客用户'
        expireDate.value = user.expireDate || '2026-12-31 23:59:59'
      } catch (e) {}
    }
    return
  }

  try {
    const userData = await authAPI.getMe()
    username.value = userData.username || '游客用户'
    expireDate.value = userData.expire_date || ''

    const userStr = localStorage.getItem('user')
    if (userStr) {
      const user = JSON.parse(userStr)
      user.username = username.value
      user.expireDate = expireDate.value
      localStorage.setItem('user', JSON.stringify(user))
    }
  } catch (error) {
    // 401 等错误已在 api.js 中统一处理跳转，此处静默忽略
  }
}

const handleStorageChange = (e) => {
  if (e.key === 'user') {
    loadUserInfo()
  }
}

window.addEventListener('storage', handleStorageChange)

const goHome = () => {
  router.push('/')
}

const goPersonal = () => {
  router.push('/personal')
}

const logout = () => {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('isLoggedIn')
    router.push('/login')
  }
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  z-index: 1000;
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-top: none;
}

.header-left {
  flex: 0 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-image {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 8px;
  object-fit: contain;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-nav {
  display: flex;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 500;
  transition: all 0.3s ease;
  background: transparent;
}

.nav-item:hover {
  background: rgba(230, 126, 34, 0.1);
  transform: translateY(-2px);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.15), rgba(243, 156, 18, 0.15));
  color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(230, 126, 34, 0.2);
}

.nav-icon {
  font-size: 1.2rem;
}

.header-right {
  flex: 0 0 auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  background: rgba(255, 255, 255, 0.5);
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.15);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(230, 126, 34, 0.3);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.username {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.user-balance {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-left: 16px;
  border-left: 1px solid rgba(0, 0, 0, 0.08);
}

.balance-icon {
  font-size: 0.9rem;
}

.balance-text {
  color: var(--primary-color);
  font-weight: 600;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  font-size: 0.9rem;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.logout-icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 16px;
  }

  .nav-text {
    display: none;
  }

  .user-details {
    display: none;
  }

  .logo-text {
    font-size: 1.2rem;
  }

  .logout-text {
    display: none;
  }

  .logout-btn {
    padding: 10px 12px;
  }
}
</style>
