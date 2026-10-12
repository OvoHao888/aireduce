<template>
  <div class="card-management">
    <!-- 工具栏 -->
    <div class="toolbar">
      <button @click="showCreateModal = true" class="btn btn-primary">生成卡密</button>
    </div>

    <!-- 卡密表格 -->
    <div class="table-container">
      <table class="data-table" style="width:100%; table-layout:auto; border-collapse:collapse;">
        <thead>
          <tr>
            <th style="padding:12px; text-align:left;">ID</th>
            <th style="padding:12px; text-align:left;">卡密码</th>
            <th style="padding:12px; text-align:left;">套餐类型</th>
            <th style="padding:12px; text-align:left;">时长</th>
            <th style="padding:12px; text-align:left;">状态</th>
            <th style="padding:12px; text-align:left;">使用者</th>
            <th style="padding:12px; text-align:left;">创建时间</th>
            <th style="padding:12px; text-align:left;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="card in cards" :key="card.id">
            <td style="padding:12px;">{{ card.id }}</td>
            <td class="code-cell" style="padding:12px;">{{ card.card_code }}</td>
            <td style="padding:12px;">{{ card.token_type }}</td>
            <td style="padding:12px;">{{ card.duration_days ? card.duration_days + '天' : card.duration_hours ? card.duration_hours + '小时' : '-' }}</td>
            <td style="padding:12px;">
              <span :class="['status-badge', card.status]">
                {{ card.status === 'used' ? '已使用' : card.status === 'unused' ? '未使用' : '已过期' }}
              </span>
            </td>
            <td style="padding:12px;">{{ card.used_by || '-' }}</td>
            <td style="padding:12px;">{{ formatDate(card.created_at) }}</td>
            <td style="padding:12px;">
              <button @click="handleDelete(card)" class="btn-link danger">删除</button>
            </td>
          </tr>
          <tr v-if="cards.length === 0 && !loading">
            <td colspan="8" class="empty">暂无数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <span>共 {{ total }} 条，第 {{ page }}/{{ totalPages }} 页</span>
      <div class="pagination-buttons">
        <button @click="handlePageChange(page - 1)" :disabled="page <= 1" class="btn">上一页</button>
        <button @click="handlePageChange(page + 1)" :disabled="page >= totalPages" class="btn">下一页</button>
      </div>
    </div>

    <!-- 创建卡密弹窗 -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>生成卡密</h3>
          <button @click="showCreateModal = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>生成数量</label>
            <input v-model.number="createForm.count" type="number" min="1" max="100" placeholder="1" />
          </div>
          <div class="form-group">
            <label>卡密类型</label>
            <select v-model="createForm.type">
              <option value="1hour">1小时卡</option>
              <option value="3hour">3小时卡</option>
              <option value="12hour">12小时卡</option>
              <option value="1day">日卡</option>
              <option value="3day">3天卡</option>
              <option value="7day">7天卡</option>
              <option value="1month">月卡</option>
              <option value="1quarter">季卡</option>
              <option value="6month">半年卡</option>
              <option value="1year">年卡</option>
            </select>
          </div>
          <div class="form-group">
            <label>次数限制</label>
            <input v-model.number="createForm.expire_days" type="number" min="1" placeholder="不填则不限制" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateModal = false" class="btn btn-cancel">取消</button>
          <button @click="handleCreate" class="btn btn-generate">生成</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { cardAPI } from '../utils/adminApi.js'

export default {
  name: 'CardManagement',
  setup() {
    const loading = ref(false)
    const error = ref('')
    const cards = ref([])
    const page = ref(1)
    const limit = ref(10)
    const total = ref(0)
    const showCreateModal = ref(false)
    
    const createForm = ref({
      count: 1,
      type: '1day',
      expire_days: null
    })

    const totalPages = computed(() => Math.ceil(total.value / limit.value))

    const fetchCards = async () => {
      loading.value = true
      error.value = ''
      try {
        const data = await cardAPI.getCards(page.value, limit.value)
        cards.value = data.items || []
        total.value = data.total || cards.value.length
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchCards()
    }

    const handleCreate = async () => {
      try {
        const payload = {
          token_type: createForm.value.type,
          quantity: createForm.value.count
        }
        if (createForm.value.expire_days) {
          payload.expire_days = createForm.value.expire_days
        }
        await cardAPI.createCard(payload)
        showCreateModal.value = false
        createForm.value = { count: 1, type: '1day', expire_days: null }
        fetchCards()
      } catch (err) {
        error.value = err.message
      }
    }

    const handleDelete = async (card) => {
      if (!confirm('确定删除这张卡密？')) return
      try {
        await cardAPI.deleteCard(card.id)
        fetchCards()
      } catch (err) {
        error.value = err.message
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('zh-CN')
    }

    onMounted(() => {
      fetchCards()
    })

    return {
      loading,
      error,
      cards,
      page,
      limit,
      total,
      showCreateModal,
      createForm,
      totalPages,
      handlePageChange,
      handleCreate,
      handleDelete,
      formatDate
    }
  }
}
</script>

<style scoped>
.card-management {
  width: 100%;
}

.code-cell {
  font-family: 'Consolas', monospace;
  font-size: 13px;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.unused {
  background: rgba(230, 126, 34, 0.15);
  color: #e67e22;
}

.status-badge.used {
  background: rgba(39, 174, 96, 0.15);
  color: #27ae96;
}

.status-badge.expired {
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

.empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 12px;
  width: 440px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 26px;
  cursor: pointer;
  color: #999;
  line-height: 1;
}

.close-btn:hover { color: #666; }

.modal-body {
  padding: 0 24px 20px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #00d4ff;
}

.modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-cancel {
  padding: 10px 24px;
  border: 1px solid #ddd;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}

.btn-cancel:hover { background: #f5f5f5; }

.btn-generate {
  padding: 10px 28px;
  border: none;
  background: #00d4ff;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.btn-generate:hover { background: #00b8e6; }
</style>