import {defineStore} from 'pinia'
import {computed, ref} from 'vue'

export const useLogStore = defineStore('log', () => {
    // 状态
    const rawLogs = ref([])      // 原始日志数据
    const currentIndex = ref(-1)  // 当前播放到的日志索引
    const isPlaying = ref(false) // 是否正在播放
    const typeDurations = {
        add_player: 300,
        new_turn: 1500,
        play_card: 800,
        attack: 800,
        deal_damage: 500,
        destroy: 1000,
        default: 1000
    }

// 添加这个公共方法
    const getLogBatch = (startIndex) => {
        const startLog = rawLogs.value[startIndex]
        if (!startLog) return {count: 0}

        // 处理连续dealDamage的特殊情况
        if (startLog.type === 'deal_damage') {
            let count = 1
            while (rawLogs.value[startIndex + count]?.type === 'deal_damage') {
                count++
            }
            return {type: 'deal_damage', count}
        }

        return {type: startLog.type, count: 1}
    }

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
        getLogsByType,
        typeDurations,
        getLogBatch
    }
})