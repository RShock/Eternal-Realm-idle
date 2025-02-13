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
import {computed, onUnmounted, ref} from "vue";

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

const startPlayback = () => {
  logStore.startPlayback()
  intervalId.value = setInterval(() => {
    if (logStore.currentIndex < logStore.rawLogs.length - 1) {
      logStore.currentIndex++
    } else {
      pausePlayback()
    }
  }, 1000)
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