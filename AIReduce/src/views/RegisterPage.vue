<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-illustration">
        <div class="illustration-content">
          <div class="brand-logo">
            <img src="/favicon.png" alt="迅文" class="brand-icon">
            <span class="brand-name">迅文</span>
          </div>
          <h2 class="brand-title">开启智能写作之旅</h2>
          <p class="brand-subtitle">加入迅文，让AI为您的学术之路保驾护航</p>
          <div class="features-preview">
            <div class="feature-item">
              <span class="feature-icon">🎯</span>
              <span class="feature-text">智能降重</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">✨</span>
              <span class="feature-text">学术润色</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🔒</span>
              <span class="feature-text">隐私保护</span>
            </div>
          </div>
          <div class="decorative-dots">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>

      <div class="register-card">
        <button class="back-btn" @click="goHome">
          <svg class="back-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          <span>返回首页</span>
        </button>
        <div class="register-header">
          <h1 class="register-title">创建账号</h1>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label class="form-label">用户名</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <input
                v-model="form.username"
                type="text"
                class="form-input"
                placeholder="请输入用户名"
                required
              />
            </div>
            <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">邮箱地址</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <input
                v-model="form.email"
                type="email"
                class="form-input"
                placeholder="请输入邮箱地址"
                required
              />
            </div>
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <div class="label-row">
              <label class="form-label">密码</label>
              <button type="button" @click="togglePassword" class="forgot-link">
                {{ showPassword ? '隐藏' : '显示' }}
              </button>
            </div>
            <div class="input-wrapper">
              <svg v-if="!showPassword" class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <svg v-else class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="请输入密码"
                required
              />
            </div>
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
            <span class="password-hint">密码长度8-16位，建议包含字母和数字</span>
          </div>

          <div class="form-group">
            <label class="form-label">确认密码</label>
            <div class="input-wrapper">
              <svg v-if="!showPassword" class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <svg v-else class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              <input
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="请再次输入密码"
                required
              />
            </div>
            <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.agreed" />
              <span class="checkbox-icon"></span>
              <span>
                我已阅读并同意
                <a href="#" class="link-primary">用户协议</a>
                和
                <a href="#" class="link-primary">隐私政策</a>
              </span>
            </label>
            <span v-if="errors.agreed" class="error-message">{{ errors.agreed }}</span>
          </div>

          <button type="submit" :disabled="loading" class="btn btn-primary btn-block">
            <svg v-if="loading" class="loading-spinner" viewBox="0 0 24 24">
              <circle class="path" cx="12" cy="12" r="10" fill="none" stroke-width="4"/>
            </svg>
            {{ loading ? '注册中...' : '立即注册' }}
          </button>
        </form>

        <div class="divider">
          <span class="divider-line"></span>
          <span class="divider-text">或</span>
          <span class="divider-line"></span>
        </div>

        <div class="social-login">
          <button class="social-btn wechat" @click="registerWithWechat">
            <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c4.801 0 8.692-3.287 8.692-7.343 0-4.054-3.891-7.339-8.692-7.339z"/>
            </svg>
            <span>微信注册</span>
          </button>
        </div>

        <div class="register-footer">
          <p>
            已有账号？
            <router-link to="/login" class="link-primary">立即登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../utils/api'
import { showToast } from '../utils/toast'

const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreed: false
})

const showPassword = ref(false)
const loading = ref(false)
const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreed: ''
})

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const validateForm = () => {
  let isValid = true
  errors.username = ''
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''
  errors.agreed = ''

  if (!form.username) {
    errors.username = '请输入用户名'
    isValid = false
  } else if (form.username.length < 2 || form.username.length > 20) {
    errors.username = '用户名长度应在2-20位之间'
    isValid = false
  } else if (!/^[a-zA-Z0-9\u4e00-\u9fa5]+$/.test(form.username)) {
    errors.username = '用户名只能包含中文、字母和数字'
    isValid = false
  }

  if (!form.email) {
    errors.email = '请输入邮箱地址'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = '请输入有效的邮箱地址'
    isValid = false
  }

  if (!form.password) {
    errors.password = '请输入密码'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = '密码长度不能少于8位'
    isValid = false
  } else if (form.password.length > 16) {
    errors.password = '密码长度不能超过16位'
    isValid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = '请再次输入密码'
    isValid = false
  } else if (form.confirmPassword !== form.password) {
    errors.confirmPassword = '两次输入的密码不一致'
    isValid = false
  }

  if (!form.agreed) {
    errors.agreed = '请同意用户协议和隐私政策'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) return

  loading.value = true

  try {
    const response = await authAPI.register({
      username: form.username,
      email: form.email,
      password: form.password
    })
    
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
    localStorage.setItem('isLoggedIn', 'true')
    
    showToast('注册成功', 'success')
    router.push('/workspace')
  } catch (error) {
    errors.email = error.message || '注册失败，请稍后重试'
    showToast(error.message || '注册失败', 'error')
  } finally {
    loading.value = false
  }
}

const registerWithWechat = () => {
  showToast('微信注册功能开发中，请使用账号密码注册', 'info')
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fdf6e3 0%, #fef9f3 50%, #fff8f0 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.register-page::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(230, 126, 34, 0.08) 0%, transparent 70%);
  border-radius: 50%;
}

.register-page::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(243, 156, 18, 0.06) 0%, transparent 70%);
  border-radius: 50%;
}

.register-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 900px;
  position: relative;
  z-index: 1;
}

@media (min-width: 900px) {
  .register-container {
    flex-direction: row;
    gap: 60px;
    align-items: center;
  }
}

.register-illustration {
  display: none;
}

@media (min-width: 900px) {
  .register-illustration {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    padding: 40px;
    order: -1;
  }

  .illustration-content {
    text-align: center;
    animation: slideInLeft 0.8s ease-out;
    position: relative;
  }

  .brand-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 28px;
  }

  .brand-icon {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(230, 126, 34, 0.15);
    transition: transform 0.3s ease;
  }

  .brand-logo:hover .brand-icon {
    transform: scale(1.05);
  }

  .brand-name {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e67e22, #f39c12);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .brand-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
    letter-spacing: -0.5px;
  }

  .brand-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: 40px;
  }

  .features-preview {
    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: center;
  }

  .feature-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 24px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 14px;
    border: 1px solid rgba(230, 126, 34, 0.1);
    box-shadow: 0 4px 16px rgba(230, 126, 34, 0.08);
    transition: all 0.3s ease;
    width: 100%;
    max-width: 280px;
  }

  .feature-item:hover {
    transform: translateX(8px);
    box-shadow: 0 6px 24px rgba(230, 126, 34, 0.12);
  }

  .feature-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .feature-text {
    font-size: 0.95rem;
    color: var(--text-secondary);
    font-weight: 500;
  }

  .decorative-dots {
    position: absolute;
    bottom: -20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 8px;
  }

  .dot {
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, #e67e22, #f39c12);
    border-radius: 50%;
    animation: dotPulse 2s ease-in-out infinite;
  }

  .dot:nth-child(2) {
    animation-delay: 0.3s;
  }

  .dot:nth-child(3) {
    animation-delay: 0.6s;
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes dotPulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

.register-card {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  padding: 32px 40px 48px;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 24px;
  border: 1px solid rgba(230, 126, 34, 0.08);
  box-shadow: 0 20px 60px rgba(230, 126, 34, 0.12);
  animation: slideInRight 0.8s ease-out;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 16px;
}

.back-btn:hover {
  color: var(--primary-color);
  transform: translateX(-4px);
}

.back-icon {
  width: 18px;
  height: 18px;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.register-header {
  text-align: center;
  margin-bottom: 36px;
}

.register-title {
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.register-subtitle {
  font-size: 0.95rem;
  color: var(--primary-color);
  font-weight: 600;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.forgot-link {
  font-size: 0.85rem;
  color: var(--primary-color);
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: var(--primary-dark);
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: var(--text-light);
  transition: color 0.3s ease;
}

.form-input:focus + .input-icon,
.form-input:not(:placeholder-shown) + .input-icon {
  color: var(--primary-color);
}

.form-input {
  width: 100%;
  padding: 16px 16px 16px 52px;
  border: 2px solid rgba(230, 126, 34, 0.12);
  border-radius: 14px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.9);
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.08);
}

.form-input::placeholder {
  color: var(--text-light);
}

.error-message {
  font-size: 0.82rem;
  color: var(--danger);
}

.password-hint {
  font-size: 0.82rem;
  color: var(--text-light);
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.checkbox-label input {
  display: none;
}

.checkbox-icon {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(230, 126, 34, 0.25);
  border-radius: 5px;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.3s ease;
}

.checkbox-label input:checked + .checkbox-icon {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  border-color: var(--primary-color);
}

.checkbox-label input:checked + .checkbox-icon::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.link-primary {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link-primary:hover {
  color: var(--primary-dark);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 28px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  gap: 10px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  box-shadow: 0 4px 20px rgba(230, 126, 34, 0.35);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(230, 126, 34, 0.45);
}

.btn-block {
  width: 100%;
  padding: 16px;
  font-size: 1.05rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

.loading-spinner .path {
  stroke-dasharray: 100;
  stroke-dashoffset: 0;
  animation: dash 1.5s ease-in-out infinite;
  stroke: white;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes dash {
  0% { stroke-dashoffset: 100; }
  50% { stroke-dashoffset: 25; }
  100% { stroke-dashoffset: 100; }
}

.divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 28px 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(230, 126, 34, 0.2), transparent);
}

.divider-text {
  font-size: 0.85rem;
  color: var(--text-light);
  font-weight: 500;
}

.social-login {
  display: flex;
  gap: 12px;
}

.social-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  border: 2px solid rgba(230, 126, 34, 0.1);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.9);
  font-size: 0.95rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-btn:hover {
  border-color: var(--primary-color);
  background: rgba(230, 126, 34, 0.03);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.1);
}

.social-btn.wechat {
  border-color: rgba(0, 191, 165, 0.3);
}

.social-btn.wechat:hover {
  border-color: #00bfa5;
  background: rgba(0, 191, 165, 0.05);
}

.social-btn.wechat .social-icon {
  color: #00bfa5;
}

.social-icon {
  width: 20px;
  height: 20px;
}

.register-footer {
  text-align: center;
  margin-top: 24px;
}

.register-footer p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

@media (max-width: 900px) {
  .register-card {
    padding: 40px 28px;
  }

  .register-title {
    font-size: 1.6rem;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 32px 20px;
    border-radius: 20px;
  }
}
</style>