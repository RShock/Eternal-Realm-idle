import {defineStore} from 'pinia'
import {computed, ref} from 'vue'

export const useLogStore = defineStore('log', () => {
    // 状态
    const rawLogs = ref([])      // 原始日志数据
    const currentIndex = ref(-1)  // 当前播放到的日志索引
    const isPlaying = ref(false) // 是否正在播放

    // 方法
    const loadLogs = async () => {
        try {
            const response = await fetch('/log.json')
            rawLogs.value = await response.json()
        } catch (error) {
            console.error('日志加载失败:', error)
            rawLogs.value = []
        }
    }

    const startPlayback = () => {
        isPlaying.value = true
    }

    const pausePlayback = () => {
        isPlaying.value = false
    }

    const reset = () => {
        currentIndex.value = -1
        isPlaying.value = false
    }

    // 计算属性
    const currentLog = computed(() => {
        return rawLogs.value[currentIndex.value] || null
    })

    // 添加类型过滤方法
    const getLogsByType = (type) => {
        return rawLogs.value.filter(log => log.type === type)
    }

    return {
        rawLogs,
        currentIndex,
        isPlaying,
        loadLogs,
        startPlayback,
        pausePlayback,
        reset,
        currentLog,
        getLogsByType
    }
})