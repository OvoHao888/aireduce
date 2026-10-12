<template>
  <div class="landing-page">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-inner">
        <div class="navbar-brand">
          <img src="/favicon.png" alt="迅文" class="nav-logo-img">
          <span class="nav-logo-text">迅文</span>
        </div>
        <div class="navbar-links">
          <a href="#" @click.prevent="scrollToSection('features')" class="nav-link">功能</a>
          <a href="#" @click.prevent="scrollToSection('how-it-works')" class="nav-link">使用流程</a>
          <a href="#" @click.prevent="scrollToSection('faq')" class="nav-link">常见问题</a>
        </div>
        <div class="navbar-actions">
          <button @click="goToLogin" class="btn btn-ghost btn-sm">登录</button>
          <button @click="goToRegister" class="btn btn-primary btn-sm">免费注册</button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content" ref="heroRef">
        <div class="hero-text">
          <div class="hero-badge">
            <span class="badge-icon">🎓</span>
            <span class="badge-text">科研工作者首选工具</span>
          </div>
          <h1 class="hero-title">
            <span class="title-highlight">迅文</span>
            <br>AI智能双降平台
          </h1>
          <p class="hero-subtitle">
            降重 · 降AI · 学术润色
          </p>
          <p class="hero-description">
            融合前沿AI技术，专为科研工作者打造的一站式学术写作辅助平台。
            智能降低重复率与AI痕迹率，让您的文稿更具原创性，顺利通过学术评审。
          </p>
          <!-- 核心指标 -->
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-icon">📊</span>
              <span class="stat-value">50-80%</span>
              <span class="stat-label">降重率</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">🎯</span>
              <span class="stat-value"><10%</span>
              <span class="stat-label">AI痕迹率</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">⚡</span>
              <span class="stat-value">30秒</span>
              <span class="stat-label">处理速度</span>
            </div>
          </div>
          <div class="hero-actions">
            <button @click="goToWorkspace" class="btn btn-primary btn-lg">
              立即开始
              <span class="btn-arrow">→</span>
            </button>
            <button @click="scrollToFeatures" class="btn btn-outline btn-lg">
              了解更多
            </button>
          </div>
        </div>
        <!-- 右侧演示卡片 -->
        <div class="hero-visual">
          <div class="demo-card">
            <div class="demo-header">
              <div class="demo-tabs">
                <span
                  class="tab"
                  :class="{ active: demoTab === 'mode1' }"
                  role="button"
                  tabindex="0"
                  @click="demoTab = 'mode1'"
                  @keydown.enter="demoTab = 'mode1'"
                >快速降重</span>
                <span
                  class="tab"
                  :class="{ active: demoTab === 'mode2' }"
                  role="button"
                  tabindex="0"
                  @click="demoTab = 'mode2'"
                  @keydown.enter="demoTab = 'mode2'"
                >深度降重</span>
              </div>
              <span class="demo-badge">实时预览</span>
            </div>
            <div class="demo-input">
              <textarea readonly placeholder="输入或粘贴需要降重的文本...">随着人工智能技术的快速发展，深度学习在自然语言处理领域取得了显著的突破性进展。近年来，基于Transformer架构的大规模预训练语言模型展现出了强大的文本生成和理解能力。</textarea>
            </div>
            <div class="demo-output">
              <div class="output-label">✨ 降重结果</div>
              <p class="output-text">{{ demoPreview[demoTab].output }}</p>
            </div>
            <div class="demo-actions">
              <div class="demo-stats-row">
                <span class="demo-stat">重复率 <strong>{{ demoPreview[demoTab].duplicate }}</strong></span>
                <span class="demo-stat">AI率 <strong>{{ demoPreview[demoTab].aiRate }}</strong></span>
                <span class="demo-stat success">✅ 顺利通过</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 向下滚动指示器 -->
      <div class="scroll-indicator" @click="scrollToFeatures">
        <span>向下滚动</span>
        <div class="scroll-arrow">↓</div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section" ref="featuresRef" id="features">
      <div class="section-header">
        <h2 class="section-title">核心功能</h2>
        <p class="section-subtitle">为什么选择迅文</p>
      </div>
      <div class="features-grid">
        <div class="feature-card" v-for="(feature, index) in features" :key="index" :data-delay="index * 100">
          <div class="feature-icon">{{ feature.icon }}</div>
          <div class="feature-highlight">{{ feature.highlight }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-description">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Stats Section (新增) -->
    <section class="stats-section">
      <div class="section-header">
        <h2 class="section-title">数据说话</h2>
        <p class="section-subtitle">用实力证明品质</p>
      </div>
      <div class="stats-content">
        <div class="stats-grid">
          <div class="stat-card" v-for="(stat, index) in stats" :key="index" :data-delay="index * 100">
            <div class="stat-icon">{{ stat.icon }}</div>
            <div class="stat-number">{{ stat.number }}</div>
            <div class="stat-label">{{ stat.label }}</div>
            <p class="stat-desc">{{ stat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section" id="how-it-works">
      <div class="section-header">
        <h2 class="section-title">使用流程</h2>
        <p class="section-subtitle">简单三步，轻松完成</p>
      </div>
      <div class="steps-grid">
        <div class="step-card" v-for="(step, index) in steps" :key="index" :data-delay="index * 150">
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-icon">{{ step.icon }}</div>
          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-description">{{ step.description }}</p>
          <div class="step-time">{{ step.time }}</div>
        </div>
      </div>
    </section>

    <!-- Comparison Section (新增) -->
    <section class="comparison-section">
      <div class="section-header">
        <h2 class="section-title">对比传统方案</h2>
        <p class="section-subtitle">迅文 vs 传统降重方式</p>
      </div>
      <div class="comparison-grid">
        <div class="comparison-card" :data-delay="0">
          <h3 class="card-title">❌ 传统方式</h3>
          <div class="comparison-items">
            <div class="item" v-for="(item, i) in comparisonBad" :key="'b'+i">
              <span class="item-label">{{ item.label }}</span>
              <span class="item-status bad">{{ item.value }}</span>
            </div>
          </div>
        </div>
        <div class="comparison-card our" :data-delay="200">
          <div class="card-badge">推荐</div>
          <h3 class="card-title">✅ 迅文平台</h3>
          <div class="comparison-items">
            <div class="item" v-for="(item, i) in comparisonGood" :key="'g'+i">
              <span class="item-label">{{ item.label }}</span>
              <span class="item-status good">{{ item.value }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>



    <!-- Advantages Section -->
    <section class="advantages-section">
      <div class="section-header">
        <h2 class="section-title">平台优势</h2>
        <p class="section-subtitle">我们的承诺</p>
      </div>
      <div class="advantages-grid">
        <div class="advantage-card" v-for="(advantage, index) in advantages" :key="index" :data-delay="index * 100">
          <div class="advantage-icon">{{ advantage.icon }}</div>
          <h3 class="advantage-title">{{ advantage.title }}</h3>
          <p class="advantage-description">{{ advantage.description }}</p>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section" ref="faqRef" id="faq">
      <div class="section-header">
        <h2 class="section-title">常见问题</h2>
        <p class="section-subtitle">您可能想了解的问题</p>
      </div>
      <div class="faq-list">
        <div 
          class="faq-item" 
          v-for="(faq, index) in faqs" 
          :key="index"
          :data-delay="index * 100"
          :class="{ active: activeFaq === index }"
          @click="toggleFaq(index)"
        >
          <div class="faq-header">
            <span class="faq-question">{{ faq.question }}</span>
            <span class="faq-icon">{{ activeFaq === index ? '−' : '+' }}</span>
          </div>
          <div class="faq-answer">{{ faq.answer }}</div>
        </div>
      </div>
    </section>

    <!-- CTA Section (新增) -->
    <section class="cta-section">
      <div class="cta-content">
        <h2 class="cta-title">准备好提升您的文稿质量了吗？</h2>
        <p class="cta-subtitle">立即体验迅文AI智能双降平台，让学术写作更轻松</p>
        <button @click="goToWorkspace" class="btn btn-primary btn-lg cta-btn">
          免费开始使用 →
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer-section">
      <div class="footer-content">
        <div class="footer-logo">
          <img src="/favicon.png" alt="迅文" class="footer-logo-img">
          <span class="footer-logo-text">迅文</span>
        </div>
        <div class="footer-links">
          <a href="#" class="footer-link">功能介绍</a>
          <a href="#" class="footer-link">使用教程</a>
          <a href="#" class="footer-link">关于我们</a>
          <a href="#" class="footer-link">联系我们</a>
        </div>
        <div class="footer-copyright">
          © 2026 迅文. 保留所有权利.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Scroll refs
const heroRef = ref(null)
const featuresRef = ref(null)
const faqRef = ref(null)

// FAQ active state
const activeFaq = ref(0)

// 首屏演示卡片：快速 / 深度 两种模式的效果对照
const demoTab = ref('mode1')
const demoPreview = {
  mode1: {
    output: '伴随AI技术的迅猛演进，深度学习于NLP领域实现了重大突破。近些年来，依托Transformer框架的大规模预训练语言模型呈现出卓越的文本生成与理解性能。',
    duplicate: '32% → 8%',
    aiRate: '45% → 5%'
  },
  mode2: {
    output: '近年来，人工智能技术的迭代速度显著加快，其中深度学习在自然语言处理方向上的推进尤为突出。以Transformer为核心架构的大规模预训练模型，凭借其在文本生成与语义理解两方面的出色表现，已成为支撑该领域发展的关键技术。',
    duplicate: '32% → 5%',
    aiRate: '45% → 2%'
  }
}

// Features data - 4个卡片，对照数据说话样式
const features = [
  {
    icon: '🔄',
    highlight: '降重率50%-80%',
    title: '智能降重',
    description: '基于AI深度学习，智能分析文本相似度，提供多种改写方案，高效降低重复率，保持学术严谨性。'
  },
  {
    icon: '🤖',
    highlight: 'AI率 <10%',
    title: '降AI率',
    description: '先进的人性化改写算法，有效降低文本中的AI生成痕迹，让文章更自然、更符合人工写作风格。'
  },
  {
    icon: '✨',
    highlight: '专业级润色',
    title: '学术润色',
    description: '专业学术编辑团队支持，优化文章结构，规范专业术语，提升论文整体质量。'
  },
  {
    icon: '🚀',
    highlight: '30秒响应',
    title: '极速处理',
    description: '分布式处理架构，30秒内完成文本分析与改写，支持批量处理，节省宝贵时间。'
  }
]

// Stats data (新增)
const stats = [
  { icon: '📊', number: '50%–80%', label: '平均降重率', desc: '智能语义改写，保持原意' },
  { icon: '🎯', number: '<10%', label: 'AI痕迹率', desc: '自然流畅通过审核' },
  { icon: '⚡', number: '30s', label: '平均处理时间', desc: '极速响应，立等可取' },
  { icon: '🔒', number: '100%', label: '数据安全', desc: 'AES-256加密存储' }
]

// Steps data (增强)
const steps = [
  { icon: '📝', title: '粘贴文本', description: '将需要处理的文本粘贴到输入框中，支持Word、PDF等多种格式内容。', time: '约10秒' },
  { icon: '⚙️', title: '选择模式', description: '根据需求选择「快速降重」或「深度降重」模式，系统自动匹配最优策略。', time: '约5秒' },
  { icon: '✅', title: '获取结果', description: '系统智能处理后输出结果，可直接复制或下载，一键完成全部操作。', time: '约15秒' }
]

// Comparison data (新增)
const comparisonBad = [
  { label: '降重效果', value: '差' },
  { label: '保持原意', value: '容易曲解' },
  { label: '处理速度', value: '数小时' },
  { label: '安全性', value: '有泄露风险' },
  { label: '价格', value: '昂贵' }
]
const comparisonGood = [
  { label: '降重效果', value: '优秀' },
  { label: '保持原意', value: '高度保真' },
  { label: '处理速度', value: '30秒内' },
  { label: '安全性', value: '端到端加密' },
  { label: '价格', value: '实惠透明' }
]



// Advantages data
const advantages = [
  { icon: '🔬', title: '学术级算法', description: '针对学术论文场景专项优化，理解学科术语和专业表达习惯，避免通用改写工具的"外行感"。' },
  { icon: '💡', title: '多策略引擎', description: '融合同义词替换、句式重构、语序调整、段落重组等多重策略，确保改写结果的多样性和自然度。' },
  { icon: '📐', title: '格式保留', description: '完美保留原文档格式，包括引用标注、公式编号、图表说明等，无需二次排版调整。' },
  { icon: '🛡️', title: '隐私保护', description: '采用零知识证明理念设计，处理完成后数据自动销毁，不留任何痕迹，您的知识产权绝对安全。' }
]

// FAQ data
const faqs = [
  {
    question: '迅文降重效果如何？',
    answer: '我们的降重功能基于深度语义理解模型，可以在保持原文意思的同时提供多种自然改写方案。降重率通常可以达到50%-80%，同时保持文章的学术性和专业性。'
  },
  {
    question: '迅文降低AI率效果如何？',
    answer: '迅文采用先进的人性化改写模型，可以有效降低AI痕迹率，使文章更符合人工写作风格。降AI率效果显著，通常可以降到10%以下。'
  },
  {
    question: '降重与降AI率可以同时使用吗?',
    answer: '可以的！如果您的文章AI生成痕迹较重，可以先使用降AI率功能；如果重复率较高，可以使用降重功能。建议先降重，再降AI率，效果更佳。'
  },
  {
    question: '我的文章会泄露吗?',
    answer: '放心，迅文采用业界领先的加密技术保护您的数据安全。所有数据传输都使用SSL加密，存储的数据采用AES-256加密。我们严格遵守数据保护法规，不会将您的数据用于任何未经授权的用途。'
  },
  {
    question: '支持哪些文档格式?',
    answer: '目前支持纯文本直接粘贴处理。对于Word、PDF等格式，建议先将文本内容复制到输入框中使用。我们正在开发更多格式的原生支持，敬请期待。'
  },
  {
    question: '处理后的文章质量如何保证?',
    answer: '迅文采用多轮校验机制，每段改写结果都会经过语法检查、语义一致性验证和学术规范审核。同时提供预览对比功能，您可以逐段确认满意后再导出。'
  }
]

// Methods
const goToWorkspace = () => {
  router.push('/workspace')
}

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const scrollToFeatures = () => {
  scrollToSection('features')
}

const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? -1 : index
}

// 通用锚点平滑滚动（统一处理导航栏高度）
const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (!el) return
  const navbarHeight = 80
  const elementPosition = el.getBoundingClientRect().top + window.pageYOffset
  window.scrollTo({
    top: elementPosition - navbarHeight,
    behavior: 'smooth'
  })
}

// Scroll animations
let observer = null

const setupScrollAnimation = () => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const children = entry.target.querySelectorAll('.feature-card, .stat-card, .step-card, .advantage-card, .faq-item, .comparison-card')
        
        if (entry.isIntersecting) {
          // 进入视口：播放入场动画
          children.forEach((child, i) => {
            const delay = parseInt(child.dataset.delay || 0) || i * 120
            setTimeout(() => {
              child.classList.remove('pre-animate', 'animate-in')
              void child.offsetWidth // 强制回流，重新触发动画
              child.classList.add('animate-in')
            }, delay)
          })
          // section 本身也加动画（无子卡片时）
          if (children.length === 0) {
            entry.target.classList.add('animate-in')
          }
        } else {
          // 离开视口：重置状态，以便重新进入时再次播放动画
          children.forEach((child) => {
            child.classList.remove('animate-in')
            child.classList.add('pre-animate')
          })
        }
      })
    },
    {
      threshold: 0.08,
      rootMargin: '0px 0px -40px 0px'
    }
  )

  const sections = document.querySelectorAll('.features-section, .stats-section, .how-it-works-section, .comparison-section, .advantages-section, .faq-section, .cta-section')
  sections.forEach((section) => {
    if (section) {
      // 初始隐藏子元素（用 class 而非内联 style，避免优先级冲突）
      const children = section.querySelectorAll('.feature-card, .stat-card, .step-card, .advantage-card, .faq-item, .comparison-card')
      children.forEach((child) => {
        child.classList.add('pre-animate')
      })
      observer.observe(section)
    }
  })
}

onMounted(() => {
  setupScrollAnimation()
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
/* ===== Hero Section ===== */
.hero-section {
  min-height: 100vh;
  padding: 150px 32px;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #fdfbf7 0%, #faf5ef 50%, #fdf6e3 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(230, 126, 34, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(243, 156, 18, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(231, 76, 60, 0.05) 0%, transparent 40%);
}

.hero-content {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 56px;
  align-items: center;
  position: relative;
  z-index: 1;
  min-height: 0;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(39, 174, 96, 0.1), rgba(46, 204, 113, 0.1));
  border: 1px solid rgba(39, 174, 96, 0.2);
  padding: 10px 20px;
  border-radius: 30px;
  margin-bottom: 14px;
}

.badge-icon { font-size: 1.2rem; }

.badge-text {
  font-size: 0.95rem;
  color: #27ae60;
  font-weight: 600;
}

.hero-text {
  animation: slideInLeft 0.8s ease-out;
}

.hero-title {
  font-size: 2.6rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.15;
}

.title-highlight {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 8px;
  letter-spacing: 2px;
}

.hero-description {
  font-size: 0.98rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 14px;
  max-width: 500px;
}

/* 数据统计 */
.hero-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 18px;
}

.stat-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-icon { font-size: 1.6rem; }

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* 按钮 */
.hero-actions {
  display: flex;
  gap: 16px;
}

.btn-arrow {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.btn:hover .btn-arrow {
  transform: translateX(4px);
}

/* 右侧演示卡片 */
.hero-visual {
  animation: slideInRight 0.8s ease-out 0.2s both;
}

.demo-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 14px;
  box-shadow: 0 20px 60px rgba(230, 126, 34, 0.15);
  border: 1px solid rgba(230, 126, 34, 0.1);
}

.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.demo-tabs {
  display: flex;
  gap: 8px;
}

.tab {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  background: rgba(230, 126, 34, 0.1);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab.active {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  cursor: default;
}

.tab:not(.active):hover {
  background: rgba(230, 126, 34, 0.2);
  color: var(--primary-color);
}

.demo-badge {
  background: linear-gradient(135deg, #27ae60, #2ecc71);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.demo-input textarea {
  width: 100%;
  min-height: 100px;
  padding: 14px;
  border: 2px solid rgba(230, 126, 34, 0.15);
  border-radius: 12px;
  font-size: 0.88rem;
  line-height: 1.6;
  resize: none;
  background: rgba(250, 250, 250, 0.9);
  transition: all 0.3s ease;
  color: var(--text-secondary);
  font-family: inherit;
}

.demo-input textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.demo-output {
  margin-top: 14px;
  padding: 14px;
  background: linear-gradient(135deg, rgba(39, 174, 96, 0.05), rgba(46, 204, 113, 0.05));
  border-radius: 12px;
  border: 1px solid rgba(39, 174, 96, 0.15);
}

.output-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #27ae60;
  margin-bottom: 6px;
}

.output-text {
  font-size: 0.88rem;
  line-height: 1.65;
  color: var(--text-primary);
  margin: 0;
}

.demo-actions {
  margin-top: 14px;
}

.demo-stats-row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.demo-stat {
  font-size: 0.82rem;
  color: var(--text-secondary);
  background: rgba(230, 126, 34, 0.06);
  padding: 6px 12px;
  border-radius: 8px;
}

.demo-stat strong {
  color: var(--primary-color);
}

.demo-stat.success {
  color: #27ae60;
  font-weight: 600;
  background: rgba(39, 174, 96, 0.08);
}

.scroll-indicator {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  animation: bounce 2s ease-in-out infinite;
}

.scroll-indicator span {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.scroll-arrow {
  font-size: 1.4rem;
  color: var(--primary-color);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(10px); }
}

/* ===== 导航栏 ===== */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(230, 126, 34, 0.08);
  padding: 12px 32px;
}

.navbar-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-logo-img {
  width: 28px;
  height: 28px;
  border-radius: 8px;
}

.nav-logo-text {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
}

.navbar-links {
  display: flex;
  gap: 28px;
}

.nav-link {
  font-size: 0.9rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  color: var(--primary-color);
}

.navbar-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-ghost {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid rgba(230, 126, 34, 0.2);
}

.btn-ghost:hover:not(:disabled) {
  background: rgba(230, 126, 34, 0.06);
  border-color: var(--primary-color);
}

.btn-sm {
  padding: 8px 20px;
  font-size: 0.88rem;
}

/* ===== Section 通用样式（减少padding）===== */
section {
  padding: 28px 24px;
  opacity: 1;
  transform: translateY(0);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  scroll-margin-top: 80px;
}

section.animate-in {
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(36px) scale(0.97);
    filter: blur(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }
}

.section-header {
  text-align: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 1.95rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.section-subtitle {
  font-size: 1.05rem;
  color: var(--text-secondary);
}

/* ===== Features Section - 对照数据说话样式 ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 0 auto;
}

/* ===== Features Section - 对照数据说话样式 ===== */
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 0 auto;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 20px 14px 16px;
  text-align: center;
  border: 1px solid rgba(230, 126, 34, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #e67e22, #f39c12);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(230, 126, 34, 0.12);
}

.feature-card:hover::before {
  opacity: 1;
}

/* 动画前置状态（替代内联 style） */
.pre-animate {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.feature-card.animate-in,
.stat-card.animate-in,
.step-card.animate-in,
.advantage-card.animate-in,
.faq-item.animate-in,
.comparison-card.animate-in {
  opacity: 1 !important;
  transform: translateY(0) !important;
}

.feature-icon {
  font-size: 2.2rem;
  margin-bottom: 10px;
}

.feature-highlight {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  line-height: 1.2;
}

.feature-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.feature-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0;
}

/* ===== Stats Section (新增) ===== */
.stats-section {
  background: linear-gradient(135deg, rgba(230, 126, 34, 0.07), rgba(243, 156, 18, 0.04));
}

.stats-content {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 20px 14px 16px;
  text-align: center;
  border: 1px solid rgba(230, 126, 34, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #e67e22, #f39c12);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(230, 126, 34, 0.12);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card.animate-in {
  opacity: 1 !important;
  transform: translateY(0) !important;
}

.stat-icon {
  font-size: 1.8rem;
  margin-bottom: 6px;
}

.stat-number {
  font-size: 1.9rem;
  font-weight: 800;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.95rem;
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 4px;
}

.stat-desc {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin: 0;
}

/* ===== How It Works Section ===== */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  max-width: 1100px;
  margin: 0 auto;
}

.step-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  border: 1px solid rgba(230, 126, 34, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.step-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(230, 126, 34, 0.12);
}

.step-number {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
}

.step-icon {
  font-size: 2.2rem;
  margin-bottom: 8px;
}

.step-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.step-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 8px;
}

.step-time {
  display: inline-block;
  font-size: 0.82rem;
  color: var(--primary-color);
  font-weight: 600;
  background: rgba(230, 126, 34, 0.08);
  padding: 4px 14px;
  border-radius: 20px;
}

/* ===== Comparison Section (新增) ===== */
.comparison-section {
  background: linear-gradient(135deg, #faf5ef, #fdf6e3);
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  max-width: 860px;
  margin: 0 auto;
}

.comparison-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 18px;
  border: 2px solid rgba(230, 126, 34, 0.1);
  position: relative;
}

.comparison-card.animate-in {
  opacity: 1 !important;
  transform: translateY(0) !important;
}

.comparison-card.our {
  border-color: var(--primary-color);
  box-shadow: 0 8px 24px rgba(230, 126, 34, 0.15);
}

.card-badge {
  position: absolute;
  top: -12px;
  right: 24px;
  background: linear-gradient(135deg, #e67e22, #f39c12);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.comparison-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: rgba(230, 126, 34, 0.04);
  border-radius: 10px;
}

.item-label {
  font-size: 0.92rem;
  color: var(--text-primary);
}

.item-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 600;
}

.item-status.good {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.item-status.bad {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}



/* ===== Advantages Section ===== */
.advantages-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  max-width: 1400px;
  margin: 0 auto;
}

.advantage-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 22px 14px 18px;
  text-align: center;
  border: 1px solid rgba(230, 126, 34, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.advantage-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #e67e22, #f39c12);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.advantage-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(230, 126, 34, 0.12);
}

.advantage-card:hover::before {
  opacity: 1;
}

.advantage-icon {
  font-size: 2.2rem;
  margin-bottom: 10px;
}

.advantage-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.advantage-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.55;
}

/* ===== FAQ Section ===== */
.faq-list {
  max-width: 760px;
  margin: 0 auto;
}

.faq-item {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 10px;
  border: 1px solid rgba(230, 126, 34, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.faq-item.animate-in {
  opacity: 1 !important;
  transform: translateY(0) !important;
}

.faq-item:hover {
  border-color: rgba(230, 126, 34, 0.3);
}

.faq-item.active {
  border-color: var(--primary-color);
  box-shadow: 0 4px 16px rgba(230, 126, 34, 0.1);
}

.faq-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.faq-question {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.faq-icon {
  font-size: 1.5rem;
  color: var(--primary-color);
  font-weight: 300;
  transition: transform 0.3s ease;
  flex-shrink: 0;
  margin-left: 16px;
}

.faq-answer {
  margin-top: 12px;
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.6;
  display: none;
  animation: fadeInAnswer 0.3s ease;
}

.faq-item.active .faq-answer {
  display: block;
}

@keyframes fadeInAnswer {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== CTA Section (新增) ===== */
.cta-section {
  background: linear-gradient(135deg, #e67e22, #f39c12);
  padding: 28px 32px;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 1.65rem;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
}

.cta-subtitle {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 28px;
}

.cta-btn {
  background: white;
  color: #e67e22;
  font-size: 1.1rem;
}

.cta-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
}

/* ===== Footer ===== */
.footer-section {
  background: var(--text-primary);
  padding: 32px 32px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 18px;
}

.footer-logo-img {
  width: 28px;
  height: 28px;
  border-radius: 8px;
}

.footer-logo-text {
  font-size: 1.35rem;
  font-weight: 700;
  color: white;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 28px;
  margin-bottom: 18px;
}

.footer-link {
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: white;
}

.footer-copyright {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
}

/* ===== Animations ===== */
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-30px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}

/* ===== Button Styles ===== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 28px;
  font-size: 1.05rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
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
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(230, 126, 34, 0.45);
}

.btn-outline {
  background: rgba(255, 255, 255, 0.9);
  color: var(--primary-color);
  border: 2px solid rgba(230, 126, 34, 0.3);
  backdrop-filter: blur(10px);
}

.btn-outline:hover:not(:disabled) {
  background: rgba(230, 126, 34, 0.08);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.btn-lg {
  padding: 16px 32px;
  font-size: 1.1rem;
}

/* ===== Responsive ===== */
@media (max-width: 1200px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-text { order: 1; }
  .hero-visual { order: 2; }

  .hero-title { font-size: 2.6rem; }
  .hero-description { max-width: 100%; }
  .hero-stats { justify-content: center; }
  .hero-actions { justify-content: center; }

  .features-grid { grid-template-columns: repeat(2, 1fr); }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .advantages-grid { grid-template-columns: repeat(2, 1fr); }

}

@media (max-width: 768px) {
  section { padding: 28px 16px; }

  .navbar { padding: 10px 16px; }
  .navbar-links { display: none; }

  .hero-section { padding: 56px 16px 80px; min-height: 100vh; }
  .hero-title { font-size: 2rem; }
  .hero-subtitle { font-size: 1.2rem; }
  .hero-stats { gap: 20px; flex-wrap: wrap; }
  .hero-actions { flex-direction: column; }

  .features-grid,
  .stats-grid,
  .advantages-grid { grid-template-columns: 1fr; }
  .steps-grid { grid-template-columns: 1fr; }
  .comparison-grid { grid-template-columns: 1fr; }


  .section-title { font-size: 1.75rem; }
  .cta-title { font-size: 1.45rem; }

  .footer-links { flex-wrap: wrap; gap: 12px; }

  .demo-card { padding: 16px; }
  .demo-stats-row { flex-wrap: wrap; gap: 6px; }
}
</style>
