<template>
  <div class="product-management">
    <!-- 工具栏 -->
    <div class="toolbar">
      <button @click="handleCreate" class="btn btn-primary">添加套餐</button>
    </div>

    <!-- 套餐表格 -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>套餐名称</th>
            <th>类型</th>
            <th>价格(元)</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.token_type }}</td>
            <td>{{ product.price }}</td>
            <td>
              <span :class="['status-badge', product.is_active ? 'active' : 'inactive']">
                {{ product.is_active ? '启用' : '禁用' }}
              </span>
            </td>
            <td>
              <button @click="handleEdit(product)" class="btn-link">编辑</button>
              <button @click="handleDelete(product)" class="btn-link danger">删除</button>
            </td>
          </tr>
          <tr v-if="products.length === 0 && !loading">
            <td colspan="6" class="empty">暂无数据</td>
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

    <!-- 添加/编辑套餐弹窗 -->
    <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ isEdit ? '编辑套餐' : '添加套餐' }}</h3>
          <button @click="showModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>套餐名称</label>
            <input v-model="form.name" type="text" placeholder="例如：月卡套餐" />
          </div>
          <div class="form-group">
            <label>类型</label>
            <select v-model="form.token_type">
              <option value="1hour">1小时卡</option>
              <option value="3hour">3小时卡</option>
              <option value="12hour">12小时卡</option>
              <option value="1day">1天卡</option>
              <option value="3day">3天卡</option>
              <option value="7day">7天卡</option>
              <option value="1month">1个月卡</option>
              <option value="1quarter">1季卡</option>
              <option value="6month">半年卡</option>
              <option value="1year">1年卡</option>
            </select>
          </div>
          <div class="form-group">
            <label>价格(元)</label>
            <input v-model.number="form.price" type="number" min="0" step="0.01" />
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="form.description" rows="3" placeholder="套餐描述..."></textarea>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="form.is_active" type="checkbox" />
              启用
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showModal = false" class="btn">取消</button>
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
import { productAPI } from '../utils/adminApi.js'

export default {
  name: 'ProductManagement',
  setup() {
    const loading = ref(false)
    const error = ref('')
    const products = ref([])
    const page = ref(1)
    const limit = ref(10)
    const total = ref(0)
    const showModal = ref(false)
    const isEdit = ref(false)
    const form = ref({
      id: null,
      name: '',
      token_type: '1month',
      price: 0,
      duration_days: 30,
      duration_hours: null,
      description: '',
      is_active: true
    })

    const totalPages = computed(() => Math.ceil(total.value / limit.value))

    const fetchProducts = async () => {
      loading.value = true
      error.value = ''
      try {
        const data = await productAPI.getProducts(page.value, limit.value)
        products.value = data.items || data || []
        total.value = data.total || products.value.length
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchProducts()
    }

    const resetForm = () => {
      form.value = {
        id: null,
        name: '',
        token_type: '1month',
        price: 0,
        duration_days: 30,
        duration_hours: null,
        description: '',
        is_active: true
      }
    }

    const handleCreate = () => {
      isEdit.value = false
      resetForm()
      showModal.value = true
    }

    const handleEdit = (product) => {
      isEdit.value = true
      form.value = {
        id: product.id,
        name: product.name,
        token_type: product.token_type,
        price: product.price,
        duration_days: product.duration_days,
        duration_hours: product.duration_hours,
        description: product.description || '',
        is_active: product.is_active
      }
      showModal.value = true
    }

    const handleSave = async () => {
      try {
        const data = {
          name: form.value.name,
          token_type: form.value.token_type,
          price: form.value.price,
          duration_days: form.value.duration_days,
          duration_hours: form.value.duration_hours,
          description: form.value.description,
          is_active: form.value.is_active
        }
        if (isEdit.value) {
          await productAPI.updateProduct(form.value.id, data)
        } else {
          await productAPI.createProduct(data)
        }
        showModal.value = false
        fetchProducts()
      } catch (err) {
        error.value = err.message
      }
    }

    const handleDelete = async (product) => {
      if (!confirm(`确定要删除套餐 "${product.name}" ���？��操作不可恢复。`)) return
      try {
        await productAPI.deleteProduct(product.id)
        fetchProducts()
      } catch (err) {
        error.value = err.message
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchProducts()
    })

    return {
      loading,
      error,
      products,
      page,
      totalPages,
      total,
      showModal,
      isEdit,
      form,
      handlePageChange,
      handleCreate,
      handleEdit,
      handleSave,
      handleDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
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

.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.status-badge.active {
  background: #e6f7e6;
  color: #52c41a;
}

.status-badge.inactive {
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
  max-height: 90vh;
  overflow-y: auto;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input {
  width: auto !important;
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