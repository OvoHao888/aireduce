<template>
  <div class="user-management">
    <!-- 工具栏 -->
    <div class="toolbar">
      <input 
        v-model="searchKeyword" 
        type="text" 
        placeholder="搜索用户名/邮箱..." 
        class="search-input"
        @keyup.enter="handleSearch"
      />
      <button @click="handleSearch" class="btn btn-primary">搜索</button>
      <button @click="handleReset" class="btn">重置</button>
    </div>

    <!-- 用户表格 -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>会员状态</th>
            <th>剩余次数</th>
            <th>注册时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span :class="['status-badge', user.is_vip ? 'vip' : 'normal']">
                {{ user.is_vip ? '会员' : '普通' }}
              </span>
            </td>
            <td>{{ user.remaining_uses }}</td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <button @click="handleEdit(user)" class="btn-link">编辑</button>
              <button @click="handleToggleStatus(user)" class="btn-link">
                {{ user.is_vip ? '取消会员' : '设为会员' }}
              </button>
              <button @click="handleDelete(user)" class="btn-link danger">删除</button>
            </td>
          </tr>
          <tr v-if="users.length === 0 && !loading">
            <td colspan="7" class="empty">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <span>共 {{ total }} 条，第 {{ page }}/{{ totalPages }} 页</span>
      <div class="pagination-buttons">
        <button 
          @click="handlePageChange(page - 1)" 
          :disabled="page <= 1"
          class="btn"
        >上一页</button>
        <button 
          @click="handlePageChange(page + 1)" 
          :disabled="page >= totalPages"
          class="btn"
        >下一页</button>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <div v-if="showEditModal" class="modal-overlay" @click="showEditModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>编辑用户</h3>
          <button @click="showEditModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="editForm.username" type="text" />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="editForm.email" type="email" />
          </div>
          <div class="form-group">
            <label>剩余次数</label>
            <input v-model.number="editForm.remaining_uses" type="number" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showEditModal = false" class="btn">取消</button>
          <button @click="handleSave" class="btn btn-primary">保存</button>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>
    
    <!-- 错误提示 -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { userAPI } from '../utils/adminApi.js'

export default {
  name: 'UserManagement',
  setup() {
    const loading = ref(false)
    const error = ref('')
    const users = ref([])
    const page = ref(1)
    const limit = ref(10)
    const total = ref(0)
    const searchKeyword = ref('')
    const showEditModal = ref(false)
    const editForm = ref({
      id: null,
      username: '',
      email: '',
      remaining_uses: 0
    })

    const totalPages = computed(() => Math.ceil(total.value / limit.value))

    const fetchUsers = async () => {
      loading.value = true
      error.value = ''
      try {
        const data = await userAPI.getUsers(page.value, limit.value)
        users.value = data.items || data || []
        total.value = data.total || users.value.length
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      page.value = 1
      fetchUsers()
    }

    const handleReset = () => {
      searchKeyword.value = ''
      page.value = 1
      fetchUsers()
    }

    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchUsers()
    }

    const handleEdit = (user) => {
      editForm.value = {
        id: user.id,
        username: user.username,
        email: user.email,
        remaining_uses: user.remaining_uses
      }
      showEditModal.value = true
    }

    const handleSave = async () => {
      try {
        await userAPI.updateUser(editForm.value.id, {
          username: editForm.value.username,
          email: editForm.value.email,
          remaining_uses: editForm.value.remaining_uses
        })
        showEditModal.value = false
        fetchUsers()
      } catch (err) {
        error.value = err.message
      }
    }

    const handleToggleStatus = async (user) => {
      if (!confirm(`确定要${user.is_vip ? '取消' : '设置'}该用户的会员身份吗？`)) return
      try {
        await userAPI.updateUserStatus(user.id, user.is_vip ? 'normal' : 'vip')
        fetchUsers()
      } catch (err) {
        error.value = err.message
      }
    }

    const handleDelete = async (user) => {
      if (!confirm(`确定要删除用户 "${user.username}" 吗？此操作不可恢复。`)) return
      try {
        await userAPI.deleteUser(user.id)
        fetchUsers()
      } catch (err) {
        error.value = err.message
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchUsers()
    })

    return {
      loading,
      error,
      users,
      page,
      totalPages,
      total,
      searchKeyword,
      showEditModal,
      editForm,
      handleSearch,
      handleReset,
      handlePageChange,
      handleEdit,
      handleSave,
      handleToggleStatus,
      handleDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 240px;
  font-size: 14px;
}

.table-container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.data-table th {
  background: #fafafa;
  font-weight: 600;
  color: #333;
}

.data-table td {
  color: #666;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.status-badge.vip {
  background: #fff7e6;
  color: #fa8c16;
}

.status-badge.normal {
  background: #f5f5f5;
  color: #999;
}

.btn-link {
  background: none;
  border: none;
  color: #00d4ff;
  cursor: pointer;
  margin-right: 12px;
  font-size: 14px;
}

.btn-link:hover {
  text-decoration: underline;
}

.btn-link.danger {
  color: #ff4444;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
}

.pagination-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.btn:hover {
  background: #f5f5f5;
}

.btn-primary {
  background: #00d4ff;
  border-color: #00d4ff;
  color: #fff;
}

.btn-primary:hover {
  background: #00b8e6;
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
}

.modal {
  background: #fff;
  border-radius: 12px;
  width: 480px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.loading, .error, .empty {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #ff4444;
}
</style>