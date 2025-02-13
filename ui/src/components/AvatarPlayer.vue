<template>
  <div
      class="avatar-player"
      :data-entity-id="entityId"
      :class="[type, { 'ally': isAlly, 'enemy': !isAlly , 'enter-active': visible }, ]"
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
        {{ mana.type }}：{{ mana.count }}
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed} from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'ally', // 或 enemy
    validator: val => ['ally', 'enemy'].includes(val)
  },
  avatarImage: String,
  attack: Number,
  health: Number,
  mana: { // 修改属性名并调整类型
    type: Object,
    default: () => ({})
  },
  visible: Boolean,
  entityId: {
    type: String,
    required: true
  },
})
// 将对象转换为数组格式
const manas = computed(() => {
  return Object.entries(props.mana || {})
      .filter(([_, count]) => count > 0)
      .map(([type, count]) => ({
        type: type.toUpperCase(),
        count
      }))
})
const isAlly = computed(() => props.type === 'ally')

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

  .avatar-player {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.5s ease-out;
  }

  .avatar-player.enter-active {
    opacity: 1;
    transform: translateY(0);
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

    &.fire {
      color: #ff6666;
    }

    &.water {
      color: #66aaff;
    }

    &.earth {
      color: #66cc66;
    }

    &.air {
      color: #cccccc;
    }
  }
}
</style>
