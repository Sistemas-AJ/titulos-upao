<script setup>
import reglamentoPdf from '@/assets/reglamento.pdf'

defineProps({
  isSidebarOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-sidebar'])
</script>

<template>
  <div class="bg-white border-b border-border-color px-4 md:px-12 py-4 flex items-center justify-between sticky top-0 z-40 w-full">
    <div class="flex items-center gap-3">
      <button
        type="button"
        class="lg:hidden inline-flex items-center justify-center w-10 h-10 rounded-full border border-border-color text-primary hover:bg-slate-50 transition-colors"
        :aria-label="isSidebarOpen ? 'Cerrar menú lateral' : 'Abrir menú lateral'"
        @click="$emit('toggle-sidebar')"
      >
        <span class="material-symbols-outlined text-[22px]">
          {{ isSidebarOpen ? 'close' : 'menu' }}
        </span>
      </button>
      <span class="material-symbols-outlined text-primary text-xl">verified_user</span>
      <p class="hidden sm:block text-[13px] text-muted font-body">
          Usted está utilizando el asistente de generación de tesis v2.4
      </p>
    </div>
    <div class="flex items-center gap-4">
      <a 
        :href="reglamentoPdf" 
        target="_blank"
        rel="noopener noreferrer"
        class="text-xs font-bold text-primary hover:underline hover:text-secondary transition-colors flex items-center gap-1.5"
      >
        <span class="material-symbols-outlined text-sm">picture_as_pdf</span>
        <span class="hidden sm:inline">Guía Metodológica</span>
      </a>
      
    </div>
  </div>
</template>
