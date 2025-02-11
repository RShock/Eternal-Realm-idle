import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // 必须显式导入

export default defineConfig({
  plugins: [vue()],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/scss/styles.scss";` // 推荐添加全局scss文件
      }
    }
  },
  build: {
    assetsInlineLimit: 4096,
    outDir: '../dist', // 建议指定构建输出目录到外层
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // '~': path.resolve(__dirname, './public') // 可选添加其他别名
    }
  }
})

