<script setup>
import reglamentoPdf from '@/assets/reglamento.pdf'
</script>

<template>
  <div class="bg-white border-b border-border-color px-12 py-4 flex items-center justify-between sticky top-0 z-50 w-full">
    <div class="flex items-center gap-3">
      <span class="material-symbols-outlined text-primary text-xl">verified_user</span>
      <p class="text-[13px] text-muted font-body">
          Usted está utilizando el asistente de generación de tesis v2.3
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
        Guía Metodológica
      </a>
      
    </div>
  </div>
</template>
