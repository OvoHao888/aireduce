import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import Home from '../views/Home.vue'
import PersonalCenter from '../views/PersonalCenter.vue'
import TokenCard from '../views/TokenCard.vue'
import UsageRecords from '../views/UsageRecords.vue'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: { title: '迅文 - AI智能双降平台' }
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    meta: { title: '登录 - 迅文' }
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    meta: { title: '注册 - 迅文' }
  },
  {
    path: '/workspace',
    name: 'Home',
    component: Home,
    meta: { title: '智能双降工作台' }
  },
  {
    path: '/home',
    redirect: '/workspace'
  },
  {
    path: '/personal',
    name: 'PersonalCenter',
    component: PersonalCenter,
    meta: { title: '个人中心' }
  },
  {
    path: '/token-card',
    name: 'TokenCard',
    component: TokenCard,
    meta: { title: '密卡中心' }
  },
  {
    path: '/records',
    name: 'UsageRecords',
    component: UsageRecords,
    meta: { title: '使用记录' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title + ' - 迅文' || '迅文'
  next()
})

export default router