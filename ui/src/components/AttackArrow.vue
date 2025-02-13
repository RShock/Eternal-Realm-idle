<template>
  <svg class="attack-arrow">
    <path
      class="arrow-line"
      :d="pathData"
      :style="lineStyle"
    />
  </svg>
</template>
<script setup>
import {ref, onMounted, watch, computed, onUnmounted} from 'vue'

const props = defineProps({
  attackerId: String,
  defenderId: String
})
const startPos = ref({x: 0, y: 0})
const endPos = ref({x: 0, y: 0})

const getElementCenter = (element) => {
  const rect = element.getBoundingClientRect()
  return {
    x: rect.left + rect.width / 2 + window.scrollX,
    y: rect.top + rect.height / 2 + window.scrollY
  }
}
const pathData = computed(() => {
  return `M ${startPos.value.x} ${startPos.value.y} L ${endPos.value.x} ${endPos.value.y}`
})

const lineStyle = computed(() => ({
  '--length': Math.hypot(endPos.value.x - startPos.value.x, endPos.value.y - startPos.value.y)
}))

const headStyle = computed(() => {
  return {
    transform: `translate(${endPos.value.x}px, ${endPos.value.y}px)`
  }
})
const updatePositions = () => {
  const attackerElem = document.querySelector(`[data-entity-id="${props.attackerId}"]`)
  const defenderElem = document.querySelector(`[data-entity-id="${props.defenderId}"]`)
  if (!attackerElem) {
    console.error(`未找到攻击者元素，ID: ${props.attackerId}`)
  }
  if (!defenderElem) {
    console.error(`未找到防御者元素，ID: ${props.defenderId}`)
  }
  if (attackerElem && defenderElem) {
    startPos.value = getElementCenter(attackerElem)
    endPos.value = getElementCenter(defenderElem)
  }
}

// 初始化时和窗口变化时更新位置
onMounted(() => {
  updatePositions()
  window.addEventListener('resize', updatePositions)
})

// 组件销毁时移除监听
onUnmounted(() => {
  window.removeEventListener('resize', updatePositions)
})

watch(() => [props.attackerId, props.defenderId], updatePositions)
</script>

<style scoped>
.attack-arrow {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 1000;
}

.arrow-line {
  stroke: #ff4444;
  stroke-width: 12px;
  fill: none;
  stroke-dasharray: var(--length);
  stroke-dashoffset: var(--length);
  filter: drop-shadow(0 0 8px rgba(255, 80, 80, 0.8));
  animation: draw 0.5s ease-out forwards;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes appear {
  to {
    opacity: 1;
  }
}
</style>
