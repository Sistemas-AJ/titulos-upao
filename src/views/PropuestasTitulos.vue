<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useWizardStore } from '@/store/wizard'
import { generateProposals } from '@/services/api'

const router = useRouter()
const store = useWizardStore()
const SAVED_SELECTIONS_KEY = 'upao_saved_title_selection'
const FIVE_DAYS_IN_MS = 5 * 24 * 60 * 60 * 1000

const selectedIndices = ref([])
const isLoading = computed(() => store.step4.status === 'loading')
const proposals = computed(() => store.step4.proposals)
const hasError = computed(() => store.step4.status === 'error')
const errorMessage = computed(() => store.step4.error)
const canRetry = computed(() => store.step4.retryable)
const savedTitles = computed(() => store.step4.selectedTitles)
const savedTitleSet = computed(() => new Set(savedTitles.value.map((item) => item.t)))
const hasSavedSelection = computed(() => savedTitles.value.length > 0)
const saveSelectionLabel = computed(() => 'Guardar Selección')

onMounted(() => {
  purgeExpiredSavedSelection()
  if (!store.isStep3Complete) {
    router.push('/paso-3')
  }
  restoreSavedSelection()
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
const selectedProposals = computed(() => selectedIndices.value.map((index) => proposals.value[index]).filter(Boolean))

watch(proposals, () => {
  restoreSavedSelection()
})

const purgeExpiredSavedSelection = () => {
  try {
    const saved = localStorage.getItem(SAVED_SELECTIONS_KEY)
    if (!saved) return

    const parsed = JSON.parse(saved)
    if (!parsed.expiresAt || Date.now() > parsed.expiresAt) {
      localStorage.removeItem(SAVED_SELECTIONS_KEY)
    }
  } catch {
    localStorage.removeItem(SAVED_SELECTIONS_KEY)
  }
}

const restoreSavedSelection = () => {
  if (!proposals.value.length) return

  try {
    const saved = localStorage.getItem(SAVED_SELECTIONS_KEY)
    if (!saved) return

    const parsed = JSON.parse(saved)
    if (!parsed.expiresAt || Date.now() > parsed.expiresAt) {
      localStorage.removeItem(SAVED_SELECTIONS_KEY)
      return
    }

    const savedTitles = new Set((parsed.items || []).map((item) => item.t))
    selectedIndices.value = proposals.value
      .map((item, index) => savedTitles.has(item.t) ? index : -1)
      .filter((index) => index !== -1)
    store.setSavedSelection({
      titles: (parsed.items || []),
      expiresAt: parsed.expiresAt
    })
  } catch {
    localStorage.removeItem(SAVED_SELECTIONS_KEY)
  }
}

const saveSelection = () => {
  if (!hasSelection.value) return

  const expiresAt = Date.now() + FIVE_DAYS_IN_MS
  const payload = {
    savedAt: Date.now(),
    expiresAt,
    items: selectedProposals.value,
    sessionId: store.step4.sessionId,
    linea: store.step1.domain,
    sublinea: store.step1.subline
  }

  localStorage.setItem(SAVED_SELECTIONS_KEY, JSON.stringify(payload))

  const expirationText = new Date(expiresAt).toLocaleDateString('es-PE')
  alert(`La selección se guardó temporalmente en este dispositivo hasta el ${expirationText}.`)
  store.setSavedSelection({
    titles: selectedProposals.value,
    expiresAt
  })
}

const escapeHtml = (value) => String(value ?? '')
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')

const splitSpatialTemporal = (value) => {
  const raw = String(value || '')
  const lastCommaIndex = raw.lastIndexOf(',')
  if (lastCommaIndex === -1) {
    return {
      espacio: raw,
      tiempo: ''
    }
  }

  return {
    espacio: raw.slice(0, lastCommaIndex).trim(),
    tiempo: raw.slice(lastCommaIndex + 1).trim()
  }
}

const exportFormat = () => {
  if (!hasSelection.value) return

  const rows = selectedProposals.value.map((item, index) => {
    const { espacio, tiempo } = splitSpatialTemporal(item.s)
    return `
      <tr>
        <td>${index + 1}</td>
        <td>${escapeHtml(item.t)}</td>
        <td>${escapeHtml(item.v1)}</td>
        <td>${escapeHtml(item.c)}</td>
        <td>${escapeHtml(item.v2)}</td>
        <td>${escapeHtml(item.u)}</td>
        <td>${escapeHtml(espacio)}</td>
        <td>${escapeHtml(tiempo)}</td>
      </tr>
    `
  }).join('')

  const html = `
    <html>
      <head>
        <meta charset="UTF-8" />
      </head>
      <body>
        <table border="1">
          <tr>
            <th>N</th>
            <th>Titulo</th>
            <th>Variable 1</th>
            <th>Conector</th>
            <th>Variable 2</th>
            <th>Unidad de Investigacion</th>
            <th>Espacio</th>
            <th>Tiempo</th>
          </tr>
          ${rows}
        </table>
      </body>
    </html>
  `

  const blob = new Blob([html], {
    type: 'application/vnd.ms-excel;charset=utf-8;'
  })

  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'formato_oficial_titulos_upao.xls'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

const goBack = () => {
  router.push('/paso-3')
}

const startNewTitleFlow = () => {
  localStorage.removeItem(SAVED_SELECTIONS_KEY)
  store.resetWizard()
  router.push('/paso-1')
}

const retryGeneration = async () => {
  store.startProposalGeneration()

  try {
    const response = await generateProposals(store.$state)
    store.setGeneratedProposals({
      proposals: response.proposals,
      sessionId: response.session_id
    })
  } catch (error) {
    console.error('Retry failed:', error)
    store.setProposalError({
      message: error.message,
      retryable: Boolean(error.retryable)
    })
  }
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
            @click="saveSelection"
            class="bg-surface border-2 border-primary text-primary px-6 py-3 font-bold uppercase tracking-wider text-xs transition-all flex items-center gap-2"
            :class="hasSelection ? 'hover:bg-primary hover:text-white cursor-pointer' : 'opacity-50 cursor-not-allowed grayscale'"
          >
            <span class="material-symbols-outlined text-lg">save</span>
            {{ saveSelectionLabel }}
          </button>
          
          <button 
            @click="exportFormat"
            class="bg-secondary text-white px-6 py-3 font-bold uppercase tracking-wider text-xs transition-all flex items-center gap-2"
             :class="hasSelection ? 'hover:brightness-110 shadow-lg shadow-secondary/20 cursor-pointer' : 'opacity-50 cursor-not-allowed grayscale'"
          >
            <span class="material-symbols-outlined text-lg">description</span>
            Exportar Titulos a Excel
          </button>
        </div>
      </header>

      <!-- AI Limitation Warning -->
      <div class="mb-10 p-4 bg-amber-50 border-l-4 border-amber-400 flex items-center gap-3">
        <span class="material-symbols-outlined text-amber-600">info</span>
        <p class="text-sm text-amber-800 font-medium">
          <strong class="font-bold">Nota:</strong> Los resultados de la IA son sugerencias y deben ser revisados académicamente por su asesor. La selección guardada se conserva solo en este dispositivo durante 5 días.
        </p>
      </div>

      <div v-if="hasError" class="mb-10 p-5 bg-red-50 border-l-4 border-red-400 flex items-start gap-3">
        <span class="material-symbols-outlined text-red-600">error</span>
        <div>
          <p class="text-sm text-red-800 font-bold">No se pudieron generar las propuestas.</p>
          <p class="text-sm text-red-700 mt-1">{{ errorMessage }}</p>
          <button
            v-if="canRetry"
            @click="retryGeneration"
            type="button"
            class="mt-4 inline-flex items-center gap-2 bg-red-600 text-white px-4 py-2 text-xs font-bold uppercase tracking-wider hover:bg-red-700 transition-colors"
          >
            <span class="material-symbols-outlined text-sm">refresh</span>
            Reintentar
          </button>
        </div>
      </div>

      <!-- Proposals List -->
      <div v-if="proposals.length" class="space-y-4 flex-1">
        <label 
          v-for="(item, index) in proposals" 
          :key="index"
          class="block bg-surface border rounded-none cursor-pointer overflow-hidden group transition-all duration-200"
          :class="selectedIndices.includes(index) ? 'border-primary shadow-[0_10px_15px_-3px_rgba(0,86,163,0.1)]' : savedTitleSet.has(item.t) ? 'border-emerald-500 shadow-[0_10px_15px_-3px_rgba(16,185,129,0.12)]' : 'border-border-color hover:border-primary/50'"
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
                 :class="selectedIndices.includes(index) ? 'border-primary bg-primary text-white' : savedTitleSet.has(item.t) ? 'border-emerald-500 bg-emerald-500 text-white' : 'border-border-color text-text-muted group-hover:bg-primary/5 group-hover:text-primary'">
              <span class="material-symbols-outlined transition-transform"
                    :class="selectedIndices.includes(index) || savedTitleSet.has(item.t) ? 'scale-110' : ''">
                {{ selectedIndices.includes(index) ? 'check_circle' : savedTitleSet.has(item.t) ? 'bookmark_added' : 'add_circle' }}
              </span>
            </div>
            
            <div class="flex-1 p-6">
              <div class="flex items-start justify-between gap-4 mb-4">
                <h3 class="font-display font-bold text-lg text-primary leading-snug">{{ item.t }}</h3>
                <span
                  v-if="savedTitleSet.has(item.t)"
                  class="shrink-0 text-[10px] font-bold uppercase tracking-[0.08em] px-2 py-1 rounded-sm bg-emerald-100 text-emerald-700"
                >
                  Guardado
                </span>
              </div>
              
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
          
          <button
            @click="startNewTitleFlow"
            type="button"
            class="bg-primary text-white px-5 py-3 font-bold uppercase tracking-wider text-xs hover:bg-primary/90 transition-all flex items-center gap-2"
          >
            <span class="material-symbols-outlined text-lg">refresh</span>
            Generar Nuevo Titulo
          </button>
        </div>
      </div>
    
    </div>
  </div>
</template>
