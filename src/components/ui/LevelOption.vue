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
  subtitle: {
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
  <label class="group relative flex items-start p-8 cursor-pointer border-2 bg-surface transition-all"
         :class="isChecked ? 'border-primary' : 'border-border-color hover:border-primary/50'">
    <input 
      type="radio" 
      :name="value" 
      :value="value"
      :checked="isChecked"
      @change="handleChange"
      class="sr-only peer" 
    />
    
    <!-- Custom Active Border Overlay (matches paso 2.html) -->
    <div class="absolute inset-0 border-4 pointer-events-none transition-colors"
         :class="isChecked ? 'border-primary' : 'border-transparent'"></div>
         
    <div class="flex-1 flex items-center justify-between relative z-10">
      <div>
        <span class="font-display font-bold text-xl transition-colors"
              :class="isChecked ? 'text-primary' : 'text-text-main group-hover:text-primary'">
          {{ title }}
        </span>
        <p class="text-[11px] text-text-muted mt-2 font-medium tracking-wide uppercase">
          {{ subtitle }}
        </p>
      </div>
      
      <!-- Radio Circle Indicator -->
       <div class="w-8 h-8 rounded-full border-2 transition-all flex items-center justify-center"
            :class="isChecked ? 'border-primary bg-primary' : 'border-border-color'">
         <div v-if="isChecked" class="w-3 h-3 bg-white rounded-full"></div>
       </div>
    </div>
  </label>
</template>
