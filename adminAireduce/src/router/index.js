import { createRouter, createWebHistory } from 'vue-router'
import AdminLayout from '../views/AdminLayout.vue'
import AdminLogin from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import UserManagement from '../views/UserManagement.vue'
import CardManagement from '../views/CardManagement.vue'
import ProductManagement from '../views/ProductManagement.vue'
import RecordManagement from '../views/RecordManagement.vue'
import FeedbackManagement from '../views/FeedbackManagement.vue'
import ApiConfig from '../views/ApiConfig.vue'

// 检查是否登录
const isAuthenticated = () => {
  const token = localStorage.getItem('admin_token')
  return !!token
}

const routes = [
  {
    path: '/login',
    name: 'AdminLogin',
    component: AdminLogin,
    meta: { title: '管理员登录', public: true }
  },
  {
    path: '/',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '统计概览' }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement,
        meta: { title: '用户管理' }
      },
      {
        path: 'cards',
        name: 'CardManagement',
        component: CardManagement,
        meta: { title: '卡密管理' }
      },
      {
        path: 'products',
        name: 'ProductManagement',
        component: ProductManagement,
        meta: { title: '套餐管理' }
      },
      {
        path: 'records',
        name: 'RecordManagement',
        component: RecordManagement,
        meta: { title: '使用记录' }
      },
      {
        path: 'feedbacks',
        name: 'FeedbackManagement',
        component: FeedbackManagement,
        meta: { title: '反馈管理' }
      },
      {
        path: 'api-config',
        name: 'ApiConfig',
        component: ApiConfig,
        meta: { title: 'API配置' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 认证检查
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = (to.meta.title || '管理后台') + ' - AIReduce管理后台'
  
  // 公开页面不需要认证
  if (to.meta.public) {
    // 如果已登录，跳转到首页
    if (to.path === '/login' && isAuthenticated()) {
      next('/')
    } else {
      next()
    }
    return
  }
  
  // 需要认证的页面
  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      // 未登录，跳转到登录页，保存原来要访问的路径
      next({ path: '/login', query: { redirect: to.fullPath } })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router