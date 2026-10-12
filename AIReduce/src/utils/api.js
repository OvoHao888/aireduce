const BASE_URL = ''

const getToken = () => {
  return localStorage.getItem('token')
}

const request = async (url, options = {}) => {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  const token = getToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  try {
    const response = await fetch(`${BASE_URL}${url}`, {
      ...options,
      headers
    })

    if (!response.ok) {
      let detail = ''
      try {
        const errData = await response.json()
        detail = errData.detail || ''
      } catch {
        // 响应体非JSON时忽略
      }
      if (response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('isLoggedIn')
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
          if (detail === 'token_expired') {
            window.location.href = '/login?reason=expired'
          } else {
            window.location.href = '/login'
          }
        }
      }
      throw new Error(detail || '请求失败')
    }

    const data = await response.json()
    return data
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
      throw new Error('网络连接失败，请检查网络')
    }
    throw error
  }
}

export const authAPI = {
  register: (data) => request('/api/users/register', {
    method: 'POST',
    body: JSON.stringify(data)
  }),

  login: (data) => request('/api/users/login', {
    method: 'POST',
    body: JSON.stringify(data)
  }),

  getMe: () => request('/api/users/me'),

  updateProfile: (data) => request('/api/users/me', {
    method: 'PUT',
    body: JSON.stringify(data)
  }),

  changePassword: (oldPassword, newPassword) => request('/api/users/me/password', {
    method: 'PUT',
    body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
  }),

  deleteAccount: (password) => request('/api/users/me', {
    method: 'DELETE',
    body: JSON.stringify({ password })
  })
}

export const tokenAPI = {
  getProducts: () => request('/api/tokens/products'),

  exchangeCard: (cardCode) => request('/api/tokens/exchange', {
    method: 'POST',
    body: JSON.stringify({ card_code: cardCode })
  }),

  getMemberStatus: () => request('/api/tokens/my-status')
}

export const processAPI = {
  processText: (text, mode) => request('/api/process', {
    method: 'POST',
    body: JSON.stringify({ text, mode })
  }),

  // 流式处理文本
  processTextStream: async function* (text, mode, maxTokens) {
    const token = getToken()
    const response = await fetch(`${BASE_URL}/api/process/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ text, mode, max_tokens: maxTokens })
    })
    
    if (!response.ok) {
      let detail = ''
      try {
        const errData = await response.json()
        detail = errData.detail || ''
      } catch {
        // 忽略
      }
      if (response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('isLoggedIn')
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
          if (detail === 'token_expired') {
            window.location.href = '/login?reason=expired'
          } else {
            window.location.href = '/login'
          }
        }
      }
      throw new Error(detail || '请求失败')
    }
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) {
        break
      }
      
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n\n')
      buffer = lines.pop() || ''
      
      for (const line of lines) {
        if (line.trim().startsWith('data:')) {
          try {
            const jsonStr = line.trim().slice(5)
            const data = JSON.parse(jsonStr)
            yield data
          } catch (e) {
            // 忽略解析错误
          }
        }
      }
    }
    
    // 处理剩余缓冲区
    if (buffer.trim().startsWith('data:')) {
      try {
        const jsonStr = buffer.trim().slice(5)
        const data = JSON.parse(jsonStr)
        yield data
      } catch (e) {
        // 忽略解析错误
      }
    }
  },

  getRecords: (page = 1, limit = 10) => request(`/api/process/records?page=${page}&limit=${limit}`),

  getRecord: (id) => request(`/api/process/records/${id}`),

  deleteRecord: (id) => request(`/api/process/records/${id}`, {
    method: 'DELETE'
  }),

  clearCache: () => request('/api/process/clear-cache', {
    method: 'POST'
  })
}

export const feedbackAPI = {
  createFeedback: (data) => request('/api/feedbacks', {
    method: 'POST',
    body: JSON.stringify(data)
  }),

  getFeedbacks: () => request('/api/feedbacks'),

  getFeedback: (id) => request(`/api/feedbacks/${id}`)
}

export default {
  authAPI,
  tokenAPI,
  processAPI,
  feedbackAPI
}