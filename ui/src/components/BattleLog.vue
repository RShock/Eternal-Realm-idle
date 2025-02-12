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
import { ref, onMounted, onUnmounted } from 'vue'
import CardPreview from './CardPreview.vue'

const logs = ref([]) // 从log.json加载的原始数据
const displayLogs = ref([]) // 实际显示的日志
const logArea = ref(null)
let logIndex = 0
let intervalId = null

// 加载日志数据
const loadLogs = async () => {
  try {
    const response = await fetch('/log.json')
    const data = await response.json()
    logs.value = data.map(item => item.log) // 提取log字段
  } catch (error) {
    console.error('加载日志失败:', error)
    logs.value = ['日志加载失败']
  }
}

// 启动日志播放
const startLogPlayback = () => {
  intervalId = setInterval(() => {
    if (logIndex < logs.value.length) {
      displayLogs.value.push(logs.value[logIndex])
      scrollToBottom()
      logIndex++
    } else {
      clearInterval(intervalId)
    }
  }, 1000)
}

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
