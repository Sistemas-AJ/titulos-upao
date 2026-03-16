<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useWizardStore } from '@/store/wizard'

const router = useRouter()
const store = useWizardStore()

const selectedIndices = ref([])
const isLoading = computed(() => store.step4.status === 'loading')
const proposals = computed(() => store.step4.proposals)
const hasError = computed(() => store.step4.status === 'error')
const errorMessage = computed(() => store.step4.error)

onMounted(() => {
  if (!store.isStep3Complete) {
    router.push('/paso-3')
  }
})

const toggleSelection = (index) => {
  const pos = selectedIndices.value.indexOf(index)
  if (pos === -1) {
    selectedIndices.value.push(index)
  } else {
    selectedIndices.value.splice(pos, 1)
  }
}

const hasSelection = computed(() => selectedIndices.value.length > 0)

const downloadSelection = () => {
  if (!hasSelection.value) return
  alert(`Descargando ${selectedIndices.value.length} propuestas seleccionadas...`)
}

const exportFormat = () => {
  if (!hasSelection.value) return
  alert(`Exportando ${selectedIndices.value.length} propuestas al Formato Excel Oficial UPAO...`)
}

const goBack = () => {
  router.push('/paso-3')
}
</script>

<template>
  <div class="max-w-[1100px] w-full mx-auto py-16 px-12 flex-1 flex flex-col relative">
    
    <!-- AI Loading Screen -->
    <div v-if="isLoading" class="absolute inset-0 flex flex-col items-center justify-center bg-white z-50">
      <div class="relative w-24 h-24 mb-8">
        <!-- Pulse effect -->
        <div class="absolute inset-0 bg-primary/20 rounded-full animate-ping"></div>
        <div class="absolute inset-2 bg-primary/30 rounded-full animate-pulse"></div>
        <!-- Center core -->
        <div class="absolute inset-0 flex items-center justify-center">
            <span class="material-symbols-outlined text-primary text-5xl animate-bounce">auto_awesome</span>
        </div>
      </div>
      <h3 class="font-display text-2xl font-bold text-primary mb-2">Generando propuestas con IA...</h3>
      <p class="text-text-muted text-sm max-w-sm text-center">
        Analizando sus variables metodológicas ({{ store.step1.subline || 'Auditoría' }} / {{ store.step2.level || 'Correlacional' }}) y cruzando datos con el repositorio institucional.
      </p>
    </div>

    <!-- Main Content -->
    <div v-else class="flex flex-col flex-1 animate-fadeIn">
      <!-- Header -->
      <header class="mb-10 flex justify-between items-end">
        <div>
          <h2 class="font-display text-4xl font-bold text-primary leading-tight mb-3">Propuestas de Títulos</h2>
          <p class="text-lg text-text-muted">Seleccione las opciones que mejor se adapten a su objetivo de estudio.</p>
          <div class="h-1 w-20 bg-secondary mt-6 rounded-full"></div>
        </div>
        <div class="flex gap-3">
          <button 
            @click="downloadSelection"
            class="bg-surface border-2 border-primary text-primary px-6 py-3 font-bold uppercase tracking-wider text-xs transition-all flex items-center gap-2"
            :class="hasSelection ? 'hover:bg-primary hover:text-white cursor-pointer' : 'opacity-50 cursor-not-allowed grayscale'"
          >
            <span class="material-symbols-outlined text-lg">download</span>
            Descargar Selección
          </button>
          
          <button 
            @click="exportFormat"
            class="bg-secondary text-white px-6 py-3 font-bold uppercase tracking-wider text-xs transition-all flex items-center gap-2"
             :class="hasSelection ? 'hover:brightness-110 shadow-lg shadow-secondary/20 cursor-pointer' : 'opacity-50 cursor-not-allowed grayscale'"
          >
            <span class="material-symbols-outlined text-lg">description</span>
            Exportar Formato Oficial
          </button>
        </div>
      </header>

      <!-- AI Limitation Warning -->
      <div class="mb-10 p-4 bg-amber-50 border-l-4 border-amber-400 flex items-center gap-3">
        <span class="material-symbols-outlined text-amber-600">info</span>
        <p class="text-sm text-amber-800 font-medium">
          <strong class="font-bold">Nota:</strong> Los resultados de la IA son sugerencias y deben ser revisados académicamente por su asesor.
        </p>
      </div>

      <div v-if="hasError" class="mb-10 p-5 bg-red-50 border-l-4 border-red-400 flex items-start gap-3">
        <span class="material-symbols-outlined text-red-600">error</span>
        <div>
          <p class="text-sm text-red-800 font-bold">No se pudieron generar las propuestas.</p>
          <p class="text-sm text-red-700 mt-1">{{ errorMessage }}</p>
        </div>
      </div>

      <!-- Proposals List -->
      <div v-if="proposals.length" class="space-y-4 flex-1">
        <label 
          v-for="(item, index) in proposals" 
          :key="index"
          class="block bg-surface border rounded-none cursor-pointer overflow-hidden group transition-all duration-200"
          :class="selectedIndices.includes(index) ? 'border-primary shadow-[0_10px_15px_-3px_rgba(0,86,163,0.1)]' : 'border-border-color hover:border-primary/50'"
        >
          <input 
            type="checkbox" 
            class="hidden" 
            :value="index" 
            @change="toggleSelection(index)"
            :checked="selectedIndices.includes(index)"
          >
          <div class="flex items-stretch transition-colors" :class="selectedIndices.includes(index) ? 'bg-primary/5' : ''">
            
            <div class="w-16 flex items-center justify-center border-r transition-colors"
                 :class="selectedIndices.includes(index) ? 'border-primary bg-primary text-white' : 'border-border-color text-text-muted group-hover:bg-primary/5 group-hover:text-primary'">
              <span class="material-symbols-outlined transition-transform"
                    :class="selectedIndices.includes(index) ? 'scale-110' : ''">
                {{ selectedIndices.includes(index) ? 'check_circle' : 'add_circle' }}
              </span>
            </div>
            
            <div class="flex-1 p-6">
              <h3 class="font-display font-bold text-lg text-primary mb-4 leading-snug">{{ item.t }}</h3>
              
              <div class="grid grid-cols-2 lg:grid-cols-5 gap-3">
                <div>
                  <span class="text-[10px] font-bold uppercase tracking-[0.05em] px-2 py-0.5 rounded-sm inline-block mb-1 bg-blue-100 text-blue-700">Variable 1</span>
                  <p class="text-[13px] text-text-muted font-medium">{{ item.v1 }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold uppercase tracking-[0.05em] px-2 py-0.5 rounded-sm inline-block mb-1 bg-slate-100 text-slate-700">Conector</span>
                  <p class="text-[13px] text-text-muted font-medium">{{ item.c }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold uppercase tracking-[0.05em] px-2 py-0.5 rounded-sm inline-block mb-1 bg-blue-100 text-blue-700">Variable 2</span>
                  <p class="text-[13px] text-text-muted font-medium">{{ item.v2 }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold uppercase tracking-[0.05em] px-2 py-0.5 rounded-sm inline-block mb-1 bg-purple-100 text-purple-700">U. de Invest.</span>
                  <p class="text-[13px] text-text-muted font-medium">{{ item.u }}</p>
                </div>
                <div>
                  <span class="text-[10px] font-bold uppercase tracking-[0.05em] px-2 py-0.5 rounded-sm inline-block mb-1 bg-emerald-100 text-emerald-700">Espacial/Temp.</span>
                  <p class="text-[13px] text-text-muted font-medium">{{ item.s }}</p>
                </div>
              </div>

            </div>
          </div>
        </label>
      </div>

      <div v-else-if="!hasError" class="flex-1 flex items-center justify-center border border-dashed border-border-color bg-background-light">
        <div class="text-center px-8 py-16">
          <span class="material-symbols-outlined text-5xl text-text-muted mb-4 block">hourglass_empty</span>
          <p class="font-display font-bold text-xl text-text-main mb-2">Esperando resultados</p>
          <p class="text-sm text-text-muted">La solicitud fue enviada y esta vista se actualizará cuando el backend responda.</p>
        </div>
      </div>

      <!-- Action Area -->
      <div class="flex justify-between items-center pt-8 border-t border-border-color mt-12 pb-8">
        <button 
          @click="goBack"
          class="group flex items-center gap-3 font-bold uppercase tracking-widest text-xs text-text-muted hover:text-primary transition-colors px-4 py-2" 
          type="button"
        >
          <span class="material-symbols-outlined text-lg group-hover:-translate-x-1 transition-transform">arrow_back</span>
          Regresar a Unidad
        </button>
        
        <div class="flex items-center gap-4">
          <span class="text-xs font-bold text-primary uppercase tracking-widest">Paso final completado</span>
          <div class="flex gap-1">
            <div class="w-2 h-2 rounded-full bg-primary animate-pulse" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 rounded-full bg-primary animate-pulse" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 rounded-full bg-primary animate-pulse" style="animation-delay: 0.4s"></div>
            <div class="w-2 h-2 rounded-full bg-primary animate-pulse" style="animation-delay: 0.6s"></div>
          </div>
        </div>
      </div>
    
    </div>
  </div>
</template>
