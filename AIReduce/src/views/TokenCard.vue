<template>
  <div class="token-card-container">
    <div class="container">
      <!-- 页面标题 -->
      <GlassCard class="page-header" padding="32px">
        <div class="header-content">
          <h1 class="page-title">🎫 卡密中心</h1>
          <p class="page-subtitle">购买卡密后在此处兑换时长，开启高效降重之旅</p>
        </div>
      </GlassCard>

      <!-- 卡密购买提示 -->
      <GlassCard class="purchase-hint card-hover" padding="24px">
        <div class="hint-content">
          <div class="hint-icon">🛒</div>
          <div class="hint-text">
            <h3 class="hint-title">购买卡密</h3>
            <p class="hint-desc">卡密购买处：<a v-if="xianyuLink" :href="xianyuLink" target="_blank" class="xianyu-link">🐟 咸鱼链接</a><span v-else>🐟 咸鱼链接即将开放</span></p>
          </div>
        </div>
      </GlassCard>

      <!-- 时长套餐选择 -->
      <GlassCard class="duration-section" padding="32px">
        <div class="section-header">
          <span class="clock-icon">⏰</span>
          <h2 class="section-title">选择时长</h2>
        </div>

        <!-- 小时卡 -->
        <div v-if="hourCards.length" class="duration-grid">
          <div class="duration-card" v-for="item in hourCards" :key="item.id" :class="{ active: selectedItem === item.name, disabled: !item.is_active }" @click="item.is_active && selectPackage(item.name)">
            <div class="discount-tag">超值优惠</div>
            <div class="card-name">{{ item.name }}</div>
            <div class="card-price">¥{{ item.price }}</div>
            <div class="card-original">¥{{ item.original_price }}</div>
            <div class="discount-text">超值优惠</div>
          </div>
        </div>

        <!-- 天卡 -->
        <div v-if="dayCards.length" class="duration-grid">
          <div class="duration-card" v-for="item in dayCards" :key="item.id" :class="{ active: selectedItem === item.name, disabled: !item.is_active }" @click="item.is_active && selectPackage(item.name)">
            <div class="discount-tag">超值优惠</div>
            <div class="card-name">{{ item.name }}</div>
            <div class="card-price">¥{{ item.price }}</div>
            <div class="card-original">¥{{ item.original_price }}</div>
            <div class="discount-text">超值优惠</div>
          </div>
        </div>

        <!-- 月卡及以上 -->
        <div v-if="monthCards.length" class="duration-grid">
          <div class="duration-card" v-for="item in monthCards" :key="item.id" :class="{ active: selectedItem === item.name, recommended: item.recommended, disabled: !item.is_active }" @click="item.is_active && selectPackage(item.name)">
            <div v-if="item.recommended" class="recommend-tag">推荐</div>
            <div class="discount-tag">超值优惠</div>
            <div class="card-name">{{ item.name }}</div>
            <div class="card-price">¥{{ item.price }}</div>
            <div class="card-original">¥{{ item.original_price }}</div>
            <div class="discount-text">超值优惠</div>
          </div>
        </div>

      </GlassCard>

      <!-- 卡密兑换 -->
      <GlassCard class="redeem-section card-hover" padding="32px">
        <div class="redeem-header">
          <div class="redeem-icon">🎫</div>
          <div>
            <h2 class="section-title">卡密兑换</h2>
            <p class="section-desc">输入购买的卡密码兑换时长</p>
          </div>
        </div>

        <div class="redeem-form">
          <input
            v-model="cardCode"
            type="text"
            placeholder="请输入卡密码"
            class="input-field large"
            maxlength="20"
          />
          <button
            @click="redeemCard"
            :disabled="!cardCode || isRedeeming"
            class="btn btn-primary"
          >
            {{ isRedeeming ? '兑换中...' : '立即兑换' }}
          </button>
        </div>

        <div class="redeem-tips">
          <h4>💡 使用提示：</h4>
          <ul>
            <li>卡密码为8-20位字母和数字组合</li>
            <li>兑换后时长将直接添加到您的账户</li>
            <li>卡密有效期为购买后30天内激活</li>
            <li>如有疑问，请联系客服获取帮助</li>
          </ul>
        </div>
      </GlassCard>

      <!-- 购买须知 -->
      <GlassCard class="notice-section card-hover" padding="32px">
        <h2 class="section-title">📋 购买须知</h2>
        <div class="notice-grid">
          <div class="notice-item">
            <div class="notice-icon">🔒</div>
            <h4>安全支付</h4>
            <p>咸鱼平台担保交易，保障您的资金安全</p>
          </div>
          <div class="notice-item">
            <div class="notice-icon">💯</div>
            <h4>售后无忧</h4>
            <p>7天内无条件退款，无后顾之忧</p>
          </div>
          <div class="notice-item">
            <div class="notice-icon">⚡</div>
            <h4>即时生效</h4>
            <p>兑换后立即到账，无需等待</p>
          </div>
          <div class="notice-item">
            <div class="notice-icon">📱</div>
            <h4>多端同步</h4>
            <p>支持网页、手机等多端同时使用</p>
          </div>
        </div>
      </GlassCard>
    </div>

    <!-- 提示消息 -->
    <transition name="slide">
      <div v-if="showToast" :class="['toast', toastType]">
        {{ toastMessage }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GlassCard from '../components/GlassCard.vue'
import { tokenAPI } from '../utils/api'
import { showToast } from '../utils/toast'

const cardCode = ref('')
const isRedeeming = ref(false)
const selectedItem = ref('')
const allProducts = ref([])
const productsLoading = ref(false)

// 咸鱼链接配置
const xianyuLink = ref('')

// 按类型分组：小时卡 / 天卡 / 月卡及以上
const hourTypes = ['1hour', '3hour', '12hour']
const dayTypes = ['1day', '3day', '7day']

const hourCards = computed(() => allProducts.value.filter(p => hourTypes.includes(p.token_type)))
const dayCards = computed(() => allProducts.value.filter(p => dayTypes.includes(p.token_type)))
const monthCards = computed(() => {
  const rest = allProducts.value.filter(p => !hourTypes.includes(p.token_type) && !dayTypes.includes(p.token_type))
  // 标记推荐（sort_order 最小的启用套餐作为推荐）
  const activeRest = rest.filter(p => p.is_active)
  if (activeRest.length > 0) {
    const minOrder = Math.min(...activeRest.map(p => p.sort_order || 999))
    return rest.map(p => ({ ...p, recommended: p.is_active && (p.sort_order || 999) === minOrder }))
  }
  return rest.map(p => ({ ...p, recommended: false }))
})

// 选择套餐
const selectPackage = (packageName) => {
  selectedItem.value = packageName
}

const redeemCard = async () => {
  if (!cardCode.value) {
    showToast('请输入卡密码', 'error')
    return
  }
  
  if (cardCode.value.length < 8 || cardCode.value.length > 20) {
    showToast('卡密码应为8-20位', 'error')
    return
  }

  isRedeeming.value = true

  try {
    const response = await tokenAPI.exchangeCard(cardCode.value)
    
    if (response.success) {
      showToast(response.message, 'success')
      cardCode.value = ''
    } else {
      showToast(response.message, 'error')
    }
  } catch (error) {
    showToast(error.message || '兑换失败，请重试', 'error')
  } finally {
    isRedeeming.value = false
  }
}

const loadProducts = async () => {
  productsLoading.value = true
  try {
    const products = await tokenAPI.getProducts()
    allProducts.value = products || []
    // 默认选中第一个启用的套餐
    const firstActive = allProducts.value.find(p => p.is_active)
    if (firstActive && !selectedItem.value) {
      selectedItem.value = firstActive.name
    }
  } catch (error) {
    console.error('加载产品失败:', error)
    showToast('加载套餐失败，请刷新重试', 'error')
  } finally {
    productsLoading.value = false
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.token-card-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 32px;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  text-align: center;
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.1), rgba(243, 156, 18, 0.05));
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

/* 购买提示区域 */
.purchase-hint {
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(39, 174, 96, 0.05));
  border: 2px solid rgba(46, 204, 113, 0.2);
}

.hint-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hint-icon {
  font-size: 2.5rem;
}

.hint-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.hint-desc {
  font-size: 1rem;
  color: var(--text-secondary);
}

.xianyu-link {
  color: #27ae60;
  text-decoration: none;
  font-weight: 600;
}

.xianyu-link:hover {
  text-decoration: underline;
}

/* 时长套餐区域 */
.duration-section {
  background: white;
  padding: 24px !important;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.clock-icon {
  font-size: 1.3rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}

.section-desc {
  font-size: 1rem;
  color: var(--text-secondary);
}

.duration-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.duration-card {
  position: relative;
  padding: 24px 16px;
  background: #ffffff;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.duration-card:hover {
  border-color: #e67e22;
}

.duration-card.active {
  border-color: #e74c3c;
  background: #fff5f5;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.duration-card.recommended {
  border-color: #3498db;
}

.duration-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
  filter: grayscale(0.8);
}

.duration-card.disabled .card-price,
.duration-card.disabled .card-name {
  color: #999;
}

.recommend-tag {
  position: absolute;
  top: -2px;
  left: -2px;
  padding: 4px 10px;
  background: #3498db;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 6px 0 8px 0;
}

.discount-tag {
  position: absolute;
  top: -2px;
  right: -2px;
  padding: 4px 10px;
  background: #27ae60;
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 0 6px 0 8px;
}

.card-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #333;
  margin: 16px 0 12px;
}

.card-price {
  font-size: 2.5rem;
  font-weight: 700;
  color: #e74c3c;
  margin-bottom: 6px;
}

.card-original {
  font-size: 1rem;
  color: #999;
  text-decoration: line-through;
  margin-bottom: 4px;
}

.discount-text {
  font-size: 0.9rem;
  color: #27ae60;
  font-weight: 600;
  margin-top: 10px;
}

/* 兑换区域 */
.redeem-section {
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.05), rgba(243, 156, 18, 0.08));
}

.redeem-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.redeem-icon {
  font-size: 3rem;
}

.redeem-form {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.input-field.large {
  flex: 1;
  padding: 16px 24px;
  font-size: 1.1rem;
  border: 2px solid rgba(230, 126, 34, 0.3);
  border-radius: 12px;
  background: white;
  transition: all 0.3s;
}

.input-field.large:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.1);
}

.btn-primary {
  padding: 14px 32px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(230, 126, 34, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(230, 126, 34, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.redeem-tips {
  padding: 20px;
  background: rgba(243, 156, 18, 0.1);
  border-radius: 12px;
}

.redeem-tips h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.redeem-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.redeem-tips li {
  position: relative;
  padding-left: 24px;
  margin-bottom: 8px;
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.redeem-tips li::before {
  content: '•';
  position: absolute;
  left: 8px;
  color: var(--primary-color);
  font-weight: bold;
}

/* 购买须知 */
.notice-section {
  background: white;
}

.notice-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.notice-item {
  text-align: center;
  padding: 24px;
  background: #fafafa;
  border-radius: 12px;
  transition: all 0.3s;
}

.notice-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.1);
}

.notice-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}

.notice-item h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.notice-item p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.toast {
  position: fixed;
  top: 100px;
  right: 32px;
  padding: 16px 24px;
  border-radius: 12px;
  color: white;
  font-weight: 500;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 2000;
}

.toast.success {
  background: linear-gradient(135deg, #27ae60, #2ecc71);
}

.toast.error {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.toast.info {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

@media (max-width: 900px) {
  .duration-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .duration-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .token-card-container {
    padding: 0 16px;
  }

  .page-title {
    font-size: 1.8rem;
  }

  .hint-content {
    flex-direction: column;
    text-align: center;
  }

  .redeem-form {
    flex-direction: column;
  }

  .notice-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .notice-grid {
    grid-template-columns: 1fr;
  }
}
</style>
