import {defineStore} from 'pinia'
import {ref} from 'vue'

export const useEntityStore = defineStore('entities', () => {
    const players = ref({
        ally: [],
        enemy: []
    })

    const cards = ref({
        ally: [],
        enemy: []
    })
    const currentTurnInfo = ref(null)

    const setTurnInfo = (info) => {
        currentTurnInfo.value = {
            ...currentTurnInfo.value, // 保留旧值
            ...info // 新值覆盖
        }
    }
    // 添加玩家
    const addPlayer = (playerData) => {
        const target = playerData.part === 'ally' ? 'ally' : 'enemy'
        players.value[target].push({
            ...playerData,
            visible: false // 用于入场动画控制
        })
    }

    // 添加卡牌
    const addCard = (cardData, playerPart) => {
        const target = playerPart === 'ally' ? 'ally' : 'enemy'
        cards.value[target].push({
            ...cardData,
            visible: false
        })
    }
    const removeEntity = (id) => {
        // 从玩家列表移除
        ['ally', 'enemy'].forEach(side => {
            players.value[side] = players.value[side].filter(p => p.id !== id)
            cards.value[side] = cards.value[side].filter(c => c.id !== id)
        })
    }

    const updateHealth = (id, newHealth) => {
        const entity = findEntity(id)
        if (entity) {
            entity.health = newHealth
        } else {
            console.error(`未找到实体：${id}`)
        }
    }
    const findEntity = (id) => {
        const allPlayers = [...players.value.ally, ...players.value.enemy]
        const allCards = [...cards.value.ally, ...cards.value.enemy]
        return [...allPlayers, ...allCards].find(e => e.id === id)
    }
    return {
        players, cards, addPlayer, addCard, findEntity, updateHealth, removeEntity, currentTurnInfo,
        setTurnInfo
    }
})
