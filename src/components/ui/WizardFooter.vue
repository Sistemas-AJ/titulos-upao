<script setup>
defineProps({
  canContinue: {
    type: Boolean,
    default: true
  },
  continueText: {
    type: String,
    default: 'Continuar Proceso'
  },
  showBack: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: 'primary' // 'primary' or 'secondary'
  },
  icon: {
    type: String,
    default: 'chevron_right'
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['next', 'back'])
</script>

<template>
  <div class="mt-auto py-8 border-t border-border-color flex items-center justify-between bg-surface relative z-20">
    
    <!-- Left Area: Can be Back button OR Custom Info Slot -->
    <div>
      <button 
        v-if="showBack"
        @click="$emit('back')" 
        type="button" 
        class="text-text-muted font-bold uppercase tracking-widest text-xs hover:text-primary transition-colors flex items-center gap-3 group px-4 py-2"
      >
        <span class="material-symbols-outlined text-lg group-hover:-translate-x-1 transition-transform">arrow_back</span>
        Regresar
      </button>
      
      <slot name="info" v-else></slot>
    </div>
    
    <!-- Right Area: Main Action -->
    <button 
      @click="$emit('next')"
      type="button"
      class="font-bold uppercase tracking-widest text-xs px-12 py-5 transition-all flex items-center gap-4 group"
      :class="{
        'bg-primary text-white shadow-lg hover:shadow-[0_10px_30px_rgba(0,86,163,0.3)] hover:bg-primary/95 cursor-pointer': canContinue && color === 'primary' && !isLoading,
        'bg-secondary text-white shadow-xl shadow-secondary/30 hover:brightness-110 tracking-[0.05em] text-sm rounded-md cursor-pointer': canContinue && color === 'secondary' && !isLoading,
        'bg-gray-200 text-text-muted opacity-60 cursor-not-allowed pointer-events-none shadow-none': !canContinue || isLoading,
        'bg-secondary text-white opacity-90 cursor-wait shadow-none': isLoading && color === 'secondary',
        'bg-primary text-white opacity-90 cursor-wait shadow-none': isLoading && color === 'primary'
      }"
      :disabled="!canContinue || isLoading"
    >
      {{ isLoading ? 'Procesando...' : continueText }}
      <span class="material-symbols-outlined transition-transform"
            :class="[
              color === 'secondary' ? 'text-sm' : 'text-[18px] group-hover:translate-x-1',
              isLoading ? 'animate-spin' : ''
            ]">{{ isLoading ? 'progress_activity' : icon }}</span>
    </button>
    
  </div>
</template>
