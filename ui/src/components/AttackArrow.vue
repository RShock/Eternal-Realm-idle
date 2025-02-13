<template>
  <div
      class="attack-arrow"
      :style="arrowStyle"
  >
    <!-- 箭头图形使用CSS绘制 -->
    <div class="arrow-line"></div>
    <div class="arrow-head"></div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch, computed, onUnmounted} from 'vue'
import {useEntityStore} from '@/stores/entities'

const props = defineProps({
  attackerId: String,
  defenderId: String
})

const entityStore = useEntityStore()
const startPos = ref({x: 0, y: 0})
const endPos = ref({x: 0, y: 0})

const getElementCenter = (element) => {
  const rect = element.getBoundingClientRect()
  return {
    x: rect.left + rect.width / 2 + window.scrollX,
    y: rect.top + rect.height / 2 + window.scrollY
  }
}

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
  // 调试日志
  console.log('Attacker Element:', attackerElem)
  console.log('Defender Element:', defenderElem)
  console.log('Start Position:', startPos.value)
  console.log('End Position:', endPos.value)
}

// 计算箭头样式
const arrowStyle = computed(() => {
  const dx = endPos.value.x - startPos.value.x
  const dy = endPos.value.y - startPos.value.y
  const length = Math.sqrt(dx * dx + dy * dy)
  const angle = Math.atan2(dy, dx) * 180 / Math.PI + 90

  return {
    '--length': `${length}px`,
    '--angle': `${angle}deg`,
    '--start-x': `${startPos.value.x}px`,
    '--start-y': `${startPos.value.y}px`,
    '--end-x': `${endPos.value.x}px`,
    '--end-y': `${endPos.value.y}px`
  }
})

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
  top: 0;
  left: 0;
  position: fixed;
  transform: translate(var(--end-x), var(--end-y)) rotate(var(--angle));
  transform-origin: 0 0;
  pointer-events: none;
  z-index: 1000;
  animation: arrowAppear 0.3s ease-out;
}

.arrow-line {
  width: 12px;
  height: var(--length);
  background: linear-gradient(to bottom,
  rgba(255, 200, 0, 0) 0%,
  rgba(255, 230, 0, 1) 30%,
  rgba(255, 100, 0, 1) 70%,
  rgba(255, 50, 0, 0) 100%);
  box-shadow: 0 0 8px rgba(255, 100, 0, 0.6), /* 添加发光效果 */ 0 0 4px rgba(255, 200, 0, 0.4);
}

.arrow-head {
  top: 0;
  position: absolute;
  bottom: -3px;
  left: -12px;
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-bottom: 12px solid #ff4444; /* 修改为 border-bottom */
  filter: drop-shadow(0 0 4px rgba(255, 80, 80, 0.8)) /* 增强阴影 */ brightness(1.2); /* 提高亮度 */
}

@keyframes arrowAppear {
  from {
    opacity: 0;
    transform: translate(-50%, -50%) rotate(var(--angle)) scaleY(0);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) rotate(var(--angle)) scaleY(1);
  }
}
</style>
