<template>
  <div class="log-controller">
    <button
        @click="togglePlay"
        :disabled="!isReady"
    >
      {{ isPlaying ? '暂停' : '播放' }}
    </button>
    <span>当前进度: {{ currentIndex + 1 }}/{{ total }}</span>
  </div>
</template>

<script setup>
import {useLogStore} from '@/stores/log'
import {computed, nextTick, onUnmounted, ref} from "vue";

const logStore = useLogStore()
const intervalId = ref(null)
const isReady = computed(() => logStore.rawLogs.length > 0)

// 计算属性
const currentIndex = computed(() => logStore.currentIndex)
const total = computed(() => logStore.rawLogs.length)
const isPlaying = computed(() => logStore.isPlaying)

const togglePlay = async () => {
  if (!isPlaying.value) {
    // 如果已经播放完，重置进度
    if (currentIndex.value >= total.value - 1) {
      logStore.reset()
    }
    startPlayback()
  } else {
    pausePlayback()
  }
}
// 修改后的processLogs方法
const processLogs = async () => {
  while (logStore.isPlaying && logStore.currentIndex < logStore.rawLogs.length - 1) {
    const currentIndex = logStore.currentIndex + 1
    const batch = logStore.getLogBatch(currentIndex)

    // 特殊处理连续deal_damage
    if (batch.type === 'deal_damage') {
      // 逐个处理但保持相同动画起始时间
      const startTime = Date.now()
      for (let i = 0; i < batch.count; i++) {
        logStore.currentIndex = currentIndex + i
        await nextTick() // 确保Vue更新
      }
      const duration = logStore.typeDurations.deal_damage * Math.min(batch.count, 3)
      const elapsed = Date.now() - startTime
      await new Promise(resolve => setTimeout(resolve, duration - elapsed))
    } else {
      logStore.currentIndex += batch.count
      const duration = logStore.typeDurations[batch.type] || logStore.typeDurations.default
      await new Promise(resolve => setTimeout(resolve, duration))
    }
  }
  pausePlayback()
}

const startPlayback = () => {
  logStore.startPlayback()
  processLogs()
}

const pausePlayback = () => {
  if (intervalId.value) {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
  logStore.pausePlayback()
}

// 组件销毁时清除计时器
onUnmounted(() => {
  pausePlayback()
})
</script>

<style scoped>
.log-controller {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 10px 20px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 20px;

  button {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;

    &:hover {
      background: #45a049;
    }

    &:disabled {
      background: #ccc;
      cursor: not-allowed;
    }
  }

  span {
    color: white;
    font-size: 14px;
  }
}
</style>