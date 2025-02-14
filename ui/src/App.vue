<!-- src/App.vue -->
<template>
  <div class="main-layout">
    <LogController/>
    <BattleLog/>
    <AttackArrow
        v-if="currentAttack"
        :attacker-id="currentAttack.attackerId"
        :defender-id="currentAttack.defenderId"
    />
    <div class="battle-container">
      <!-- 敌方区域 -->
      <div class="avatar_row enemy-area">
        <AvatarPlayer
            v-for="(player, index) in entityStore.players.enemy"
            :key="`enemy-${index}`"
            :entity-id="player.id"
            :type="player.part"
            :avatar-image="`/image/avatars/female.png` || '/default_enemy.png'"
            :attack="player.attack"
            :health="player.health"
            :visible="player.visible"
            :mana="player.mana"
        />
      </div>
      <div class="cards-row enemy-cards">
        <BattleCard
            v-for="(card, index) in entityStore.cards.enemy"
            :key="`ally-card-${index}`"
            :card-id="card.id"
            :attack="card.attack"
            :health="card.health"
            :card-image="`/image/cards/${card.name}.png`  || '/public/image/cards/default_card.png'"
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
            :card-image="`/image/cards/${card.name}.png`  || '/public/image/cards/default_card.png'"

            :visible="card.visible"
        />
      </div>
      <div class="avatar_row ally-area">
        <AvatarPlayer
            v-for="(player, index) in entityStore.players.ally"
            :key="`enemy-${index}`"
            :type="player.part"
            :entity-id="player.id"
            :avatar-image="`/image/avatars/male.png` || '/default_enemy.png'"
            :attack="player.attack"
            :health="player.health"
            :visible="player.visible"
            :mana="player.mana"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import {createApp, ref} from 'vue'
import BattleLog from './components/BattleLog.vue'
import AvatarPlayer from './components/AvatarPlayer.vue'
import BattleCard from './components/BattleCard.vue'
import LogController from "@/components/LogController.vue";
import {watch} from 'vue'
import {useLogStore} from '@/stores/log'
import {useEntityStore} from '@/stores/entities'
import AttackArrow from "@/components/AttackArrow.vue";
import DamageNumber from "@/components/DamageNumber.vue";
import {gsap} from "gsap";
const logStore = useLogStore()
const entityStore = useEntityStore()
const currentAttack = ref(null)

// 监听日志变化
watch(() => logStore.currentLog, (newLog) => {
  if (!newLog) return

  const createDamageNumber = (log) => {
    // 创建容器元素
    const container = document.createElement('div')
    document.body.appendChild(container)

    // 创建应用实例
    const damageApp = createApp(DamageNumber, {
      damage: log.damage,
      defenderId: log.defender_id
    })

    // 挂载并保存实例
    const instance = damageApp.mount(container)

    // 自动卸载（1.5秒后）
    setTimeout(() => {
      damageApp.unmount()
      document.body.removeChild(container)
    }, 1500)
  }

  switch (newLog.type) {
    case 'add_player':
      entityStore.addPlayer(newLog.player)
      // 触发入场动画
      setTimeout(() => {
        const players = entityStore.players[newLog.player.part]
        players[players.length - 1].visible = true
      }, 50) // 等待DOM更新
      break
    case 'attack':
      currentAttack.value = {
        attackerId: newLog.attacker_id,
        defenderId: newLog.defender_id
      }
      setTimeout(() => {
        currentAttack.value = null
      }, 1000)
      break
    case 'play_card':
      entityStore.addCard(newLog.card, newLog.part)
      setTimeout(() => {
        const cards = entityStore.cards[newLog.part]
        cards[cards.length - 1].visible = true
      }, 50)
      break
    case 'deal_damage':
      // 创建伤害数字组件
      createDamageNumber(newLog)
      entityStore.updateHealth(newLog.defender_id, newLog.defender_hp)
      break
    case 'destroy':
      const targetId = newLog.id
      const targetElem = document.querySelector(`[data-entity-id="${targetId}"]`)
      if (targetElem) {
        // 创建动画时间线
        const tl = gsap.timeline()

        // 第一阶段：变灰效果
        tl.to(targetElem, {
          duration: 0.2,
          filter: 'grayscale(1) brightness(0.7)',
          ease: 'power2.inOut'
        })
            // 第二阶段：抖动+缩小消失
            .to(targetElem, {
              duration: 0.3,
              opacity: 0,
              scale: 0,
              x: '+=20', // 添加抖动效果
              ease: 'back.in',
              onComplete: () => {
                entityStore.removeEntity(targetId)
              }
            })
      } else {
        // 如果找不到元素直接移除
        entityStore.removeEntity(targetId)
      }
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
