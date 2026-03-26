<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWizardStore } from '@/store/wizard'

const route = useRoute()
const router = useRouter()
const store = useWizardStore()

const confirmReset = () => {
  const ok = window.confirm('¿Está seguro de que desea empezar de cero? Todo el progreso actual se perderá.')
  if (ok) {
    store.resetWizard()
    router.push('/paso-1')
  }
}

const currentStepIndex = computed(() => {
  if (route.path === '/paso-1') return 1
  if (route.path === '/paso-2') return 2
  if (route.path === '/paso-3') return 3
  if (route.path === '/paso-4') return 4
  return 0 // 0 = not in wizard (e.g., Herramientas)
})

const isInWizard = computed(() => currentStepIndex.value > 0)

const steps = computed(() => [
  {
    index: 1,
    title: 'Línea de Investigación',
    subtitle: 'Área de estudio',
    completedText: store.step1.subline || 'Completado',
    isCompleted: store.isStep1Complete && (currentStepIndex.value > 1 || currentStepIndex.value === 0)
  },
  {
    index: 2,
    title: 'Nivel de Investigación',
    subtitle: 'Profundidad del estudio',
    completedText: store.step2.level || 'Completado',
    isCompleted: store.isStep2Complete && (currentStepIndex.value > 2 || currentStepIndex.value === 0)
  },
  {
    index: 3,
    title: 'Alcance Empresarial',
    subtitle: 'Sector y delimitación',
    completedText: store.step3.name || 'Completado',
    isCompleted: store.isStep3Complete && (currentStepIndex.value > 3 || currentStepIndex.value === 0)
  },
  {
    index: 4,
    title: 'Propuestas de Títulos',
    subtitle: 'Generación de resultados',
    completedText: store.step4.selectedTitles.length > 0 ? `${store.step4.selectedTitles.length} Seleccionados` : 'Completado',
    isCompleted: store.step4.selectedTitles.length > 0 && (currentStepIndex.value > 4 || currentStepIndex.value === 0)
  }
])

const tools = [
  {
    label: 'Base de Datos de Tesis',
    icon: 'database',
    path: '/herramientas/base-datos'
  }
]

const isToolActive = (path) => route.path === path
</script>

<template>
  <aside class="w-[280px] flex-shrink-0 border-r border-border-color bg-surface flex flex-col h-full z-20 shadow-md" style="background-color: #0056A3;">
    
    <!-- Brand Header -->
    <div class="p-8 border-b border-white/20" style="background-color: #0056A3;">
      <h1 class="font-display font-bold text-xl text-white">Ciencias Economicas</h1>
      <p class="text-[10px] text-white/70 mt-1 uppercase tracking-widest font-bold">Explorador de Tesis</p>
    </div>
    
    <div class="flex flex-col flex-1 overflow-y-auto">

      <!-- ==================== WIZARD STEPS SECTION ==================== -->
      <nav class="flex-shrink-0 p-8">
        <p class="text-[9px] uppercase tracking-[0.15em] font-bold text-white/40 mb-6">Flujo de Trabajo</p>
        <ul class="relative border-l-2 ml-3 space-y-8" style="border-color: rgba(255, 255, 255, 0.2);">
          
          <li v-for="step in steps" :key="step.index" class="relative pl-6">
            
            <!-- STEP COMPLETED -->
            <template v-if="step.isCompleted">
              <span class="absolute -left-[7px] top-1.5 w-[12px] h-[12px] rounded-full bg-secondary"></span>
              <p class="text-[10px] text-secondary font-bold uppercase tracking-widest mb-1">Paso {{ step.index }}</p>
              <p class="text-sm font-semibold text-white">{{ step.title }}</p>
              <div class="flex items-center gap-1 text-[11px] mt-1 text-white/70">
                <span class="material-symbols-outlined text-[14px] text-secondary">check_circle</span>
                <span class="capitalize">{{ step.completedText }}</span>
              </div>
            </template>

            <!-- STEP ACTIVE -->
            <template v-else-if="step.index === currentStepIndex">
              <span class="absolute -left-[7px] top-1.5 w-[12px] h-[12px] rounded-full ring-4 ring-white/10 bg-white"></span>
              <p class="text-[10px] font-bold uppercase tracking-widest mb-1 text-secondary">Paso {{ step.index }}</p>
              <p class="font-display font-bold text-lg leading-tight text-white">{{ step.title }}</p>
            </template>

            <!-- STEP UPCOMING -->
            <template v-else>
              <span class="absolute -left-[7px] top-1.5 w-[12px] h-[12px] rounded-full bg-white/20"></span>
              <p class="text-[10px] font-bold uppercase tracking-widest mb-1 text-white/50">Paso {{ step.index }}</p>
              <p class="text-sm font-medium text-white/70">{{ step.title }}</p>
            </template>

          </li>

        </ul>

        <!-- Smart CTA when browsing Herramientas -->
        <div v-if="!isInWizard" class="mt-6 flex flex-col gap-2">

          <!-- Has existing progress: offer to continue OR reset -->
          <template v-if="store.hasProgress">
            <button 
              @click="$router.push(`/paso-${store.lastCompletedStep}`)"
              class="w-full flex items-center justify-center gap-2 py-3 bg-secondary text-white text-xs font-bold uppercase tracking-widest hover:brightness-110 transition-all shadow-lg shadow-black/20"
            >
              <span class="material-symbols-outlined text-base">play_arrow</span>
              Continuar en Paso {{ store.lastCompletedStep }}
            </button>
            <button
              @click="confirmReset"
              class="w-full text-center text-[10px] text-white/40 hover:text-white/80 transition-colors py-1 uppercase tracking-widest font-bold"
            >
              Empezar de cero
            </button>
          </template>

          <!-- No progress yet -->
          <button 
            v-else
            @click="$router.push('/paso-1')"
            class="w-full flex items-center justify-center gap-2 py-3 bg-secondary text-white text-xs font-bold uppercase tracking-widest hover:brightness-110 transition-all shadow-lg shadow-black/20"
          >
            <span class="material-symbols-outlined text-base">add_circle</span>
            Nueva Consulta
          </button>

        </div>
      </nav>

      <!-- ==================== HERRAMIENTAS SECTION ==================== -->
      <div class="px-8 pb-8 border-t border-white/10 pt-6">
        <p class="text-[9px] uppercase tracking-[0.15em] font-bold text-white/40 mb-4">Herramientas</p>
        <ul class="space-y-1">
          <li v-for="tool in tools" :key="tool.path">
            <button
              @click="$router.push(tool.path)"
              class="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-semibold transition-all"
              :class="isToolActive(tool.path)
                ? 'bg-white/15 text-white border-l-2 border-secondary pl-[10px]'
                : 'text-white/60 hover:text-white hover:bg-white/10'"
            >
              <span class="material-symbols-outlined text-lg" :class="isToolActive(tool.path) ? 'text-secondary' : ''">
                {{ tool.icon }}
              </span>
              {{ tool.label }}
            </button>
          </li>
        </ul>
      </div>

    </div>
  </aside>
</template>
