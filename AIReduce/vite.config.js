import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // 放行所有 cpolar 域名，解决被拦截问题
    allowedHosts: true,
    // 代理后端接口，让外网能正常请求你的 FastAPI
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
