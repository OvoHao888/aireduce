<template>
  <div class="api-config">
    <div class="page-header">
      <h2>API配置</h2>
      <p class="subtitle">配置AI服务的API参数，修改后需重启服务生效</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载配置中...</p>
    </div>

    <!-- 配置表单 -->
    <div v-else class="config-form">
      <div class="form-card">
        <h3>API基础配置</h3>
        
        <div class="form-group">
          <label>API Key</label>
          <div class="input-with-action">
            <input 
              :type="showApiKey ? 'text' : 'password'" 
              v-model="config.api_key"
              placeholder="请输入API Key"
              class="form-input"
            />
            <button @click="showApiKey = !showApiKey" class="btn-icon">
              {{ showApiKey ? '隐藏' : '显示' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Base URL</label>
          <input 
            type="text" 
            v-model="config.base_url"
            placeholder="https://api.example.com/v1"
            class="form-input"
          />
          <span class="hint">API服务地址，如: https://api.deepseek.com/v1</span>
        </div>

        <div class="form-group">
          <label>模型名称</label>
          <select v-model="config.model" class="form-select">
            <option v-for="model in supportedModels" :key="model" :value="model">
              {{ model }}
            </option>
            <option :value="config.model" v-if="!supportedModels.includes(config.model)">
              {{ config.model }} (自定义)
            </option>
          </select>
          <span class="hint">选择或输入模型名称</span>
        </div>
      </div>

      <div class="form-card">
        <h3>模型参数</h3>
        
        <div class="form-group">
          <label>Temperature (温度)</label>
          <input 
            type="number" 
            v-model="config.temperature"
            min="0"
            max="2"
            step="0.1"
            class="form-input"
          />
          <span class="hint">控制输出随机性，0-2之间，越高越随机</span>
        </div>

        <div class="form-group">
          <label>Max Tokens (最大Token数)</label>
          <input 
            type="number" 
            v-model="config.max_tokens"
            min="100"
            max="32000"
            step="100"
            class="form-input"
          />
          <span class="hint">单次请求最大输出Token数</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button @click="testConnection" class="btn-test" :disabled="testing">
          {{ testing ? '测试中...' : '测试连接' }}
        </button>
        <button @click="saveConfig" class="btn-save" :disabled="saving">
          {{ saving ? '保存中...' : '保存配置' }}
        </button>
      </div>

      <!-- 测试结果 -->
      <div v-if="testResult" class="test-result" :class="testResult.success ? 'success' : 'error'">
        <div class="result-header">
          <span class="icon">{{ testResult.success ? '✓' : '✗' }}</span>
          <span>{{ testResult.message }}</span>
        </div>
        <div v-if="testResult.response" class="result-detail">
          <strong>响应示例:</strong> {{ testResult.response }}
        </div>
      </div>

      <!-- 保存结果 -->
      <div v-if="saveResult" class="save-result" :class="saveResult.success ? 'success' : 'error'">
        <span class="icon">{{ saveResult.success ? '✓' : '✗' }}</span>
        {{ saveResult.message }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { configAPI } from '../utils/adminApi.js'

export default {
  name: 'ApiConfig',
  setup() {
    // 配置数据
    const config = ref({
      api_key: '',
      base_url: '',
      model: '',
      temperature: 1.0,
      max_tokens: 4096
    })

    // 支持的模型列表
    const supportedModels = ref([])

    // 状态
    const loading = ref(true)
    const saving = ref(false)
    const testing = ref(false)
    const showApiKey = ref(false)
    const testResult = ref(null)
    const saveResult = ref(null)

    // 获取API配置
    const fetchConfig = async () => {
      try {
        // 获取当前配置
        const configData = await configAPI.getApiConfig()
        config.value = configData

        // 获取支持的模型
        const modelsData = await configAPI.getSupportedModels()
        supportedModels.value = modelsData.models

      } catch (error) {
        alert('获取配置失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 测试连接
    const testConnection = async () => {
      testing.value = true
      testResult.value = null
      
      try {
        testResult.value = await configAPI.testApiConnection(config.value)
      } catch (error) {
        testResult.value = {
          success: false,
          message: '测试失败: ' + error.message
        }
      } finally {
        testing.value = false
      }
    }

    // 保存配置
    const saveConfig = async () => {
      saving.value = true
      saveResult.value = null
      
      try {
        const result = await configAPI.updateApiConfig(config.value)
        saveResult.value = {
          success: true,
          message: result.message
        }
      } catch (error) {
        saveResult.value = {
          success: false,
          message: '保存失败: ' + error.message
        }
      } finally {
        saving.value = false
      }
    }

    onMounted(() => {
      fetchConfig()
    })

    return {
      config,
      supportedModels,
      loading,
      saving,
      testing,
      showApiKey,
      testResult,
      saveResult,
      testConnection,
      saveConfig
    }
  }
}
</script>

<style scoped>
.api-config {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: #1a1a1a;
}

.subtitle {
  color: #666;
  margin: 0;
}

.loading-container {
  text-align: center;
  padding: 60px 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #e67e22;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.form-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(230, 126, 34, 0.08);
}

.form-card h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

.form-input,
.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid rgba(230, 126, 34, 0.2);
  border-radius: 10px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #e67e22;
}

.input-with-action {
  display: flex;
  gap: 8px;
}

.input-with-action .form-input {
  flex: 1;
}

.btn-icon {
  padding: 8px 12px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  color: #666;
}

.btn-icon:hover {
  background: #eee;
}

.hint {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #999;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.btn-test,
.btn-save {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-test {
  background: #fff;
  border: 2px solid #e67e22;
  color: #e67e22;
}

.btn-test:hover:not(:disabled) {
  background: rgba(230, 126, 34, 0.1);
}

.btn-save {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  border: none;
  color: white;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(230, 126, 34, 0.3);
}

.btn-test:disabled,
.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.test-result,
.save-result {
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 16px;
}

.test-result.success,
.save-result.success {
  background: #e8f5e9;
  border: 1px solid #c8e6c9;
  color: #2e7d32;
}

.test-result.error,
.save-result.error {
  background: #ffebee;
  border: 1px solid #ffcdd2;
  color: #c62828;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.icon {
  font-size: 18px;
}

.result-detail {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}
</style>
