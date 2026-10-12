<template>
  <div class="feedback-management">
    <!-- 反馈表格 -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户</th>
            <th>类型</th>
            <th>内容</th>
            <th>状态</th>
            <th>提交时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="feedback in feedbacks" :key="feedback.id">
            <td>{{ feedback.id }}</td>
            <td>{{ feedback.username || feedback.user_id || '-' }}</td>
            <td>{{ formatType(feedback.type) }}</td>
            <td class="content-cell">
              <div class="feedback-content">{{ feedback.content }}</div>
            </td>
            <td>
              <span :class="['status-badge', feedback.reply ? 'replied' : 'pending']">
                {{ feedback.reply ? '已回复' : '待回复' }}
              </span>
            </td>
            <td>{{ formatDate(feedback.created_at) }}</td>
            <td>
              <button @click="handleReply(feedback)" class="btn-link">回复</button>
              <button @click="handleView(feedback)" class="btn-link">查看</button>
              <button @click="handleDelete(feedback)" class="btn-link danger">删除</button>
            </td>
          </tr>
          <tr v-if="feedbacks.length === 0 && !loading">
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
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>反馈详情</h3>
          <button @click="showDetailModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <label>用户</label>
            <div>{{ currentFeedback.username || currentFeedback.user_id || '-' }}</div>
          </div>
          <div class="detail-section">
            <label>类型</label>
            <div>{{ formatType(currentFeedback.type) }}</div>
          </div>
          <div class="detail-section">
            <label>提交时间</label>
            <div>{{ formatDate(currentFeedback.created_at) }}</div>
          </div>
          <div class="detail-section">
            <label>反馈内容</label>
            <div class="content-box">{{ currentFeedback.content }}</div>
          </div>
          <div v-if="currentFeedback.reply" class="detail-section">
            <label>回复内容</label>
            <div class="content-box reply-box">{{ currentFeedback.reply }}</div>
          </div>
          <div v-if="currentFeedback.reply_at" class="detail-section">
            <label>回复时间</label>
            <div>{{ formatDate(currentFeedback.reply_at) }}</div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showDetailModal = false" class="btn">关闭</button>
        </div>
      </div>
    </div>

    <!-- 回复弹窗 -->
    <div v-if="showReplyModal" class="modal-overlay" @click="showReplyModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>回复反馈</h3>
          <button @click="showReplyModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <label>反馈内容</label>
            <div class="content-box">{{ currentFeedback.content }}</div>
          </div>
          <div class="form-group">
            <label>回复内容</label>
            <textarea v-model="replyForm.content" rows="5" placeholder="请输入回复内容..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showReplyModal = false" class="btn">取消</button>
          <button @click="handleSubmitReply" class="btn btn-primary">提交回复</button>
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
import { feedbackAPI } from '../utils/adminApi.js'

export default {
  name: 'FeedbackManagement',
  setup() {
    const loading = ref(false)
    const error = ref('')
    const feedbacks = ref([])
    const page = ref(1)
    const limit = ref(10)
    const total = ref(0)
    const showDetailModal = ref(false)
    const showReplyModal = ref(false)
    const currentFeedback = ref({})
    const replyForm = ref({
      content: ''
    })

    const totalPages = computed(() => Math.ceil(total.value / limit.value))

    const fetchFeedbacks = async () => {
      loading.value = true
      error.value = ''
      try {
        const data = await feedbackAPI.getFeedbacks(page.value, limit.value)
        feedbacks.value = data.items || data || []
        total.value = data.total || feedbacks.value.length
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchFeedbacks()
    }

    const handleView = (feedback) => {
      currentFeedback.value = feedback
      showDetailModal.value = true
    }

    const handleReply = (feedback) => {
      currentFeedback.value = feedback
      replyForm.value = { content: feedback.reply || '' }
      showReplyModal.value = true
    }

    const handleSubmitReply = async () => {
      if (!replyForm.value.content.trim()) {
        error.value = '回复内容不能为空'
        return
      }
      try {
        await feedbackAPI.replyFeedback(currentFeedback.value.id, replyForm.value.content)
        showReplyModal.value = false
        fetchFeedbacks()
      } catch (err) {
        error.value = err.message
      }
    }

    const handleDelete = async (feedback) => {
      if (!confirm('确定要删除该反馈吗？此操作不可恢复。')) return
      try {
        await feedbackAPI.deleteFeedback(feedback.id)
        fetchFeedbacks()
      } catch (err) {
        error.value = err.message
      }
    }

    const formatType = (type) => {
      const types = {
        'bug': '问题反馈',
        'feature': '功能建议',
        'question': '问题咨询',
        'other': '其他'
      }
      return types[type] || type || '-'
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchFeedbacks()
    })

    return {
      loading,
      error,
      feedbacks,
      page,
      totalPages,
      total,
      showDetailModal,
      showReplyModal,
      currentFeedback,
      replyForm,
      handlePageChange,
      handleView,
      handleReply,
      handleSubmitReply,
      handleDelete,
      formatType,
      formatDate
    }
  }
}
</script>

<style scoped>
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

.content-cell {
  max-width: 300px;
}

.feedback-content {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.status-badge.pending {
  background: #fff7e6;
  color: #fa8c16;
}

.status-badge.replied {
  background: #e6f7e6;
  color: #52c41a;
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
  width: 500px;
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
  max-height: 150px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

.reply-box {
  background: #e6f7e6;
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

.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  resize: vertical;
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