<template>
  <div class="record-management">
    <!-- 使用记录表格 -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户</th>
            <th>模式</th>
            <th>输入</th>
            <th>输出</th>
            <th>状态</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.id">
            <td>{{ record.id }}</td>
            <td>{{ record.username || record.user_id }}</td>
            <td>{{ formatMode(record.mode) }}</td>
            <td>{{ record.input_text || '-' }}</td>
            <td>{{ record.output_text || '-' }}</td>
            <td>{{ record.status }}</td>
            <td>{{ formatDate(record.created_at) }}</td>
            <td>
              <button @click="handleView(record)" class="btn-link">查看</button>
              <button @click="handleDelete(record)" class="btn-link danger">删除</button>
            </td>
          </tr>
          <tr v-if="records.length === 0 && !loading">
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

    <!-- 查看详情弹窗 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="showDetailModal = false">
      <div class="modal modal-large" @click.stop>
        <div class="modal-header">
          <h3>使用记录详情</h3>
          <button @click="showDetailModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <label>用户</label>
            <div>{{ currentRecord.username || currentRecord.user_id }}</div>
          </div>
          <div class="detail-section">
            <label>处理模式</label>
            <div>{{ formatMode(currentRecord.mode) }}</div>
          </div>
          <div class="detail-section">
            <label>处理时间</label>
            <div>{{ formatDate(currentRecord.created_at) }}</div>
          </div>
          <div class="detail-section">
            <label>原始文本</label>
            <div class="content-box">{{ currentRecord.input || currentRecord.input_text || '-' }}</div>
          </div>
          <div class="detail-section">
            <label>处理后文本</label>
            <div class="content-box">{{ currentRecord.output || currentRecord.output_text || '-' }}</div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showDetailModal = false" class="btn">关闭</button>
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
import { recordAPI } from '../utils/adminApi.js'

export default {
  name: 'RecordManagement',
  setup() {
    const loading = ref(false)
    const error = ref('')
    const records = ref([])
    const page = ref(1)
    const limit = ref(10)
    const total = ref(0)
    const showDetailModal = ref(false)
    const currentRecord = ref({})

    const totalPages = computed(() => Math.ceil(total.value / limit.value))

    const fetchRecords = async () => {
      loading.value = true
      error.value = ''
      try {
        const data = await recordAPI.getRecords(page.value, limit.value)
        records.value = data.items || data || []
        total.value = data.total || records.value.length
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchRecords()
    }

    const handleView = (record) => {
      currentRecord.value = record
      showDetailModal.value = true
    }

    const handleDelete = async (record) => {
      if (!confirm('确定要删除该使用记录吗？此操作不可恢复。')) return
      try {
        await recordAPI.deleteRecord(record.id)
        fetchRecords()
      } catch (err) {
        error.value = err.message
      }
    }

    const formatMode = (mode) => {
      const modes = {
        'reduce': '压缩',
        'expand': '扩展',
        'both': '双降'
      }
      return modes[mode] || mode || '-'
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchRecords()
    })

    return {
      loading,
      error,
      records,
      page,
      totalPages,
      total,
      showDetailModal,
      currentRecord,
      handlePageChange,
      handleView,
      handleDelete,
      formatMode,
      formatDate
    }
  }
}
</script>

<style scoped>
.table-container {
  background: #fff;
  border-radius: 8px;
  overflow-x: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

/* 输入/输出列允许换行并限制宽度 */
.data-table td:nth-child(4),
.data-table td:nth-child(5) {
  max-width: 300px;
  white-space: normal;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
}

.data-table th {
  background: #fafafa;
  font-weight: 600;
  color: #333;
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

.modal-large {
  width: 700px;
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

.detail-section {
  margin-bottom: 16px;
}

.detail-section label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.detail-section > div {
  color: #333;
  font-size: 14px;
}

.content-box {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
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