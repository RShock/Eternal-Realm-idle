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

// 监听播放进度
watch(() => logStore.currentIndex, (newIndex) => {
  if (newIndex < logStore.rawLogs.length) {
    displayLogs.value.push(logStore.rawLogs[newIndex].log)
    scrollToBottom()
  }
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

onMounted(async () => {
  await loadLogs()
  startLogPlayback()
})

onUnmounted(() => {
  clearInterval(intervalId) // 清除定时器防止内存泄漏
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
