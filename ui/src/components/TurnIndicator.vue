<!-- src/components/TurnIndicator.vue -->
<template>
  <transition @enter="enterAnim">
    <div
      v-if="visible"
      class="turn-indicator"
      :class="[currentTurnInfo.current_player_id === '1' ? 'ally' : 'enemy']"
    >
      <div class="main-text">{{ playerName }}的回合</div>
      <div class="sub-text">回合数：{{ currentTurnInfo.turn }}</div>
    </div>
  </transition>
</template>

<script setup>
import {computed, watch} from 'vue'
import { useEntityStore } from '@/stores/entities'
import { gsap } from 'gsap'

const entityStore = useEntityStore()

const visible = computed(() => entityStore.currentTurnInfo?.visible)
const currentTurnInfo = computed(() => entityStore.currentTurnInfo || {})
const playerName = computed(() => {
  const player = entityStore.findEntity(currentTurnInfo.value.current_player_id)
  return player?.name || '未知玩家'
})
watch(currentTurnInfo, (newVal) => {
  console.log('回合信息变化:', newVal)
}, { deep: true })

watch(visible, (newVal) => {
  console.log('可见性变化:', newVal) // 调试点3
})
const enterAnim = (el, done) => {
  gsap.fromTo(el,
    { scale: 0.5, opacity: 0 },
    {
      scale: 1,
      opacity: 1,
      duration: 0.5,
      ease: 'back.out(1.7)',
      onComplete: done
    }
  )
  // 自动隐藏
  setTimeout(() => {
    entityStore.setTurnInfo({ ...currentTurnInfo.value, visible: false })
  }, 1500)
}
</script>

<style scoped>
.turn-indicator {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 9999;
  pointer-events: none;

  .main-text {
    font-size: 72px;
    font-weight: 900;
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    line-height: 1.2;
  }

  .sub-text {
    font-size: 24px;
    opacity: 0.8;
    margin-top: 12px;
  }

  &.ally .main-text {
    color: #66aaff;
    text-shadow: 0 0 20px rgba(102,170,255,0.5);
  }

  &.enemy .main-text {
    color: #ff6666;
    text-shadow: 0 0 20px rgba(255,102,102,0.5);
  }
}
</style>
