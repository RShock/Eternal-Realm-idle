<!-- src/components/BattleLog.vue -->
<template>
  <div class="sidebar">
    <h3>战斗日志</h3>
    <div id="log-area" ref="logArea">
      <div v-for="(log, index) in logs" :key="index" class="log-item">
        {{ log }}
      </div>
    </div>
    <hr>
    <CardPreview />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CardPreview from './CardPreview.vue'

const logs = ref([
  '战斗开始！',
  '敌方召唤了水元素',
  '我方召唤了火精灵'
])

const logArea = ref(null)

onMounted(() => {
  // 自动滚动到底部
  const scrollToBottom = () => {
    if (logArea.value) {
      logArea.value.scrollTop = logArea.value.scrollHeight
    }
  }

  // 示例：添加新日志
  setTimeout(() => {
    logs.value.push('敌方英雄使用了寒冰箭')
    scrollToBottom()
  }, 1000)
})
</script>

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
