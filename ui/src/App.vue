<!-- src/App.vue -->
<template>
  <div class="main-layout">
    <BattleLog />

    <div class="battle-container">
      <!-- 敌方区域 -->
      <div class="avatar_row enemy-area">
        <AvatarPlayer
          type="enemy"
          avatar-image="/path_to_enemy_avatar.png"
          :attack="0"
          :health="20"
          :manas="[{ type: 'water', count: 1 }]"
        />
      </div>

      <div class="cards-row enemy-cards">
        <BattleCard
          v-for="(card, index) in enemyCards"
          :key="'enemy-' + index"
          :card-id="card.id"
          :attack="card.attack"
          :health="card.health"
          :card-image="card.image"
          is-enemy
        />
      </div>

      <!-- 我方区域 -->
      <div class="cards-row ally-cards">
        <BattleCard
          v-for="(card, index) in allyCards"
          :key="'ally-' + index"
          :card-id="card.id"
          :attack="card.attack"
          :health="card.health"
          :card-image="card.image"
        />
      </div>

      <div class="avatar_row ally-area">
        <AvatarPlayer
          type="ally"
          avatar-image="/path_to_ally_avatar.png"
          :attack="0"
          :health="20"
          :manas="[{ type: 'fire', count: 1 }, { type: 'fire', count: 1 }]"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BattleLog from './components/BattleLog.vue'
import AvatarPlayer from './components/AvatarPlayer.vue'
import BattleCard from './components/BattleCard.vue'

// 示例数据
const enemyCards = ref([
  { id: 'e1', attack: 1, health: 3, image: '/placeholder_card.png' }
])

const allyCards = ref([
  { id: 'a1', attack: 1, health: 2, image: '/placeholder_card.png' }
])
</script>

<style lang="scss">
@import './src/scss/styles.scss';

.main-layout {
  display: flex;
  height: 100vh;
  width: 100%;
}

/* 调整原SCSS中需要全局生效的样式 */
.battle-container {
  .avatar_row {
    // 保持原有布局样式
  }

  .cards-row {
    // 保持原有布局样式
    gap: 20px; // 增加间距
  }
}
</style>
