<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { getReferenceTitlesPaged } from '@/services/api'

// We map our visual tabs to the specific backend "linea_investigacion" values. 
// For 'Todos', we will send null/undefined to let the backend return all.
// The possible lines per user requirement are: auditoria, contabilidad, costos, finanzas, tributacion
const tabs = ['Todos', 'auditoria', 'contabilidad', 'costos', 'finanzas', 'tributacion']
const activeTab = ref('Todos')

const years = Array.from({ length: 2026 - 2012 + 1 }, (_, i) => 2026 - i) // 2026 to 2012
const selectedYear = ref('')

const records = ref([])
const isLoading = ref(false)
const searchQuery = ref('')
const debouncedSearch = ref('')
let searchTimeout = null
const selectedAbstract = ref(null)

// Pagination state
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const pageSize = ref(10)

const fetchRecords = async () => {
  isLoading.value = true
  try {
    const linea = activeTab.value === 'Todos' ? null : activeTab.value
    // API Call
    const response = await getReferenceTitlesPaged({
      page: currentPage.value,
      linea_investigacion: linea,
      q: debouncedSearch.value,
      anio: selectedYear.value || undefined
    })
    
    // Schema mapping based on real JSON structure
    records.value = response.items || []
    
    // Mapping exact keys from backend
    if (response.total_pages !== undefined) totalPages.value = response.total_pages
    if (response.total !== undefined) totalItems.value = response.total
    if (response.page_size !== undefined) pageSize.value = response.page_size
    // Ensure currentPage syncs with backend if it modified it
    if (response.page !== undefined) currentPage.value = response.page
  } catch (err) {
    console.error(err)
    records.value = []
  } finally {
    isLoading.value = false
  }
}

// Watchers
watch(activeTab, () => {
  currentPage.value = 1 // Reset to page 1 on tab change
  fetchRecords()
})

watch(selectedYear, () => {
  currentPage.value = 1 // Reset to page 1 on year change
  fetchRecords()
})

watch(currentPage, () => {
  fetchRecords()
})

watch(searchQuery, (newVal) => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    debouncedSearch.value = newVal
    currentPage.value = 1 // Any new search implies we return to page 1
    fetchRecords()
  }, 500) // 500ms debounce
})

onMounted(() => {
  fetchRecords()
})

const getStatusIcon = (status) => {
  const s = (status || '').toUpperCase()
  if (s.includes('APROVADO') || s.includes('APROBADO')) return 'check_circle'
  return 'pending'
}

const getStatusColor = (status) => {
  const s = (status || '').toUpperCase()
  if (s.includes('APROVADO') || s.includes('APROBADO')) return 'text-green-600'
  return 'text-secondary'
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

// Helper para resaltar la búsqueda con color anaranjado
const highlightMatch = (text, term) => {
  if (!text) return ''
  if (!term || term.trim() === '') return text
  
  // Escape caracteres especiales de RegExp en el término de búsqueda
  const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${escapedTerm})`, 'gi')
  
  // Reemplazamos la coincidencia con un span anaranjado
  return text.replace(regex, '<span class="bg-orange-300 text-orange-900 font-bold px-1 rounded-sm">$1</span>')
}

// Compute the visible page buttons to avoid long rows of buttons
const visiblePages = computed(() => {
  const current = currentPage.value;
  const total = totalPages.value;
  const delta = 2; // Number of items to show around current page
  
  if (total <= 7) {
    // Show all if 7 or less
    return Array.from({ length: total }, (_, i) => i + 1);
  }
  
  const pages = [];
  
  // Left side
  if (current - delta > 2) {
    pages.push(1, '...');
    for (let i = current - delta; i <= current; i++) {
        pages.push(i);
    }
  } else {
    for (let i = 1; i <= current; i++) {
        pages.push(i);
    }
  }
  
  // Right side
  if (current + delta < total - 1) {
    for (let i = current + 1; i <= current + delta; i++) {
        pages.push(i);
    }
    pages.push('...', total);
  } else {
    for (let i = current + 1; i <= total; i++) {
        pages.push(i);
    }
  }
  
  return pages;
})
</script>

<template>
  <div class="max-w-[1100px] w-full mx-auto py-12 px-12 flex-1 flex flex-col">

    <!-- Header -->
    <header class="flex justify-between items-end mb-8">
      <div>
        <h2 class="font-display font-bold text-4xl text-primary leading-tight tracking-tight">Base de Datos de Tesis</h2>
        <p class="text-text-muted text-lg mt-1 italic">Módulo de consulta interna de títulos e investigaciones registradas.</p>
        <div class="h-1 w-20 bg-secondary mt-4 rounded-full"></div>
      </div>
      <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider bg-background-light border border-border-color px-3 py-2 text-text-muted">
        <span class="material-symbols-outlined text-sm">cloud_sync</span>
        API Conectada
      </div>
    </header>

    <!-- Search & Filters -->
    <section class="flex flex-col gap-0 mb-0">
      <div class="flex gap-4 mb-4">
        <div class="relative group flex-1">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-primary/50 group-focus-within:text-primary transition-colors">
            <span class="material-symbols-outlined">search</span>
          </div>
          <input
            v-model="searchQuery"
            class="w-full pl-12 pr-4 py-4 bg-surface border-2 border-border-color focus:ring-2 focus:ring-primary/10 focus:border-primary outline-none transition-all text-base"
            placeholder="Buscar por título exacto o autor..."
            type="text"
          />
        </div>
        <div class="relative group w-48 shrink-0">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-primary/50 group-focus-within:text-primary transition-colors">
            <span class="material-symbols-outlined">calendar_today</span>
          </div>
          <select
            v-model="selectedYear"
            class="w-full pl-12 pr-10 py-4 bg-surface border-2 border-border-color focus:ring-2 focus:ring-primary/10 focus:border-primary outline-none transition-all text-base appearance-none cursor-pointer"
          >
            <option value="">Cualquier año</option>
            <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
          </select>
          <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-text-muted">
            <span class="material-symbols-outlined">expand_more</span>
          </div>
        </div>
      </div>

      <!-- Category Tabs -->
      <div class="flex border-b border-border-color overflow-x-auto bg-surface px-4">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          class="px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors capitalize"
          :class="activeTab === tab
            ? 'border-b-[3px] border-primary text-primary font-bold -mb-px'
            : 'text-text-muted hover:text-primary'"
        >
          {{ tab }}
        </button>
      </div>
    </section>

    <!-- Records Table -->
    <div class="bg-surface border border-border-color divide-y divide-border-color flex-1 relative">
      <div v-if="isLoading" class="absolute inset-0 bg-white/80 z-10 flex items-center justify-center">
        <div class="flex flex-col items-center gap-3">
          <span class="material-symbols-outlined animate-spin text-4xl text-primary">sync</span>
          <span class="text-sm font-bold text-primary animate-pulse tracking-widest uppercase">Cargando datos...</span>
        </div>
      </div>

      <div
        v-for="(record, index) in records"
        :key="index"
        class="p-6 hover:bg-background-light transition-colors flex flex-col md:flex-row md:items-center justify-between gap-6 group"
      >
        <div class="flex-1 flex flex-col gap-2">
          <div class="flex items-center gap-3">
            <span class="px-2 py-0.5 bg-blue-100 text-blue-700 text-[10px] font-bold uppercase tracking-wider rounded-sm capitalize">{{ record.linea_investigacion }}</span>
            <span class="text-xs text-text-muted font-medium italic capitalize" v-if="record.sub_linea">Sublínea: {{ record.sub_linea }}</span>
          </div>
          <h3 
            class="font-display font-bold text-lg text-text-main group-hover:text-primary transition-colors cursor-pointer leading-snug"
            v-html="highlightMatch(record.titulo_investigacion, debouncedSearch)"
          ></h3>
          <div class="flex items-center gap-6 text-sm text-text-muted flex-wrap mt-1">
            <span class="flex items-center gap-1.5 capitalize">
              <span class="material-symbols-outlined text-base">person</span>
              <span v-html="highlightMatch(record.authors?.toLowerCase() || 'Desconocido', debouncedSearch)"></span>
            </span>
            <span class="flex items-center gap-1.5 font-medium" v-if="record.anio">
              <span class="material-symbols-outlined text-base">calendar_today</span>
              {{ record.anio }}
            </span>
            <span class="flex items-center gap-1.5 font-medium capitalize" v-if="record.nivel_investigacion">
              <span class="material-symbols-outlined text-base">science</span>
              {{ record.nivel_investigacion }}
            </span>
            <span class="flex items-center gap-1.5 font-medium uppercase text-[11px] tracking-wider" :class="getStatusColor(record.status)">
              <span class="material-symbols-outlined text-base">{{ getStatusIcon(record.status) }}</span>
              {{ record.status || 'SIN ESTADO' }}
            </span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="selectedAbstract = record"
            class="p-2 text-text-muted hover:text-primary transition-colors border border-border-color hover:border-primary"
            title="Ver Abstract"
          >
            <span class="material-symbols-outlined">subject</span>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!isLoading && records.length === 0" class="py-24 text-center">
        <span class="material-symbols-outlined text-6xl text-border-color mb-4 block">search_off</span>
        <p class="font-display font-bold text-xl text-text-muted mb-2">Sin resultados</p>
        <p class="text-text-muted text-sm">No se encontraron registros en esta página o categoría.</p>
      </div>

      <!-- Count Footer -->
      <div v-if="!isLoading && records.length > 0" class="bg-background-light border-t border-border-color p-4 text-center">
        <p class="text-xs text-text-muted font-medium italic">
          Mostrando resultados de la página <strong class="text-text-main">{{ currentPage }}</strong>.
          <template v-if="activeTab !== 'Todos'"> Categoría filtro: '<strong><span class="capitalize">{{ activeTab }}</span></strong>'</template>
        </p>
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-8 flex justify-between items-center pb-8" v-if="totalPages > 0">
      <div class="text-sm text-text-muted">Página <span class="font-bold text-text-main">{{ currentPage }}</span> de <span class="font-bold text-text-main">{{ totalPages }}</span></div>
      <nav class="flex items-center gap-1">
        <button 
          @click="prevPage" 
          :disabled="currentPage === 1"
          class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <span class="material-symbols-outlined">chevron_left</span>
        </button>
        
        <template v-for="(page, idx) in visiblePages" :key="'page-' + idx">
          <button
            v-if="page !== '...'"
            @click="currentPage = page"
            class="w-10 h-10 flex items-center justify-center text-sm transition-colors border"
            :class="currentPage === page
              ? 'bg-primary border-primary text-white font-bold shadow-md'
              : 'border-border-color text-text-muted hover:text-primary hover:border-primary'"
          >
            {{ page }}
          </button>
          <span v-else class="w-10 h-10 flex items-center justify-center text-text-muted font-bold tracking-widest px-1">...</span>
        </template>
        
        <button 
          @click="nextPage" 
          :disabled="currentPage >= totalPages"
          class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <span class="material-symbols-outlined">chevron_right</span>
        </button>
      </nav>
    </div>

    <!-- Abstract Modal -->
    <div
      v-if="selectedAbstract"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-8"
      @click.self="selectedAbstract = null"
    >
      <div class="bg-surface max-w-2xl w-full p-8 shadow-2xl relative">
        <button
          @click="selectedAbstract = null"
          class="absolute top-4 right-4 text-text-muted hover:text-text-main transition-colors"
        >
          <span class="material-symbols-outlined">close</span>
        </button>
        <p class="text-[10px] font-bold uppercase tracking-widest text-secondary mb-2">{{ selectedAbstract.linea_investigacion }} <template v-if="selectedAbstract.sub_linea">— {{ selectedAbstract.sub_linea }}</template></p>
        <h3 class="font-display font-bold text-xl text-primary mb-4 leading-snug">{{ selectedAbstract.titulo_investigacion }}</h3>
        <div class="flex items-center gap-4 text-sm text-text-muted mb-6 border-b border-border-color pb-4 flex-wrap">
          <span class="flex items-center gap-1.5 capitalize">
            <span class="material-symbols-outlined text-base">person</span>
            {{ selectedAbstract.authors?.toLowerCase() || 'Desconocido' }}
          </span>
          <span class="flex items-center gap-1.5 font-medium" v-if="selectedAbstract.anio">
            <span class="material-symbols-outlined text-base">calendar_today</span>
            {{ selectedAbstract.anio }}
          </span>
          <span class="flex items-center gap-1.5 font-medium capitalize" v-if="selectedAbstract.nivel_investigacion">
            <span class="material-symbols-outlined text-base">science</span>
            {{ selectedAbstract.nivel_investigacion }}
          </span>
          <span class="flex items-center gap-1.5 font-medium uppercase text-[11px] tracking-wider" :class="getStatusColor(selectedAbstract.status)">
            <span class="material-symbols-outlined text-base">{{ getStatusIcon(selectedAbstract.status) }}</span>
            {{ selectedAbstract.status || 'SIN ESTADO' }}
          </span>
        </div>
        <p class="text-text-muted text-sm leading-relaxed">
          <em>El equipo de desarrollo pronto habilitará el detalle completo del abstract y la metadata expandida para este título de la base de datos de titulos.</em>
        </p>
      </div>
    </div>

  </div>
</template>
