<script setup>
import { ref, computed } from 'vue'

// Simulated backend data
const allHistory = ref([
  {
    id: 1,
    domain: 'Auditoría',
    domainColor: 'bg-primary/10 text-primary',
    date: 'Hace 2 horas (12 Oct, 2023)',
    title: 'Impacto de la Auditoría Forense en la Detección de Fraude en Entidades Públicas del Perú: Un Estudio Comparativo 2020–2023',
    variants: 5,
    isFavorite: true
  },
  {
    id: 2,
    domain: 'Administración',
    domainColor: 'bg-blue-50 text-blue-600',
    date: 'Ayer, 16:45',
    title: 'Estrategias de Resiliencia Organizacional en Pymes del Sector Manufacturero Post-Pandemia en la Región La Libertad',
    variants: 3,
    isFavorite: false
  },
  {
    id: 3,
    domain: 'Derecho',
    domainColor: 'bg-amber-50 text-amber-600',
    date: '8 Oct, 2023',
    title: 'La Responsabilidad Civil del Estado en la Gestión de Conflictos Socioambientales: Análisis de la Jurisprudencia Reciente',
    variants: 8,
    isFavorite: false
  },
  {
    id: 4,
    domain: 'Finanzas',
    domainColor: 'bg-emerald-50 text-emerald-700',
    date: '5 Oct, 2023',
    title: 'Rentabilidad del Portafolio de Inversiones y su relación con la Gestión del Riesgo en las AFP Peruanas, 2022',
    variants: 6,
    isFavorite: false
  },
  {
    id: 5,
    domain: 'Tributación',
    domainColor: 'bg-purple-50 text-purple-700',
    date: '1 Oct, 2023',
    title: 'Planeamiento tributario y la reducción de contingencias fiscales en MYPES del sector comercio en Trujillo, 2023',
    variants: 4,
    isFavorite: true
  },
])

const searchQuery = ref('')
const currentPage = ref(1)
const perPage = 10

const filtered = computed(() =>
  allHistory.value.filter(item =>
    item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    item.domain.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

const deleteItem = (id) => {
  const idx = allHistory.value.findIndex(i => i.id === id)
  if (idx !== -1) allHistory.value.splice(idx, 1)
}

const viewItem = (item) => {
  alert(`Abriendo: ${item.title}`)
}

const copyItem = (item) => {
  navigator.clipboard.writeText(item.title).then(() => {
    alert('Título copiado al portapapeles')
  })
}

const downloadItem = (item) => {
  alert(`Descargando: ${item.title}`)
}
</script>

<template>
  <div class="max-w-[1100px] w-full mx-auto py-12 px-12 flex-1 flex flex-col">

    <!-- Page Intro -->
    <div class="mb-10">
      <h2 class="font-display font-bold text-4xl text-primary leading-tight mb-3">Registro de Consultas</h2>
      <p class="text-text-muted text-lg max-w-2xl leading-relaxed">
        Administra y revisa las propuestas de títulos generadas por el sistema de IA para tus diversas líneas de investigación académica.
      </p>
      <div class="h-1 w-20 bg-secondary mt-6 rounded-full"></div>
    </div>

    <!-- Filters & Search -->
    <div class="flex flex-col md:flex-row gap-4 mb-8">
      <div class="flex-1 relative group">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors">search</span>
        <input 
          v-model="searchQuery"
          class="w-full pl-10 pr-4 py-3 bg-surface border border-border-color focus:ring-1 focus:ring-primary/20 focus:border-primary text-sm transition-all outline-none placeholder:text-text-muted" 
          placeholder="Buscar por título, palabra clave o línea..." 
          type="text"
        />
      </div>
      <div class="flex gap-3">
        <button class="flex items-center gap-2 px-4 py-3 bg-surface border border-border-color text-sm font-semibold hover:bg-background-light transition-colors">
          <span class="material-symbols-outlined text-lg">filter_list</span>
          Líneas
          <span class="material-symbols-outlined text-lg">expand_more</span>
        </button>
        <button class="flex items-center gap-2 px-4 py-3 bg-surface border border-border-color text-sm font-semibold hover:bg-background-light transition-colors">
          <span class="material-symbols-outlined text-lg">calendar_month</span>
          Fecha
          <span class="material-symbols-outlined text-lg">expand_more</span>
        </button>

      </div>
    </div>

    <!-- History List -->
    <div class="flex flex-col gap-4 flex-1">
      <div 
        v-for="item in filtered"
        :key="item.id"
        class="bg-surface border border-border-color p-6 hover:border-primary/40 hover:shadow-md transition-all group"
      >
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-3">
              <span class="px-2 py-1 text-[10px] font-bold uppercase tracking-widest rounded-sm" :class="item.domainColor">{{ item.domain }}</span>
              <span class="text-text-muted text-xs flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">schedule</span>
                {{ item.date }}
              </span>
            </div>
            <h4 class="font-display font-bold text-[17px] text-text-main mb-3 group-hover:text-primary transition-colors leading-snug">{{ item.title }}</h4>
            <div class="flex gap-4">
              <p class="text-sm text-text-muted flex items-center gap-1.5">
                <span class="material-symbols-outlined text-base">description</span>
                {{ item.variants }} variantes generadas
              </p>
              <p v-if="item.isFavorite" class="text-sm text-text-muted flex items-center gap-1.5">
                <span class="material-symbols-outlined text-base text-secondary">star</span>
                Favorito
              </p>
            </div>
          </div>

          <div class="flex items-center gap-1">
            <button @click="viewItem(item)" class="p-2.5 text-text-muted hover:text-primary transition-colors hover:bg-primary/5" title="Ver">
              <span class="material-symbols-outlined">visibility</span>
            </button>
            <button @click="copyItem(item)" class="p-2.5 text-text-muted hover:text-primary transition-colors hover:bg-primary/5" title="Copiar">
              <span class="material-symbols-outlined">content_copy</span>
            </button>
            <button @click="downloadItem(item)" class="p-2.5 text-text-muted hover:text-primary transition-colors hover:bg-primary/5" title="Descargar">
              <span class="material-symbols-outlined">download</span>
            </button>
            <div class="w-[1px] h-8 bg-border-color mx-2"></div>
            <button @click="deleteItem(item.id)" class="p-2.5 text-text-muted hover:text-red-500 transition-colors hover:bg-red-50" title="Eliminar">
              <span class="material-symbols-outlined">delete</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filtered.length === 0" class="flex flex-col items-center justify-center py-24 text-center">
        <span class="material-symbols-outlined text-6xl text-border-color mb-4">manage_search</span>
        <p class="font-display font-bold text-xl text-text-muted mb-2">Sin resultados</p>
        <p class="text-text-muted text-sm">No se encontraron consultas que coincidan con tu búsqueda.</p>
      </div>

      <!-- Pagination -->
      <div v-if="filtered.length > 0" class="mt-8 flex items-center justify-between pt-6 border-t border-border-color">
        <p class="text-sm text-text-muted font-medium">
          Mostrando <strong class="text-text-main">{{ filtered.length }}</strong> de <strong class="text-text-main">{{ allHistory.length }}</strong> consultas
        </p>
        <div class="flex gap-2">
          <button class="w-10 h-10 flex items-center justify-center border border-border-color bg-surface text-text-muted hover:text-primary hover:border-primary transition-colors disabled:opacity-30 disabled:cursor-not-allowed" disabled>
            <span class="material-symbols-outlined">chevron_left</span>
          </button>
          <button class="w-10 h-10 flex items-center justify-center bg-primary text-white font-bold text-sm shadow-md">1</button>
          <button class="w-10 h-10 flex items-center justify-center border border-border-color bg-surface text-text-muted hover:border-primary hover:text-primary transition-colors">
            <span class="material-symbols-outlined">chevron_right</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Summary Card -->
    <div class="mt-12 bg-primary/5 p-8 flex flex-col md:flex-row items-center justify-between border border-primary/10 gap-6">
      <div class="flex items-center gap-6">
        <div class="w-14 h-14 bg-surface flex items-center justify-center text-primary border border-primary/10">
          <span class="material-symbols-outlined text-2xl">insights</span>
        </div>
        <div>
          <h5 class="font-display text-lg font-bold text-text-main mb-1">Resumen Mensual</h5>
          <p class="text-sm text-text-muted">
            Has generado <strong class="text-primary">24 títulos</strong> este mes. Te quedan <strong class="text-primary">76 créditos</strong> de investigación.
          </p>
        </div>
      </div>
      <button class="px-6 py-2.5 border-2 border-primary text-primary font-bold hover:bg-primary hover:text-white transition-all">
        Ver Estadísticas
      </button>
    </div>

  </div>
</template>
