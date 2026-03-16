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
  description: {
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
  <label class="cursor-pointer group block relative h-full">
    <input 
      type="radio" 
      :name="value" 
      :value="value" 
      :checked="isChecked"
      @change="handleChange"
      class="peer sr-only domain-card-input"
    />
    <div 
      class="domain-card h-full min-h-[220px] bg-surface p-8 border-2 flex flex-col transition-all duration-200 ease-in-out relative z-10"
      :class="{
        'border-primary': isChecked,
        'border-border-color hover:border-primary/50': !isChecked
      }"
    >
      <div class="absolute inset-0 border-4 pointer-events-none transition-colors"
           :class="isChecked ? 'border-primary' : 'border-transparent'"></div>
           
      <div class="flex items-center justify-between mb-6 relative z-10">
        <span class="material-symbols-outlined text-3xl transition-colors"
          :class="isChecked ? 'text-primary' : 'text-text-muted group-hover:text-primary'"
        >{{ icon }}</span>
        <div class="w-8 h-8 flex justify-center items-center transition-colors border-2 rounded-full"
          :class="isChecked ? 'bg-primary border-primary' : 'bg-transparent border-border-color'"
        >
          <div v-if="isChecked" class="w-3 h-3 bg-white rounded-full"></div>
        </div>
      </div>
      <h3 class="font-display text-2xl font-bold text-text-main mb-3 relative z-10"
          :class="isChecked ? 'text-primary' : 'group-hover:text-primary'"
      >{{ title }}</h3>
      <p class="text-sm text-text-muted leading-relaxed flex-1 relative z-10">
        {{ description }}
      </p>
    </div>
  </label>
</template>
