<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="gradient-text">管理后台</h2>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <span class="nav-icon">📊</span>
          <span>统计概览</span>
        </router-link>
        <router-link to="/users" class="nav-item" active-class="active">
          <span class="nav-icon">👥</span>
          <span>用户管理</span>
        </router-link>
        <router-link to="/cards" class="nav-item" active-class="active">
          <span class="nav-icon">🎫</span>
          <span>卡密管理</span>
        </router-link>
        <router-link to="/products" class="nav-item" active-class="active">
          <span class="nav-icon">📦</span>
          <span>套餐管理</span>
        </router-link>
        <router-link to="/records" class="nav-item" active-class="active">
          <span class="nav-icon">📝</span>
          <span>使用记录</span>
        </router-link>
        <router-link to="/feedbacks" class="nav-item" active-class="active">
          <span class="nav-icon">💬</span>
          <span>反馈管理</span>
        </router-link>
        <router-link to="/api-config" class="nav-item" active-class="active">
          <span class="nav-icon">⚙️</span>
          <span>API配置</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <header class="content-header">
        <h1>{{ pageTitle }}</h1>
      </header>
      <div class="content-body">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'AdminLayout',
  setup() {
    const route = useRoute()
    const router = useRouter()

    const pageTitle = computed(() => {
      const titles = {
        '/': '统计概览',
        '/users': '用户管理',
        '/cards': '卡密管理',
        '/products': '套餐管理',
        '/records': '使用记录',
        '/feedbacks': '反馈管理',
        '/api-config': 'API配置'
      }
      return titles[route.path] || '管理后台'
    })

    const handleLogout = () => {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('token')
      localStorage.removeItem('admin_user')
      localStorage.removeItem('user')
      localStorage.removeItem('isLoggedIn')
      window.location.href = '/'
    }

    return {
      pageTitle,
      handleLogout
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #fdfbf7 0%, #faf5ef 50%, #fdf6e3 100%);
}

.sidebar {
  width: 240px;
  background: #fff;
  box-shadow: 2px 0 10px rgba(230, 126, 34, 0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(230, 126, 34, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
  margin: 4px 12px;
  border-radius: 10px;
}

.nav-item:hover {
  background: rgba(230, 126, 34, 0.08);
  color: #e67e22;
}

.nav-item.active {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: #fff;
  box-shadow: 0 4px 15px rgba(230, 126, 34, 0.3);
}

.nav-icon {
  margin-right: 12px;
  font-size: 18px;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(230, 126, 34, 0.1);
}

.logout-btn {
  width: 100%;
  padding: 12px;
  background: transparent;
  border: 2px solid #e67e22;
  color: #e67e22;
  cursor: pointer;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #e67e22;
  color: #fff;
}

.main-content {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
}

.content-header {
  background: #fff;
  padding: 20px 30px;
  border-bottom: 2px solid rgba(230, 126, 34, 0.1);
}

.content-header h1 {
  margin: 0;
  font-size: 24px;
  color: #2c3e50;
  font-weight: 600;
}

.content-body {
  flex: 1;
  padding: 24px;
}

/* 统一表格样式 */
:deep(.data-table) {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(230, 126, 34, 0.08);
  table-layout: auto;
}

:deep(.data-table th) {
  background: linear-gradient(135deg, #fdfbf7, #faf5ef);
  color: #e67e22;
  font-weight: 600;
  padding: 14px 16px;
  text-align: left;
  border-bottom: 2px solid rgba(230, 126, 34, 0.1);
}

:deep(.data-table td) {
  padding: 14px 16px;
  color: #666;
  border-bottom: 1px solid rgba(230, 126, 34, 0.08);
  min-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.data-table tr:hover) {
  background: rgba(230, 126, 34, 0.03);
}

/* 统一按钮样式 */
:deep(.btn) {
  padding: 10px 18px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

:deep(.btn-primary) {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: #fff;
}

:deep(.btn-primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(230, 126, 34, 0.3);
}

:deep(.btn-link) {
  background: none;
  color: #e67e22;
  padding: 6px 12px;
}

:deep(.btn-link:hover) {
  background: rgba(230, 126, 34, 0.1);
  border-radius: 6px;
}

:deep(.btn-link.danger) {
  color: #e74c3c;
}

:deep(.btn-link.danger:hover) {
  background: rgba(231, 76, 60, 0.1);
}

/* 状态徽章 */
:deep(.status-badge) {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

:deep(.status-badge.vip),
:deep(.status-badge.active),
:deep(.status-badge.replied) {
  background: rgba(230, 126, 34, 0.15);
  color: #e67e22;
}

:deep(.status-badge.normal),
:deep(.status-badge.inactive),
:deep(.status-badge.pending) {
  background: #f5f5f5;
  color: #999;
}

:deep(.status-badge.used) {
  background: rgba(243, 156, 18, 0.15);
  color: #f39c12;
}

/* 分页 */
:deep(.pagination) {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
}

:deep(.pagination button) {
  padding: 10px 18px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  background: #fff;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #e67e22;
  font-weight: 600;
}

:deep(.pagination button:hover:not(:disabled)) {
  background: rgba(230, 126, 34, 0.1);
  border-color: #e67e22;
}

:deep(.pagination button:disabled) {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 弹窗 */
:deep(.modal-overlay) {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

:deep(.modal) {
  background: #fff;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(230, 126, 34, 0.2);
}

:deep(.modal-header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid rgba(230, 126, 34, 0.1);
}

:deep(.modal-header h3) {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
  font-weight: 600;
}

:deep(.modal-header .close-btn) {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #999;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

:deep(.modal-header .close-btn:hover) {
  background: rgba(230, 126, 34, 0.1);
  color: #e67e22;
}

:deep(.modal-body) {
  padding: 24px;
}

:deep(.modal-footer) {
  padding: 16px 24px;
  border-top: 1px solid rgba(230, 126, 34, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.form-group) {
  margin-bottom: 16px;
}

:deep(.form-group label) {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
}

:deep(.form-group input),
:deep(.form-group select),
:deep(.form-group textarea) {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
}

:deep(.form-group input:focus),
:deep(.form-group select:focus),
:deep(.form-group textarea:focus) {
  border-color: #e67e22;
  box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.1);
}

/* 工具栏 */
:deep(.toolbar) {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
}

:deep(.search-input) {
  padding: 12px 16px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 10px;
  width: 260px;
  font-size: 14px;
}

:deep(.search-input:focus) {
  border-color: #e67e22;
  outline: none;
}

/* 加载和错误状态 */
:deep(.loading),
:deep(.error),
:deep(.empty) {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 14px;
}

:deep(.error) {
  color: #e74c3c;
}

/* 代码单元格 */
:deep(.code-cell) {
  font-family: 'Consolas', monospace;
  color: #e67e22;
  font-weight: 500;
}

/* 内容框 */
:deep(.content-box) {
  background: rgba(230, 126, 34, 0.05);
  padding: 14px;
  border-radius: 10px;
  max-height: 180px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
  font-size: 13px;
  color: #555;
}

:deep(.reply-box) {
  background: rgba(230, 126, 34, 0.1);
}

/* 复选框 */
:deep(.checkbox-label) {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
}

:deep(.checkbox-label input[type="checkbox"]) {
  width: 18px;
  height: 18px;
  accent-color: #e67e22;
}
</style>