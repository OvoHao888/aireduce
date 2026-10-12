<template>
  <div class="records-container">
    <div class="container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">使用记录</h1>
        <div class="page-stats">
          <span>共 <strong>{{ filteredRecords.length }}</strong> 条</span>
          <span>今日 <strong>{{ stats.todayCount }}</strong> 条</span>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <select v-model="filters.mode" class="filter-select">
          <option value="">全部模式</option>
          <option value="mode1">快速降重</option>
          <option value="mode2">深度降重</option>
        </select>
        <select v-model="filters.dateRange" class="filter-select">
          <option value="">全部时间</option>
          <option value="today">今天</option>
          <option value="week">最近一周</option>
          <option value="month">最近一月</option>
        </select>
        <input
          v-model="filters.keyword"
          type="text"
          placeholder="搜索..."
          class="filter-input"
        />
        <button @click="resetFilters" class="filter-reset">重置</button>
      </div>

      <!-- 记录列表 -->
      <div class="records-list" ref="listRef" @scroll="handleScroll">
        <div
          v-for="record in visibleRecords"
          :key="record.id"
          class="record-item"
        >
          <div class="record-top">
            <span :class="['mode-tag', record.mode]">
              {{ record.mode === 'mode1' ? '快速' : '深度' }}
            </span>
            <span class="record-date">{{ formatDate(record.created_at) }}</span>
            <span class="record-count">{{ getCharCount(record.input_text) }} 字</span>
          </div>
          <div class="record-content">
            <div class="text-preview original">
              <span class="label">原文:</span>
              <span class="text">{{ truncateText(record.input_text, 60) }}</span>
            </div>
            <div class="text-preview result">
              <span class="label">结果:</span>
              <span class="text">{{ truncateText(record.output_text, 60) }}</span>
            </div>
          </div>
          <div class="record-actions">
            <button @click="viewDetail(record)" class="action-btn">查看</button>
            <button @click="deleteRecord(record)" class="action-btn delete">删除</button>
          </div>
        </div>

        <!-- 加载更多 -->
        <div v-if="hasMore && isLoading" class="load-more" ref="loadMoreRef">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>

        <!-- 无数据 -->
        <div v-if="filteredRecords.length === 0 && !isLoading" class="empty-state">
          <div class="empty-icon">📭</div>
          <p>暂无使用记录</p>
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetail">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>记录详情</h3>
          <button @click="closeDetail" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">处理模式:</span>
            <span>{{ selectedRecord?.mode === 'mode1' ? '快速降重' : '深度降重' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">处理时间:</span>
            <span>{{ formatDate(selectedRecord?.created_at) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">字数:</span>
            <span>{{ getCharCount(selectedRecord?.input_text) }} 字</span>
          </div>
          <div class="detail-section">
            <h4>原文内容</h4>
            <div class="detail-text">{{ selectedRecord?.input_text }}</div>
          </div>
          <div class="detail-section">
            <h4>处理结果</h4>
            <div class="detail-text">{{ selectedRecord?.output_text }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { processAPI } from '../utils/api'
import { success, error, warning } from '../utils/toast'

const router = useRouter()

// 状态
const stats = ref({ totalCount: 0, todayCount: 0 })
const filters = ref({ mode: '', dateRange: '', keyword: '' })
const showDetailModal = ref(false)
const selectedRecord = ref(null)
const loadMoreRef = ref(null)
const listRef = ref(null)
const isLoading = ref(false)

// 分页相关
const itemsPerLoad = 10
const currentPage = ref(1)
let searchTimeout = null

const records = ref([])

// 加载数据
const loadRecords = async (page = 1, reset = false) => {
  if (isLoading.value) return
  
  isLoading.value = true
  
  try {
    const response = await processAPI.getRecords(page, itemsPerLoad)
    
    const recordsList = response.records || response
    if (reset) {
      records.value = recordsList
    } else {
      records.value = [...records.value, ...recordsList]
    }
    
    updateStats()
  } catch (err) {
    console.error('加载记录失败:', err)
    error(err.message || '加载记录失败')
  } finally {
    isLoading.value = false
  }
}

// 筛选数据
const filteredRecords = computed(() => {
  let result = records.value

  if (filters.value.mode) {
    result = result.filter(r => r.mode === filters.value.mode)
  }

  if (filters.value.dateRange) {
    const now = new Date()
    let cutoff = null
    switch (filters.value.dateRange) {
      case 'today':
        cutoff = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        break
      case 'week':
        cutoff = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
        break
      case 'month':
        cutoff = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
        break
    }
    if (cutoff) {
      result = result.filter(r => new Date(r.created_at) >= cutoff)
    }
  }

  if (filters.value.keyword) {
    const keyword = filters.value.keyword.toLowerCase()
    result = result.filter(r =>
      r.input_text.toLowerCase().includes(keyword) ||
      r.output_text.toLowerCase().includes(keyword)
    )
  }

  return result
})

// 可见数据（懒加载）
const visibleRecords = computed(() => {
  return filteredRecords.value.slice(0, currentPage.value * itemsPerLoad)
})

// 是否还有更多
const hasMore = computed(() => {
  return currentPage.value * itemsPerLoad < filteredRecords.value.length
})

// 更新统计
const updateStats = () => {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const todayRecords = records.value.filter(r => new Date(r.created_at) >= today)

  stats.value = {
    totalCount: records.value.length,
    todayCount: todayRecords.length
  }
}

// 工具函数
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const minute = String(d.getMinutes()).padStart(2, '0')
  return `${month}-${day} ${hour}:${minute}`
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const getCharCount = (text) => {
  if (!text) return 0
  return text.replace(/\s+/g, '').length
}

// 事件处理
const resetFilters = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  filters.value = { mode: '', dateRange: '', keyword: '' }
  currentPage.value = 1
}

const viewDetail = (record) => {
  selectedRecord.value = record
  showDetailModal.value = true
}

const closeDetail = () => {
  showDetailModal.value = false
  selectedRecord.value = null
}

const deleteRecord = async (record) => {
  if (!confirm('确定删除这条记录？')) return

  try {
    await processAPI.deleteRecord(record.id)
    records.value = records.value.filter(r => r.id !== record.id)
    updateStats()
    success('删除成功')
  } catch (err) {
    error(err.message || '删除失败')
  }
}

// 防抖搜索
watch(filters, () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadRecords(1, true)
  }, 300)
}, { deep: true })

// 无限滚动
const handleScroll = () => {
  if (!listRef.value || !hasMore.value || isLoading.value) return

  const { scrollTop, scrollHeight, clientHeight } = listRef.value
  if (scrollTop + clientHeight >= scrollHeight - 100) {
    loadMore()
  }
}

const loadMore = () => {
  if (!hasMore.value || isLoading.value) return
  currentPage.value++
  loadRecords(currentPage.value)
}

// 生命周期
onMounted(() => {
  loadRecords(1, true)
})

onUnmounted(() => {
  if (searchTimeout) clearTimeout(searchTimeout)
})
</script>

<style scoped>
.records-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.page-stats {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.page-stats strong {
  color: var(--primary-color);
  margin: 0 4px;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.filter-select,
.filter-input {
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
}

.filter-select {
  min-width: 100px;
}

.filter-input {
  flex: 1;
}

.filter-reset {
  padding: 10px 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-reset:hover {
  background: #f3f4f6;
}

/* 记录列表 */
.records-list {
  flex: 1;
  max-height: calc(100vh - 220px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 记录项 */
.record-item {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.2s;
}

.record-item:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.record-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.mode-tag {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
}

.mode-tag.mode1 {
  background: #fef3c7;
  color: #d97706;
}

.mode-tag.mode2 {
  background: #fce7f3;
  color: #db2777;
}

.record-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.record-count {
  margin-left: auto;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.record-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.text-preview {
  display: flex;
  gap: 8px;
  font-size: 0.9rem;
  line-height: 1.5;
}

.text-preview .label {
  color: var(--text-secondary);
  flex-shrink: 0;
  font-weight: 500;
}

.text-preview .text {
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.text-preview.original .text {
  color: #6b7280;
}

.text-preview.result .text {
  color: var(--primary-color);
}

.record-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.action-btn {
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  background: #f3f4f6;
  color: var(--text-primary);
}

.action-btn:hover {
  background: #e5e7eb;
}

.action-btn.delete {
  color: #ef4444;
}

.action-btn.delete:hover {
  background: #fef2f2;
}

/* 加载更多 */
.load-more {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-btn {
  border: none;
  background: none;
  font-size: 1.3rem;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 4px;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.detail-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.detail-label {
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 80px;
}

.detail-section {
  margin-top: 20px;
}

.detail-section h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.detail-text {
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  font-size: 0.9rem;
  line-height: 1.6;
  max-height: 200px;
  overflow-y: auto;
}

/* 响应式 */
@media (max-width: 640px) {
  .records-container {
    padding: 12px;
  }

  .filter-bar {
    flex-wrap: wrap;
  }

  .filter-select {
    flex: 1;
    min-width: auto;
  }

  .filter-input {
    width: 100%;
    order: 3;
  }

  .filter-reset {
    order: 4;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
