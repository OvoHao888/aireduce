<template>
  <div class="home-container">
    <div class="container">
      <!-- 欢迎区域 -->
      <GlassCard class="welcome-section" padding="40px">
        <div class="welcome-content">
          <h1 class="welcome-title">
          <img src="/favicon.png" alt="迅文" class="title-logo">
          迅文 - AI智能双降工作台
        </h1>
          <p class="welcome-subtitle">安全、高效的文本双降工具，让您的文档更具原创性</p>
          <div class="welcome-stats">
            <div class="stat-item">
              <span class="stat-icon">✨</span>
              <span class="stat-label">智能改写</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">⚡</span>
              <span class="stat-label">极速处理</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🔒</span>
              <span class="stat-label">数据安全</span>
            </div>
          </div>
        </div>
      </GlassCard>

      <!-- 主工作区 -->
      <div class="workspace-grid">
        <!-- 左侧：输入和配置 -->
        <div class="left-panel">
          <!-- 文本输入（包含模式选择） -->
          <GlassCard class="input-section card-hover" padding="24px">
            <div class="input-header">
              <h2 class="section-title">📝 输入文本</h2>
              <!-- 模式选择嵌入 -->
              <div class="mode-selector">
                <button
                  :class="['mode-chip', { active: mode === 'mode1' }]"
                  @click="mode = 'mode1'"
                >
                  <span class="mode-chip-icon">🚀</span>
                  <span class="mode-chip-text">快速润色</span>
                  <span v-if="mode === 'mode1'" class="mode-chip-badge">推荐</span>
                </button>
                <button
                  :class="['mode-chip', { active: mode === 'mode2' }]"
                  @click="mode = 'mode2'"
                >
                  <span class="mode-chip-icon">🎯</span>
                  <span class="mode-chip-text">深度润色</span>
                  <span v-if="mode === 'mode2'" class="mode-chip-badge vip">专业</span>
                </button>
              </div>
            </div>
            <div class="textarea-wrapper">
              <textarea
                v-model="inputText"
                placeholder="请输入需要润色的文本..."
                class="text-input"
                @input="updateCharCount"
              ></textarea>
              <div class="char-info">
                <div class="char-count">{{ charCount }} / {{ maxChars }} 字符</div>
                <div v-if="inputText.length > 0" class="word-count">
                  约 {{ wordCount }} 字
                </div>
              </div>
            </div>
          </GlassCard>

          <!-- 会员有效期提示 -->
          <GlassCard class="balance-section card-hover" padding="20px">
            <div class="balance-info">
              <div class="balance-icon">🎫</div>
              <div class="balance-content">
                <div class="balance-label">会员有效期</div>
                <div class="balance-value">{{ memberExpireDate }}</div>
              </div>
              <button @click="goToTokenCard" class="btn btn-outline btn-sm">
                购买密卡
              </button>
            </div>
          </GlassCard>

          <!-- 清除缓存按钮 -->
          <GlassCard class="balance-section card-hover" padding="20px">
            <div class="balance-info">
              <div class="balance-icon">🧹</div>
              <div class="balance-content">
                <div class="balance-label">历史缓存</div>
                <div class="balance-value">防止旧内容污染新内容</div>
              </div>
              <button @click="handleClearCache" class="btn btn-outline btn-sm">
                清除缓存
              </button>
            </div>
          </GlassCard>

          <!-- 操作按钮 -->
          <div class="actions">
            <button
              @click="processText"
              :disabled="isProcessing || !canProcess"
              class="btn btn-primary btn-lg"
            >
              <span v-if="!isProcessing">▶ 开始处理</span>
              <span v-else>⏳ 处理中...</span>
            </button>
            <button
              @click="clearAll"
              :disabled="isProcessing"
              class="btn btn-secondary"
            >
              🗑️ 清空
            </button>
          </div>
        </div>

        <!-- 右侧：输出结果 -->
        <div class="right-panel">
          <GlassCard class="output-section card-hover" padding="24px">
            <h2 class="section-title">✨ 润色结果</h2>

            <!-- 进度显示 -->
            <div v-if="isProcessing" class="progress-area">
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: progress + '%' }"
                ></div>
              </div>
              <p class="progress-text">{{ progressMessage }}</p>
            </div>

            <!-- 结果显示 -->
            <div v-if="outputText" class="output-wrapper">
              <textarea
                v-model="outputText"
                readonly
                class="text-output"
              ></textarea>
              <div class="output-stats">
                <div class="stat-badge success">
                  <span>✅ 处理成功</span>
                </div>
              </div>
              <div class="output-actions">
                <button @click="copyResult" class="btn btn-outline">
                  📋 一键复制
                </button>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-if="!outputText && !isProcessing" class="empty-state">
              <div class="empty-icon">📄</div>
              <p class="empty-text">处理后的文本将显示在这里</p>
              <p class="empty-hint">请在左侧输入需要润色的文本</p>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import GlassCard from '../components/GlassCard.vue'
import { processAPI, tokenAPI } from '../utils/api'
import { success, error, info, warning } from '../utils/toast'

const router = useRouter()

// 状态变量
const inputText = ref('')
const outputText = ref('')
const mode = ref('mode1')
const isProcessing = ref(false)
const progress = ref(0)
const progressMessage = ref('')
const memberExpireDate = ref('会员已过期')
const isMember = ref(false)
const remainingDays = ref(0)

// 常量
const maxChars = 50000

// 计算属性
const charCount = computed(() => inputText.value.length)
const wordCount = computed(() => {
  const text = inputText.value.replace(/\s+/g, '').trim()
  return text.length
})

const canProcess = computed(() => {
  return (
    inputText.value.trim().length >= 10 &&
    inputText.value.trim().length <= maxChars &&
    isMember.value
  )
})

// 方法
const updateCharCount = () => {
  if (inputText.value.length > maxChars) {
    inputText.value = inputText.value.slice(0, maxChars)
  }
}

const showNotification = (message, type = 'info') => {
  switch (type) {
    case 'success':
      success(message)
      break
    case 'error':
      error(message)
      break
    case 'warning':
      warning(message)
      break
    default:
      info(message)
  }
}

const goToTokenCard = () => {
  router.push('/token-card')
}

const handleClearCache = async () => {
  try {
    await processAPI.clearCache()
    showNotification('历史缓存已清除', 'success')
  } catch (error) {
    showNotification('清除缓存失败：' + error.message, 'error')
  }
}

const processText = async () => {
  if (!canProcess.value) {
    if (!isMember.value) {
      showNotification('会员已过期，请兑换卡密', 'error')
      return
    }
    showNotification('请输入至少10个字符的文本', 'error')
    return
  }

  isProcessing.value = true
  outputText.value = ''
  progress.value = 0
  progressMessage.value = '准备开始...'

  try {
    let resultText = ''
    let currentStage = ''
    
    // 根据输入长度动态计算 max_tokens，确保 AI 能输出完整结果
    const estimatedTokens = Math.ceil(inputText.value.length / 2) // 中文约2字符/token
    const maxTokens = Math.max(4096, Math.min(estimatedTokens * 2, 16384))

    for await (const data of processAPI.processTextStream(inputText.value, mode.value, maxTokens)) {
      // 更新进度条
      if (data.progress !== undefined) {
        progress.value = data.progress
      }
      
      // 更新状态消息
      if (data.message) {
        progressMessage.value = data.message
      }
      
      // 流式内容
      if (data.status === 'streaming' && data.content) {
        if (data.stage && data.stage !== currentStage) {
          currentStage = data.stage
          // 新阶段开始，清空结果
          resultText = ''
        }
        resultText += data.content
        // ✅ 只在 enhance/rewrite 阶段（或无阶段）才显示到 UI，跳过 polish
        if (!data.stage || data.stage === 'rewrite' || data.stage === 'enhance') {
          outputText.value = resultText
        }
      }
      
      // 错误处理
      if (data.status === 'error') {
        showNotification(data.error || '处理失败', 'error')
        outputText.value = ''
        break
      }
      
      // 完成
      if (data.status === 'success') {
        progress.value = 100
        progressMessage.value = '处理完成！'
        // 深度洗稿时，只取最终阶段（rewrite）的 result
        if (data.stage === 'polish') {
          // 第一次处理完成，不显示，继续等待第二次
          console.log('[Process] 第一阶段完成，等待第二阶段...')
        } else {
          if (data.result) {
            outputText.value = data.result
          }
          showNotification('处理成功！', 'success')
          updateMemberStatus()
        }
      }
    }
  } catch (err) {
    console.error('处理错误:', err)
    showNotification(err.message || '处理失败，请重试', 'error')
    outputText.value = ''
  } finally {
    isProcessing.value = false
    if (progress.value === 100) {
      setTimeout(() => {
        progressMessage.value = ''
      }, 2000)
    }
  }
}

const updateMemberStatus = async () => {
  try {
    const status = await tokenAPI.getMemberStatus()
    isMember.value = status.is_member
    remainingDays.value = status.remaining_days
    
    if (status.expire_date) {
      const date = new Date(status.expire_date)
      memberExpireDate.value = date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    } else {
      memberExpireDate.value = '会员已过期'
    }
  } catch (err) {
    console.error('获取会员状态失败:', err)
  }
}

const copyResult = async () => {
  if (!outputText.value) {
    warning('没有可复制的内容')
    return
  }

  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(outputText.value)
    } else {
      const textArea = document.createElement('textarea')
      textArea.value = outputText.value
      textArea.style.position = 'fixed'
      textArea.style.top = '-9999px'
      textArea.style.left = '-9999px'
      textArea.style.width = '2em'
      textArea.style.height = '2em'
      textArea.style.padding = '0'
      textArea.style.border = 'none'
      textArea.style.outline = 'none'
      textArea.style.boxShadow = 'none'
      textArea.style.background = 'transparent'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()

      try {
        const successful = document.execCommand('copy')
        if (!successful) throw new Error('execCommand failed')
      } finally {
        document.body.removeChild(textArea)
      }
    }
    success('已复制到剪贴板')
  } catch (err) {
    console.error('复制失败:', err)
    error('复制失败，请手动复制')
  }
}

const clearAll = () => {
  inputText.value = ''
  outputText.value = ''
  progress.value = 0
  progressMessage.value = ''
}

onMounted(() => {
  updateMemberStatus()
})
</script>

<style scoped>
.home-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 32px;
}

.welcome-section {
  margin-bottom: 32px;
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.1), rgba(243, 156, 18, 0.05));
  border: 1px solid rgba(230, 126, 34, 0.15);
}

.welcome-content {
  text-align: center;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-flex;
  align-items: center;
  gap: 16px;
}

.title-logo {
  width: 3rem;
  height: 3rem;
  border-radius: 8px;
  object-fit: contain;
  background: white;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.welcome-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(230, 126, 34, 0.1);
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-label {
  font-weight: 600;
  color: var(--text-primary);
}

.workspace-grid {
  display: grid;
  grid-template-columns: 55fr 45fr;
  gap: 28px;
  margin-bottom: 32px;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: fit-content;
}

.right-panel .output-section {
  flex: 1;
  min-height: 500px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.mode-selector {
  display: flex;
  gap: 8px;
}

.mode-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.88rem;
}

.mode-chip:hover {
  border-color: var(--primary-color);
  background: rgba(230, 126, 34, 0.05);
}

.mode-chip.active {
  border-color: var(--primary-color);
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.15), rgba(243, 156, 18, 0.1));
  box-shadow: 0 2px 12px rgba(230, 126, 34, 0.2);
}

.mode-chip-icon {
  font-size: 1rem;
}

.mode-chip-text {
  font-weight: 500;
  color: var(--text-primary);
}

.mode-chip-badge {
  padding: 2px 8px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  border-radius: 10px;
}

.mode-chip-badge.vip {
  background: linear-gradient(135deg, #e74c3c, #fd79a8);
}

.mode-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.mode-btn {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border: 2px solid rgba(230, 126, 34, 0.15);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.mode-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mode-btn:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.18);
}

.mode-btn:hover::before {
  opacity: 1;
}

.mode-btn.active {
  border-color: var(--primary-color);
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.12), rgba(243, 156, 18, 0.08));
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.25);
}

.mode-btn.active::before {
  opacity: 1;
}

.mode-icon {
  font-size: 2.5rem;
}

.mode-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mode-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
}

.mode-desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.mode-badge {
  padding: 6px 12px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 20px;
}

.mode-badge.vip {
  background: linear-gradient(135deg, #e74c3c, #fd79a8);
}

.textarea-wrapper {
  position: relative;
}

.text-input,
.text-output {
  width: 100%;
  min-height: 300px;
  max-height: 500px;
  padding: 20px;
  border: 2px solid rgba(230, 126, 34, 0.15);
  border-radius: 16px;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  overflow-y: auto;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  scrollbar-width: thin;
  scrollbar-color: rgba(230, 126, 34, 0.4) rgba(230, 126, 34, 0.1);
}

.text-input::-webkit-scrollbar,
.text-output::-webkit-scrollbar {
  width: 6px;
}

.text-input::-webkit-scrollbar-track,
.text-output::-webkit-scrollbar-track {
  background: rgba(230, 126, 34, 0.1);
  border-radius: 3px;
}

.text-input::-webkit-scrollbar-thumb,
.text-output::-webkit-scrollbar-thumb {
  background: rgba(230, 126, 34, 0.4);
  border-radius: 3px;
}

.text-input::-webkit-scrollbar-thumb:hover,
.text-output::-webkit-scrollbar-thumb:hover {
  background: rgba(230, 126, 34, 0.6);
}

.text-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(230, 126, 34, 0.12), 0 8px 24px rgba(230, 126, 34, 0.1);
}

.text-output {
  background: rgba(250, 250, 250, 0.95);
  cursor: default;
  border-color: rgba(230, 126, 34, 0.1);
}

.char-info {
  position: absolute;
  bottom: 12px;
  right: 12px;
  display: flex;
  gap: 12px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: white;
  padding: 4px 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.char-count {
  font-weight: 500;
}

.word-count {
  color: var(--primary-color);
  font-weight: 600;
}

.balance-section {
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.08), rgba(243, 156, 18, 0.05));
  border: 1px solid rgba(230, 126, 34, 0.12);
}

.balance-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.balance-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.balance-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.balance-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.balance-value {
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 0.9rem;
}

.actions {
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  padding: 14px 24px;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.3);
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(230, 126, 34, 0.45);
}

.btn-primary:hover:not(:disabled)::before {
  left: 100%;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: var(--primary-color);
  border: 2px solid rgba(230, 126, 34, 0.3);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(230, 126, 34, 0.08);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.15);
}

.btn-lg {
  padding: 16px 32px;
  font-size: 1.2rem;
}

.btn-outline {
  background: white;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  padding: 12px 24px;
  font-size: 1rem;
}

.btn-outline:hover:not(:disabled) {
  background: rgba(230, 126, 34, 0.05);
  transform: translateY(-2px);
}

.progress-area {
  margin-bottom: 20px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(230, 126, 34, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #e67e22, #f39c12);
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-text {
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.95rem;
  animation: pulse 2s infinite;
}

.output-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.output-stats {
  display: flex;
  gap: 12px;
}

.stat-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
}

.stat-badge.success {
  background: rgba(39, 174, 96, 0.1);
  color: var(--success);
}

.stat-badge.info {
  background: rgba(52, 152, 219, 0.1);
  color: var(--info);
}

.output-actions {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid rgba(230, 126, 34, 0.1);
  margin-top: 16px;
}

.output-actions .btn-outline {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 10px;
  background: white;
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.output-actions .btn-outline:hover {
  border-color: var(--primary-color);
  background: rgba(230, 126, 34, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(230, 126, 34, 0.15);
}

.output-actions .btn-outline:first-child {
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.1), rgba(243, 156, 18, 0.05));
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.empty-state {
  padding: 80px 30px;
  text-align: center;
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.03), rgba(243, 156, 18, 0.02));
  border-radius: 16px;
  border: 2px dashed rgba(230, 126, 34, 0.15);
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 20px;
  opacity: 0.8;
}

.empty-text {
  font-size: 1.2rem;
  color: var(--text-primary);
  margin-bottom: 10px;
  font-weight: 600;
}

.empty-hint {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }

  .welcome-stats {
    flex-direction: column;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 0 16px;
  }

  .welcome-title {
    font-size: 1.8rem;
  }

  .actions {
    flex-direction: column;
  }

  .output-actions {
    flex-direction: column;
  }

  .balance-info {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
