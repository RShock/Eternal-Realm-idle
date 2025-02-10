<!-- src/components/BattleCard.vue -->
<template>
  <div
    class="battle-card"
    :class="{ 'enemy-card': isEnemy, 'ally-card': !isEnemy }"
    @mouseenter="handleHover"
    @mouseleave="handleLeave"
  >
    <img :src="cardImage" class="card-image">
    <div class="stats-overlay">
      <span class="attack">{{ attack }}</span>
      <span class="health">{{ health }}</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { useCardStore } from '../stores/card' // 需要Pinia store管理状态

const props = defineProps({
  cardId: String,
  attack: Number,
  health: Number,
  cardImage: String,
  isEnemy: Boolean
})

const cardStore = useCardStore()

const handleHover = () => {
  cardStore.setPreviewCard({
    image: props.cardImage,
    attack: props.attack,
    health: props.health
  })
}

const handleLeave = () => {
  cardStore.clearPreviewCard()
}
</script>

<style scoped>
.battle-card {
  position: relative;
  width: 100px;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);

    &.ally-card {
      outline: 2px solid #66aaff;
    }

    &.enemy-card {
      outline: 2px solid #ff6666;
    }
  }
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stats-overlay {
      position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 6px;
    display: flex;
    justify-content: space-between;
    color: white;
  font-size: 14px;
}
</style>
