<template>
  <div class="personal-container">
    <div class="container">
      <!-- 用户信息卡片 -->
      <GlassCard class="user-profile-card" padding="32px">
        <div class="profile-header">
          <div class="avatar-large">
            {{ userAvatar }}
          </div>
          <div class="profile-info">
            <h1 class="username">{{ username }}</h1>
            <p class="user-email">{{ email }}</p>
            <div class="user-badges">
              <span v-if="hasMembership" class="badge">✨ 正式会员</span>
              <span v-if="hasMembership" class="badge vip">💎 VIP用户</span>
              <span v-else class="badge expired">⚠️ 会员已过期</span>
            </div>
          </div>
          <button class="btn-edit" @click="showSettingsModal = true">
            ✏️ 编辑资料
          </button>
        </div>

        <div class="profile-stats">
          <div class="stat-card">
            <div class="stat-icon">🎫</div>
            <div class="stat-value">{{ remainingDays > 0 ? `${remainingDays}天` : `${remainingHours}小时` }}</div>
            <div class="stat-label">会员剩余时长</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📄</div>
            <div class="stat-value">{{ totalUsage }}</div>
            <div class="stat-label">累计使用次数</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📅</div>
            <div class="stat-value">{{ usedDays }}</div>
            <div class="stat-label">使用天数</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⭐</div>
            <div class="stat-value">{{ memberLevel }}</div>
            <div class="stat-label">会员等级</div>
          </div>
        </div>
      </GlassCard>

      <!-- 快捷操作 -->
      <GlassCard class="quick-actions-card" padding="24px">
        <h2 class="section-title">🚀 快捷操作</h2>
        <div class="action-grid">
          <div class="action-item" @click="goToTokenCard">
            <div class="action-icon">💎</div>
            <div class="action-text">购买密卡</div>
          </div>
          <div class="action-item" @click="goToRecords">
            <div class="action-icon">📊</div>
            <div class="action-text">使用记录</div>
          </div>
          <div class="action-item" @click="showHelp">
            <div class="action-icon">❓</div>
            <div class="action-text">使用帮助</div>
          </div>
          <div class="action-item" @click="showFeedbackDialog">
            <div class="action-icon">💬</div>
            <div class="action-text">意见反馈</div>
          </div>
        </div>
      </GlassCard>

      <!-- 账户设置弹窗 -->
      <Teleport to="body">
        <div v-if="showSettingsModal" class="modal-overlay" @click.self="showSettingsModal = false">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title">⚙️ 账户设置</h2>
              <button class="modal-close" @click="showSettingsModal = false">✕</button>
            </div>
            <div class="modal-body">
              <div class="settings-section">
                <h3 class="subsection-title">基本信息</h3>
                <div class="setting-item">
                  <label>用户名</label>
                  <input v-model="username" type="text" class="input-field" />
                </div>
                <div class="setting-item">
                  <label>邮箱地址</label>
                  <input v-model="email" type="email" class="input-field" />
                </div>
              </div>

              <div class="settings-section">
                <h3 class="subsection-title">安全设置</h3>
                <div class="setting-item">
                  <label>修改密码</label>
                  <button class="btn btn-outline" @click="changePassword">修改密码</button>
                </div>
                <div class="setting-item">
                  <label>两步验证</label>
                  <button class="btn btn-outline">启用验证</button>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showSettingsModal = false">取消</button>
              <button class="btn btn-primary" @click="saveSettings">保存设置</button>
            </div>
          </div>
        </div>
      </Teleport>

      <!-- 修改密码弹窗 -->
      <Teleport to="body">
        <div v-if="showPasswordModal" class="modal-overlay" @click.self="showPasswordModal = false">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title">🔐 修改密码</h2>
              <button class="modal-close" @click="showPasswordModal = false">✕</button>
            </div>
            <div class="modal-body">
              <div class="setting-item" style="flex-direction: column; align-items: flex-start;">
                <label style="margin-bottom: 8px;">原密码</label>
                <input v-model="oldPassword" type="password" class="input-field" style="width: 100%;" />
              </div>
              <div class="setting-item" style="flex-direction: column; align-items: flex-start;">
                <label style="margin-bottom: 8px;">新密码</label>
                <input v-model="newPassword" type="password" class="input-field" style="width: 100%;" />
              </div>
              <div class="setting-item" style="flex-direction: column; align-items: flex-start;">
                <label style="margin-bottom: 8px;">确认密码</label>
                <input v-model="confirmPassword" type="password" class="input-field" style="width: 100%;" />
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showPasswordModal = false">取消</button>
              <button class="btn btn-primary" @click="submitPasswordChange">确认修改</button>
            </div>
          </div>
        </div>
      </Teleport>

      <!-- 意见反馈弹窗 -->
      <Teleport to="body">
        <div v-if="showFeedbackModal" class="modal-overlay" @click.self="showFeedbackModal = false">
          <div class="modal-content">
            <div class="modal-header">
              <h2 class="modal-title">💬 意见反馈</h2>
              <button class="modal-close" @click="showFeedbackModal = false">✕</button>
            </div>
            <div class="modal-body">
              <div class="setting-item" style="flex-direction: column; align-items: flex-start;">
                <label style="margin-bottom: 8px;">反馈类型</label>
                <select v-model="feedbackType" class="input-field" style="width: 100%;">
                  <option value="suggestion">功能建议</option>
                  <option value="bug">问题反馈</option>
                  <option value="complaint">投诉建议</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="setting-item" style="flex-direction: column; align-items: flex-start;">
                <label style="margin-bottom: 8px;">反馈内容</label>
                <textarea v-model="feedbackContent" class="input-field" style="width: 100%; height: 120px; resize: vertical;" placeholder="请详细描述您的问题或建议..."></textarea>
              </div>
              <div class="setting-item" style="flex-direction: column; align-items: flex-start;">
                <label style="margin-bottom: 8px;">联系方式（选填）</label>
                <input v-model="feedbackContact" type="text" class="input-field" style="width: 100%;" placeholder="邮箱或微信" />
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showFeedbackModal = false">取消</button>
              <button class="btn btn-primary" @click="submitFeedback">提交反馈</button>
            </div>
          </div>
        </div>
      </Teleport>

      <!-- VIP特权 -->
      <GlassCard class="vip-card" padding="24px">
        <div class="vip-header">
          <div class="vip-title">
            <span class="vip-icon">💎</span>
            <h2>VIP特权</h2>
          </div>
          <button class="btn btn-vip" @click="goToTokenCard">
            升级VIP
          </button>
        </div>

        <div class="vip-benefits">
          <div class="benefit-item">
            <span class="benefit-icon">✅</span>
            <span class="benefit-text">无限次使用降重功能</span>
          </div>
          <div class="benefit-item">
            <span class="benefit-icon">✅</span>
            <span class="benefit-text">优先使用最新AI模型</span>
          </div>
          <div class="benefit-item">
            <span class="benefit-icon">✅</span>
            <span class="benefit-text">专属客服支持</span>
          </div>
          <div class="benefit-item">
            <span class="benefit-icon">✅</span>
            <span class="benefit-text">批量处理功能</span>
          </div>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GlassCard from '../components/GlassCard.vue'
import { authAPI, tokenAPI, feedbackAPI } from '../utils/api'
import { showToast } from '../utils/toast'

const router = useRouter()

const username = ref('尊贵的用户')
const email = ref('user@example.com')
const balance = ref(0)
const totalUsage = ref(0)
const usedDays = ref(0)
const vipDays = ref(0)
const expireDate = ref('')
const memberLevelValue = ref('')
const isLoading = ref(false)

const showFeedbackModal = ref(false)
const feedbackContent = ref('')
const feedbackType = ref('suggestion')
const feedbackContact = ref('')

const showPasswordModal = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const userAvatar = computed(() => {
  return username.value.charAt(0).toUpperCase()
})

const hasMembership = computed(() => {
  if (!expireDate.value) return false
  const expire = new Date(expireDate.value)
  const now = new Date()
  return expire.getTime() > now.getTime()
})

const remainingDays = computed(() => {
  if (!expireDate.value) return 0
  const expire = new Date(expireDate.value)
  const now = new Date()
  const diff = expire.getTime() - now.getTime()
  if (diff <= 0) return 0
  return Math.floor(diff / (1000 * 60 * 60 * 24))
})

const remainingHours = computed(() => {
  if (!expireDate.value) return 0
  const expire = new Date(expireDate.value)
  const now = new Date()
  const diff = expire.getTime() - now.getTime()
  if (diff <= 0) return 0
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  return days * 24 + hours
})

const memberLevel = computed(() => {
  if (!hasMembership.value) return '普通用户'
  const days = remainingDays.value
  if (days >= 365) return 'VIP3'
  if (days >= 180) return 'VIP2'
  if (days >= 30) return 'VIP1'
  return '普通会员'
})

const loadUserInfo = async () => {
  isLoading.value = true
  try {
    const userData = await authAPI.getMe()
    username.value = userData.username || '尊贵的用户'
    email.value = userData.email || 'user@example.com'
    expireDate.value = userData.expire_date || ''
    totalUsage.value = userData.total_usage || 0
    memberLevelValue.value = userData.member_level || ''
  } catch (error) {
    console.error('加载用户信息失败:', error)
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        username.value = user.username || '尊贵的用户'
        email.value = user.email || 'user@example.com'
        balance.value = user.balance || 0
        expireDate.value = user.expireDate || ''
      } catch (e) {
        console.error('Failed to parse user info')
      }
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadUserInfo()
})

const goToTokenCard = () => {
  router.push('/token-card')
}

const goToRecords = () => {
  router.push('/records')
}

const showHelp = () => {
  showToast('帮助文档正在开发中...', 'info')
}

const showFeedbackDialog = () => {
  showFeedbackModal.value = true
}

const submitFeedback = async () => {
  if (!feedbackContent.value || feedbackContent.value.trim().length < 5) {
    showToast('反馈内容不能少于5个字符', 'error')
    return
  }

  try {
    await feedbackAPI.createFeedback({
      content: feedbackContent.value,
      type: feedbackType.value,
      contact: feedbackContact.value
    })
    showToast('反馈提交成功！', 'success')
    feedbackContent.value = ''
    feedbackContact.value = ''
    feedbackType.value = 'suggestion'
    showFeedbackModal.value = false
  } catch (error) {
    showToast(error.message || '提交反馈失败', 'error')
  }
}

const showSettingsModal = ref(false)

const saveSettings = async () => {
  if (!username.value || username.value.trim().length < 2) {
    showToast('用户名长度不能少于2位', 'error')
    return
  }

  try {
    const response = await authAPI.updateProfile({
      username: username.value,
      email: email.value
    })

    const userStr = localStorage.getItem('user')
    if (userStr) {
      const user = JSON.parse(userStr)
      user.username = username.value
      user.email = email.value
      localStorage.setItem('user', JSON.stringify(user))
    }

    window.dispatchEvent(new Event('storage'))

    showToast('设置已保存', 'success')
    showSettingsModal.value = false
  } catch (error) {
    showToast(error.message || '保存失败', 'error')
  }
}

const changePassword = () => {
  showPasswordModal.value = true
}

const submitPasswordChange = async () => {
  if (!oldPassword.value) {
    showToast('请输入原密码', 'error')
    return
  }

  if (!newPassword.value || newPassword.value.length < 6) {
    showToast('新密码长度不能少于6位', 'error')
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    showToast('两次输入的密码不一致', 'error')
    return
  }

  try {
    await authAPI.changePassword(oldPassword.value, newPassword.value)
    showToast('密码修改成功', 'success')
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    showPasswordModal.value = false
  } catch (error) {
    showToast(error.message || '修改密码失败', 'error')
  }
}
</script>

<style scoped>
.personal-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}

.container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.user-profile-card {
  grid-column: 1 / -1;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 32px;
}

.avatar-large {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 2.5rem;
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.3);
}

.profile-info {
  flex: 1;
}

.username {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.user-email {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.user-badges {
  display: flex;
  gap: 12px;
}

.badge {
  padding: 6px 16px;
  background: rgba(230, 126, 34, 0.1);
  color: var(--primary-color);
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 20px;
}

.badge.vip {
  background: linear-gradient(135deg, #e74c3c, #fd79a8);
  color: white;
}

.badge.expired {
  background: rgba(149, 165, 166, 0.2);
  color: var(--text-secondary);
  border: 1px solid rgba(149, 165, 166, 0.3);
}

.btn-edit {
  padding: 12px 24px;
  background: white;
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-edit:hover {
  background: rgba(230, 126, 34, 0.05);
  transform: translateY(-2px);
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-card {
  padding: 24px;
  background: white;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(230, 126, 34, 0.08);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.15);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.quick-actions-card {
  grid-column: 1 / -1;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.action-item {
  padding: 24px;
  background: white;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(230, 126, 34, 0.08);
}

.action-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.15);
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.05), rgba(243, 156, 18, 0.05));
}

.action-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.action-text {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.settings-card {
  grid-column: 1 / -1;
}

.settings-section {
  margin-bottom: 32px;
}

.subsection-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(230, 126, 34, 0.1);
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  margin-bottom: 12px;
  background: #fafafa;
  border-radius: 10px;
}

.setting-item label {
  font-weight: 500;
  color: var(--text-primary);
}

.input-field {
  padding: 10px 16px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 8px;
  font-size: 0.95rem;
  width: 300px;
}

.input-field:focus {
  outline: none;
  border-color: var(--primary-color);
}

.btn-outline {
  padding: 10px 20px;
  background: white;
  border: 2px solid var(--primary-color);
  color: var(--primary-color);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-outline:hover {
  background: rgba(230, 126, 34, 0.05);
  transform: translateY(-2px);
}

.settings-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-primary {
  padding: 12px 32px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(230, 126, 34, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(230, 126, 34, 0.4);
}

.vip-card {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, rgba(231, 76, 60, 0.05), rgba(253, 121, 168, 0.05));
}

.vip-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.vip-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.vip-icon {
  font-size: 2rem;
}

.vip-title h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.btn-vip {
  padding: 12px 32px;
  background: linear-gradient(135deg, #e74c3c, #fd79a8);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

.btn-vip:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(231, 76, 60, 0.4);
}

.vip-benefits {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.benefit-icon {
  font-size: 1.5rem;
}

.benefit-text {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-primary);
}

@media (max-width: 1024px) {
  .container {
    grid-template-columns: 1fr;
  }

  .profile-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .action-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .vip-benefits {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .personal-container {
    padding: 0 16px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .profile-stats {
    grid-template-columns: 1fr 1fr;
  }

  .setting-item {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .input-field {
    width: 100%;
  }

  .action-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid #eee;
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 4px 12px;
  border-radius: 8px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f5f5f5;
  color: var(--text-primary);
}

.modal-body {
  padding: 24px;
  max-height: calc(90vh - 140px);
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #eee;
  background: #fafafa;
}

.btn-secondary {
  padding: 12px 24px;
  background: #f5f5f5;
  border: none;
  color: var(--text-primary);
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: #eee;
}
</style>
