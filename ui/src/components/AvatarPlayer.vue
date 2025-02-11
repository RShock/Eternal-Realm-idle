<template>
  <div
    class="avatar-player"
    :class="[type, { 'ally': isAlly, 'enemy': !isAlly }]"
  >
    <img :src="avatarImage" class="avatar-image">
    <div class="stats-overlay">
      <span class="attack">{{ attack }}</span>
      <span class="health">{{ health }}</span>
    </div>
    <div class="mana-display">
      <div
        v-for="(mana, index) in manas"
        :key="index"
        class="mana-item"
        :class="mana.type"
      >
        {{ mana.typeLabel }}：{{ mana.count }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'ally', // 或 enemy
    validator: val => ['ally', 'enemy'].includes(val)
  },
  avatarImage: String,
  attack: Number,
  health: Number,
  manas: {
    type: Array,
    default: () => [] // 格式示例：[{ type: 'fire', count: 1 }]
  }
})

const isAlly = computed(() => props.type === 'ally')
const typeLabelMap = {
  fire: '火',
  water: '水',
  earth: '土',
  air: '风'
}

// 添加本地类型标签
const manasWithLabel = computed(() =>
  props.manas.map(mana => ({
    ...mana,
    typeLabel: typeLabelMap[mana.type] || '未知'
  }))
)
</script>

<style scoped>
.avatar-player {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 25px;
  border: 2px solid transparent;
  border-radius: 12px;
  transition: transform 0.2s;

  &.ally:hover {
    border-color: #66aaff;
    transform: scale(1.05);
  }

  &.enemy:hover {
    border-color: #ff6666;
    transform: scale(1.05);
  }
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.stats-overlay {
  /* 共用样式已在父组件定义 */
  font-size: 16px;
  padding: 8px !important;
}

.mana-display {
  position: absolute;
  left: calc(100% + 5px);
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.6);
  padding: 6px 10px;
  border-radius: 4px;
  line-height: 1.3;
  min-width: 60px;

  .mana-item {
    white-space: nowrap;
    font-size: 12px;

    &.fire { color: #ff6666; }
    &.water { color: #66aaff; }
    &.earth { color: #66cc66; }
    &.air { color: #cccccc; }
  }
}
</style>
