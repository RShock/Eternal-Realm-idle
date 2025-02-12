<template>
  <div class="log-controller">
    <button @click="start">开始播放</button>
    <span>当前进度: {{ currentIndex + 1 }}/{{ total }}</span>
  </div>
</template>

<script setup>
import { useLogStore } from '@/stores/log'
import {computed} from "vue";

const logStore = useLogStore()
let intervalId = null

const start = async () => {
  clearInterval(intervalId) // 先清除旧计时器
  await logStore.loadLogs()
  logStore.reset()

  // 统一在此处控制播放
  intervalId = setInterval(() => {
    if (logStore.currentIndex < logStore.rawLogs.length) {
      console.log(logStore.currentIndex)
      logStore.currentIndex++
    } else {
      clearInterval(intervalId)
    }
  }, 1000)
}

// 计算属性
const currentIndex = computed(() => logStore.currentIndex)
const total = computed(() => logStore.rawLogs.length)
</script>
