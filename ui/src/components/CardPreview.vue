<!-- src/components/CardPreview.vue -->
<template>
  <div id="card-preview">
    <h3>卡牌详情</h3>
    <img
      id="card-preview-image"
      :src="currentCard?.image || ''"
      :alt="currentCard?.name || '卡牌大图'"
    >
    <div v-if="currentCard" id="card-preview-info">
      <h4>{{ currentCard.name }}</h4>
      <p>{{ currentCard.description }}</p>
      <div class="card-stats">
        <span>攻击：{{ currentCard.attack }}</span>
        <span>生命：{{ currentCard.health }}</span>
      </div>
    </div>
    <div v-else class="placeholder">
      鼠标悬停卡牌查看详情
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentCard = ref(null)

// 示例数据
setTimeout(() => {
  currentCard.value = {
    name: '火球术',
    image: 'placeholder_card.png',
    attack: 3,
    health: 0,
    description: '对目标造成3点伤害'
  }
}, 1500)
</script>

<style scoped>
#card-preview {
  margin-top: 20px;
}

#card-preview-image {
  max-width: 100%;
  height: 200px;
  object-fit: contain;
}

#card-preview-info {
  margin-top: 10px;
  padding: 10px;
  background: rgba(0,0,0,0.3);
  border-radius: 4px;
}

.placeholder {
  color: #888;
  text-align: center;
  padding: 20px;
}

.card-stats {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}
</style>
