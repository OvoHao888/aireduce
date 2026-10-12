const API_BASE = 'http://localhost:8000/api/admin'

// 获取 token
const getToken = () => localStorage.getItem('admin_token')

// 带认证的请求头
const getHeaders = () => {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  return headers
}

// 通用请求方法
const request = async (url, options = {}) => {
  const token = getToken()
  if (!token) {
    throw new Error('未登录，请先登录')
  }
  
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers
    }
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    // token 过期或无效
    if (response.status === 401) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      window.location.href = '/login'
    }
    throw new Error(data.message || '请求失败')
  }
  
  return data
}

// ==================== 用户管理 ====================
export const userAPI = {
  getUsers: (page = 1, limit = 10) => 
    request(`/users?page=${page}&limit=${limit}`),
  
  getUser: (id) => 
    request(`/users/${id}`),
  
  updateUser: (id, data) => 
    request(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
  
  updateUserStatus: (id, status) => 
    request(`/users/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    }),
  
  deleteUser: (id) => 
    request(`/users/${id}`, { method: 'DELETE' })
}

// ==================== 卡密管理 ====================
export const cardAPI = {
  getCards: (page = 1, limit = 10) => 
    request(`/cards?page=${page}&limit=${limit}`),
  
  createCard: (data) => 
    request(`/cards`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  
  getCard: (id) => 
    request(`/cards/${id}`),
  
  updateCardStatus: (id, status) => 
    request(`/cards/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    }),
  
  deleteCard: (id) => 
    request(`/cards/${id}`, { method: 'DELETE' })
}

// ==================== 套餐管理 ====================
export const productAPI = {
  getProducts: (page = 1, limit = 10) => 
    request(`/products?page=${page}&limit=${limit}`),
  
  createProduct: (data) => 
    request(`/products`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  
  updateProduct: (id, data) => 
    request(`/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),
  
  deleteProduct: (id) => 
    request(`/products/${id}`, { method: 'DELETE' })
}

// ==================== 使用记录 ====================
export const recordAPI = {
  getRecords: (page = 1, limit = 10) => 
    request(`/records?page=${page}&limit=${limit}`),
  
  deleteRecord: (id) => 
    request(`/records/${id}`, { method: 'DELETE' })
}

// ==================== 反馈管理 ====================
export const feedbackAPI = {
  getFeedbacks: (page = 1, limit = 10) => 
    request(`/feedbacks?page=${page}&limit=${limit}`),
  
  replyFeedback: (id, reply) => 
    request(`/feedbacks/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ reply })
    }),
  
  deleteFeedback: (id) => 
    request(`/feedbacks/${id}`, { method: 'DELETE' })
}

// ==================== 统计概览 ====================
export const statsAPI = {
  getStats: () => request('/stats')
}

// ==================== API配置 ====================
export const configAPI = {
  // 获取API配置
  getApiConfig: () => request('/config/api'),
  
  // 更新API配置
  updateApiConfig: (data) => 
    request('/config/api', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  
  // 测试API连接
  testApiConnection: (data) => 
    request('/config/api/test', {
      method: 'POST',
      body: JSON.stringify(data)
    }),
  
  // 获取支持的模型列表
  getSupportedModels: () => request('/config/models')
}