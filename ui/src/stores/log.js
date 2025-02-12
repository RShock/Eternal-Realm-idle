import {defineStore} from 'pinia'
import {computed, ref} from 'vue'

export const useLogStore = defineStore('log', () => {
    // 状态
    const rawLogs = ref([])      // 原始日志数据
    const currentIndex = ref(0)  // 当前播放到的日志索引
    const isPlaying = ref(false) // 是否正在播放

    // 方法
    const loadLogs = async () => {
        try {
            const response = await fetch('/log.json')
            const data = await response.json()
            rawLogs.value = data
        } catch (error) {
            console.error('日志加载失败:', error)
            rawLogs.value = []
        }
    }

    const startPlayback = () => {
        isPlaying.value = true
    }

    const reset = () => {
        currentIndex.value = 0
        isPlaying.value = false
    }
    // 添加获取当前日志的方法
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
        reset,
        currentLog,
        getLogsByType
    }
})
