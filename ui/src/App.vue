<!-- src/App.vue -->
<template>
  <div class="main-layout">
    <LogController/>
    <BattleLog/>

    <div class="battle-container">
      <!-- 敌方区域 -->
      <div class="avatar_row enemy-area">
        <AvatarPlayer
            v-for="(player, index) in entityStore.players.enemy"
            :key="`enemy-${index}`"
            :type="player.part"
            :avatar-image="player.avatar || '/default_enemy.png'"
            :attack="player.attack"
            :health="player.health"
            :visible="player.visible"
        />
      </div>
      <div class="cards-row enemy-cards">
        <BattleCard
            v-for="(card, index) in entityStore.cards.enemy"
            :key="`ally-card-${index}`"
            :card-id="card.id"
            :attack="card.attack"
            :health="card.health"
            :card-image="`/public/image/cards/${card.name}.png`  || '/public/image/cards/default_card.png'"
            :visible="card.visible"
        />
      </div>
      <div class="cards-row ally-cards">
        <BattleCard
            v-for="(card, index) in entityStore.cards.ally"
            :key="`ally-card-${index}`"
            :card-id="card.id"
            :attack="card.attack"
            :health="card.health"
            :card-image="`/public/image/cards/${card.name}.png`  || '/public/image/cards/default_card.png'"

            :visible="card.visible"
        />
      </div>

      <div class="avatar_row ally-area">
        <AvatarPlayer
            v-for="(player, index) in entityStore.players.ally"
            :key="`enemy-${index}`"
            :type="player.part"
            :avatar-image="player.avatar || '/default_enemy.png'"
            :attack="player.attack"
            :health="player.health"
            :visible="player.visible"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import BattleLog from './components/BattleLog.vue'
import AvatarPlayer from './components/AvatarPlayer.vue'
import BattleCard from './components/BattleCard.vue'
import LogController from "@/components/LogController.vue";
import {watch} from 'vue'
import {useLogStore} from '@/stores/log'
import {useEntityStore} from '@/stores/entities'

const logStore = useLogStore()
const entityStore = useEntityStore()

// 监听日志变化
watch(() => logStore.currentLog, (newLog) => {
  if (!newLog) return

  switch (newLog.type) {
    case 'add_player':
      entityStore.addPlayer(newLog.player)
      // 触发入场动画
      setTimeout(() => {
        const players = entityStore.players[newLog.player.part]
        players[players.length - 1].visible = true
      }, 50) // 等待DOM更新
      break

    case 'play_card':
      entityStore.addCard(newLog.card, newLog.part)
      setTimeout(() => {
        const cards = entityStore.cards[newLog.part]
        cards[cards.length - 1].visible = true
      }, 50)
      break
  }
})
</script>

<style lang="scss">

.main-layout {
  display: flex;
  height: 100vh;
  width: 100%;
}

</style>
