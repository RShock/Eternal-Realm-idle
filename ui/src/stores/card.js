// src/stores/card.js
import { defineStore } from 'pinia'

export const useCardStore = defineStore('card', {
  state: () => ({
    currentCard: null,       // 当前预览的卡牌数据
    previewVisible: false,   // 预览面板可见状态
  }),
  actions: {
    setPreviewCard(cardData) {
      this.currentCard = {
        ...cardData,
        name: cardData.name || '未命名卡牌',
        description: cardData.description || '暂无描述'
      }
      this.previewVisible = true
    },
    clearPreviewCard() {
      this.currentCard = null
      this.previewVisible = false
    }
  },
  getters: {
    cardStats: (state) => {
      return state.currentCard
        ? `攻:${state.currentCard.attack} 血:${state.currentCard.health}`
        : ''
    }
  }
})
