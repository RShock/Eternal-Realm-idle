<template>
  <div
    ref="damageEl"
    class="damage-number"
    :data-defender-id="defenderId"
    :style="positionStyle"
  >
    -{{ damage }}
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { gsap } from 'gsap'

const props = defineProps({
  damage: {
    type: Number,
    required: true
  },
  defenderId: {
    type: String,
    required: true
  }
})

const damageEl = ref(null)
const position = ref({ x: 0, y: 0 })

// 计算初始位置
const positionStyle = computed(() => ({
  left: `${position.value.x}px`,
  top: `${position.value.y}px`
}))

// onMounted(() => {
//   // 定位到受伤者中心
//   const targetElem = document.querySelector(`[data-entity-id="${props.defenderId}"]`)
//   if (targetElem) {
//     const rect = targetElem.getBoundingClientRect()
//     position.value = {
//       x: rect.left + rect.width/2 - 20,
//       y: rect.top + rect.height/2 - 20
//     }
//   }
//

// })

onMounted(() => {
  const targetElem = document.querySelector(`[data-entity-id="${props.defenderId}"]`)
  if (targetElem) {
    const rect = targetElem.getBoundingClientRect()
    position.value = {
      x: rect.left + rect.width/2,
      y: rect.top + rect.height/2
    }
    console.log(targetElem, rect)
  } else {
    console.warn(`未找到目标实体：${props.defenderId}`)
    // 默认显示在屏幕中间
    position.value = {
      x: window.innerWidth/2,
      y: window.innerHeight/2
    }
  }

    // 执行动画
  gsap.fromTo(damageEl.value,
    { opacity: 1, scale: 0.5, y: 0 },
    {
      opacity: 0,
      scale: 2,
      y: -100,
      duration: 1,
      ease: "power2.out",
      onComplete: () => {
        if (damageEl.value) {
          damageEl.value.remove()
        }
      }
    }
  )
})
</script>

<style scoped>
.damage-number {
  position: fixed;
  font-size: 48px;
  font-weight: 900;
  color: #ff4444;
  text-shadow:
    0 0 10px rgba(255, 50, 50, 0.8),
    2px 2px 4px rgba(0, 0, 0, 0.5);
  pointer-events: none;
  z-index: 2000;
  transform: translate(-50%, -50%);
}
</style>
