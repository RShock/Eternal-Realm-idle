<!-- src/components/BattleLog.vue -->
<template>
  <div class="sidebar">
    <h3>战斗日志</h3>
    <div id="log-area" ref="logArea">
      <div v-for="(log, index) in displayLogs" :key="index" class="log-item">
        {{ log }}
      </div>
    </div>
    <hr>
    <CardPreview />
  </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted, watch} from 'vue'
import CardPreview from './CardPreview.vue'

import { useLogStore } from '@/stores/log'

const logStore = useLogStore()
const displayLogs = ref([])
const logArea = ref(null)
let intervalId = null

// 监听播放进度
watch(() => logStore.currentIndex, (newIndex) => {
  const newLogs = logStore.rawLogs
    .slice(displayLogs.value.length, newIndex + 1)
    .map(log => log.log)

  displayLogs.value.push(...newLogs)
  scrollToBottom()
})

// 自动滚动
const scrollToBottom = () => {
  if (logArea.value) {
    // 使用nextTick确保DOM更新后滚动
    setTimeout(() => {
      logArea.value.scrollTop = logArea.value.scrollHeight
    }, 0)
  }
}

onMounted(() => {
  // startLogPlayback() // 注意这里不需要加 await
  logStore.loadLogs() // 只保留日志加载
})

onUnmounted(() => {
  clearInterval(intervalId)
  logStore.reset() // 清理状态
})
</script>

<!-- 样式部分保持不变 -->

<style scoped>
.sidebar {
  width: 34%;
  background: #444;
  color: white;
  padding: 20px;
  overflow-y: auto;
}

#log-area {
  min-height: 200px;
  max-height: 60vh;
  overflow-y: auto;
  margin-bottom: 20px;
}

.log-item {
  padding: 4px 0;
  border-bottom: 1px solid #666;
  font-size: 0.9em;
}
</style>
