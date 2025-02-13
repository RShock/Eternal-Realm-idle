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
// 在useEntityStore中添加
    const findEntity = (id) => {
        const allPlayers = [...players.value.ally, ...players.value.enemy]
        const allCards = [...cards.value.ally, ...cards.value.enemy]
        return [...allPlayers, ...allCards].find(e => e.id === id)
    }
    return {players, cards, addPlayer, addCard, findEntity}
})
