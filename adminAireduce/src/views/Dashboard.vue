<template>
  <div class="dashboard">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>
    
    <!-- 错误提示 -->
    <div v-if="error" class="error">{{ error }}</div>
    
    <!-- 统计卡片 -->
    <div v-else class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-label">总用户数</div>
          <div class="stat-value">{{ stats.total_users || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💎</div>
        <div class="stat-info">
          <div class="stat-label">会员用户</div>
          <div class="stat-value">{{ stats.vip_users || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🎫</div>
        <div class="stat-info">
          <div class="stat-label">总卡密数</div>
          <div class="stat-value">{{ stats.total_cards || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <div class="stat-label">已使用卡密</div>
          <div class="stat-value">{{ stats.used_cards || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <div class="stat-label">使用次数</div>
          <div class="stat-value">{{ stats.total_uses || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-info">
          <div class="stat-label">反馈数量</div>
          <div class="stat-value">{{ stats.total_feedbacks || 0 }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { statsAPI } from '../utils/adminApi.js'

export default {
  name: 'Dashboard',
  setup() {
    const loading = ref(true)
    const error = ref('')
    const stats = ref({})

    const fetchStats = async () => {
      loading.value = true
      error.value = ''
      try {
        stats.value = await statsAPI.getStats()
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchStats()
    })

    return {
      loading,
      error,
      stats
    }
  }
}
</script>

<style scoped>
.dashboard {
  width: 100%;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #666;
}

.error {
  color: #e74c3c;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.15);
}

.stat-icon {
  font-size: 40px;
  margin-right: 16px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.1), rgba(243, 156, 18, 0.1));
  border-radius: 14px;
}

.stat-info {
  flex: 1;
}

.stat-label {
  color: #888;
  font-size: 14px;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #e67e22;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>