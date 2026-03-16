<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
  value: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const isChecked = computed(() => props.modelValue === props.value)

const handleChange = () => {
  emit('update:modelValue', props.value)
}
</script>

<template>
  <label class="cursor-pointer block relative h-full">
    <input 
      type="radio" 
      :name="value" 
      :value="value"
      :checked="isChecked"
      @change="handleChange"
      class="sr-only subline-input" 
    />
    <div 
      class="subline-card border-2 px-4 py-6 text-center text-xs font-bold uppercase tracking-tight transition-all flex flex-col items-center justify-center gap-2 h-full relative"
      :class="{
        'bg-primary text-white border-primary': isChecked,
        'border-border-color bg-surface hover:border-primary/50 text-text-main': !isChecked
      }"
    >
      <div class="absolute inset-0 border-4 pointer-events-none transition-colors"
           :class="isChecked ? 'border-primary' : 'border-transparent'"></div>
           
      <span class="material-symbols-outlined text-[18px] relative z-10">{{ icon }}</span>
      <span class="relative z-10">{{ title }}</span>
    </div>
  </label>
</template>
