// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  css: {
    preprocessorOptions: {
      scss: {
        // additionalData: `@import "./src/scss/_variables.scss";` // 全局scss变量文件
      }
    }
  },
  build: {
    assetsInlineLimit: 4096 // 小于4KB的资源转base64
  }
})
