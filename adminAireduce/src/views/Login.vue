<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <h1 class="gradient-text">管理后台登录</h1>
        <p>请输入管理员账号密码</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="请输入用户名"
            required
          />
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码"
            required
          />
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="login-footer">
        <router-link to="/" class="back-link">返回用户端</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'AdminLogin',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    const form = ref({
      username: '',
      password: ''
    })
    const loading = ref(false)
    const error = ref('')
    
    const handleLogin = async () => {
      if (!form.value.username || !form.value.password) {
        error.value = '请填写用户名和密码'
        return
      }
      
      loading.value = true
      error.value = ''
      
      try {
        const response = await fetch('http://localhost:8000/api/admin/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: form.value.username,
            password: form.value.password
          })
        })
        
        const data = await response.json()
        
        if (response.ok && data.token) {
          localStorage.setItem('admin_token', data.token)
          localStorage.setItem('admin_user', JSON.stringify(data.user || { username: form.value.username }))
          
          const redirect = route.query.redirect || '/'
          router.push(redirect)
        } else {
          error.value = data.message || '用户名或密码错误'
        }
      } catch (err) {
        error.value = '网络错误，请检查后端服务是否运行'
        console.error('Login error:', err)
      } finally {
        loading.value = false
      }
    }
    
    // 检查是否已登录
    onMounted(() => {
      const token = localStorage.getItem('admin_token')
      if (token) {
        router.push('/')
      }
    })
    
    return {
      form,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fdfbf7 0%, #faf5ef 50%, #fdf6e3 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(230, 126, 34, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  font-size: 28px;
  margin-bottom: 8px;
}

.login-header p {
  color: #888;
  font-size: 14px;
}

.login-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-group input:focus {
  border-color: #e67e22;
  box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.1);
  outline: none;
}

.error-message {
  color: #e74c3c;
  background: rgba(231, 76, 60, 0.1);
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 16px;
  font-size: 14px;
  text-align: center;
}

.login-form .btn {
  width: 100%;
  margin-top: 8px;
}

.login-footer {
  text-align: center;
}

.back-link {
  color: #888;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #e67e22;
}
</style>