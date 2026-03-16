<script setup>
import { ref, computed } from 'vue'

// Simulated backend data
const allRecords = ref([
  {
    id: 'T-2023-0452',
    linea: 'Tributación Nacional',
    categoria: 'Tributación',
    titulo: 'Impacto de la recaudación del impuesto predial en la gestión financiera de la Municipalidad de Trujillo, 2022',
    autor: 'Castillo Mendoza, Roberto',
    fecha: '12/11/2023',
    estado: 'Aprobada',
    estadoIcon: 'check_circle',
    estadoColor: 'text-green-600'
  },
  {
    id: 'T-2023-0918',
    linea: 'Tributación Empresarial',
    categoria: 'Tributación',
    titulo: 'Estrategias de planeamiento tributario y su relación con la rentabilidad en empresas del sector construcción',
    autor: 'Díaz Palacios, Elena',
    fecha: '05/08/2022',
    estado: 'Aprobada',
    estadoIcon: 'check_circle',
    estadoColor: 'text-green-600'
  },
  {
    id: 'T-2024-0124',
    linea: 'Derecho Tributario',
    categoria: 'Tributación',
    titulo: 'Análisis de la elusión fiscal en el marco de la Norma XVI del Título Preliminar del Código Tributario',
    autor: 'Ruiz Galarreta, Carlos',
    fecha: '15/01/2024',
    estado: 'En Revisión',
    estadoIcon: 'pending',
    estadoColor: 'text-secondary'
  },
  {
    id: 'T-2023-0876',
    linea: 'Política Fiscal',
    categoria: 'Tributación',
    titulo: 'Incidencia de los incentivos tributarios en la inversión de las Micro y Pequeñas Empresas de la Región La Libertad',
    autor: 'Sánchez Flores, María',
    fecha: '20/10/2023',
    estado: 'Aprobada',
    estadoIcon: 'check_circle',
    estadoColor: 'text-green-600'
  },
  {
    id: 'F-2023-0321',
    linea: 'Finanzas Corporativas',
    categoria: 'Finanzas',
    titulo: 'Gestión del riesgo financiero y su impacto en la rentabilidad de las empresas del sector minero, 2022',
    autor: 'Torres Vera, Andrés',
    fecha: '08/07/2023',
    estado: 'Aprobada',
    estadoIcon: 'check_circle',
    estadoColor: 'text-green-600'
  },
  {
    id: 'F-2022-0755',
    linea: 'Mercados de Capital',
    categoria: 'Finanzas',
    titulo: 'Análisis del apalancamiento financiero y su efecto en el valor de las empresas listadas en la BVL, 2020-2022',
    autor: 'López Campos, Paola',
    fecha: '22/03/2022',
    estado: 'Aprobada',
    estadoIcon: 'check_circle',
    estadoColor: 'text-green-600'
  },
  {
    id: 'A-2023-0610',
    linea: 'Auditoría Interna',
    categoria: 'Auditoría',
    titulo: 'El control interno y su relación con la gestión administrativa en las instituciones educativas públicas de Piura, 2022',
    autor: 'Guerrero Neyra, Sofía',
    fecha: '30/09/2023',
    estado: 'Aprobada',
    estadoIcon: 'check_circle',
    estadoColor: 'text-green-600'
  },
  {
    id: 'C-2024-0053',
    linea: 'Contabilidad de Gestión',
    categoria: 'Contabilidad',
    titulo: 'Implementación de NIIF 15 y su impacto en el reconocimiento de ingresos en empresas constructoras, 2023',
    autor: 'Medina Castillo, Luis',
    fecha: '10/02/2024',
    estado: 'En Revisión',
    estadoIcon: 'pending',
    estadoColor: 'text-secondary'
  },
])

const tabs = ['Todos', 'Tributación', 'Finanzas', 'Auditoría', 'Contabilidad', 'Costos', 'Gestión Pública']
const activeTab = ref('Todos')
const searchQuery = ref('')
const selectedAbstract = ref(null)

const filtered = computed(() => {
  let data = allRecords.value
  if (activeTab.value !== 'Todos') {
    data = data.filter(r => r.categoria === activeTab.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    data = data.filter(r =>
      r.titulo.toLowerCase().includes(q) ||
      r.autor.toLowerCase().includes(q) ||
      r.id.toLowerCase().includes(q)
    )
  }
  return data
})
</script>

<template>
  <div class="max-w-[1100px] w-full mx-auto py-12 px-12 flex-1 flex flex-col">

    <!-- Header -->
    <header class="flex justify-between items-end mb-8">
      <div>
        <h2 class="font-display font-bold text-4xl text-primary leading-tight tracking-tight">Base de Datos de Tesis UPAO</h2>
        <p class="text-text-muted text-lg mt-1 italic">Módulo de consulta interna de títulos e investigaciones registradas.</p>
        <div class="h-1 w-20 bg-secondary mt-4 rounded-full"></div>
      </div>
      <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider bg-background-light border border-border-color px-3 py-2 text-text-muted">
        <span class="material-symbols-outlined text-sm">storage</span>
        Local DB v2.4
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
            placeholder="Buscar por título exacto, autor o código de registro..."
            type="text"
          />
        </div>
        <button class="px-6 py-4 bg-primary text-white font-bold flex items-center gap-2 hover:bg-primary/90 transition-all shadow-lg">
          <span class="material-symbols-outlined">filter_list</span>
          Filtros Avanzados
        </button>
      </div>

      <!-- Category Tabs -->
      <div class="flex border-b border-border-color overflow-x-auto bg-surface px-4">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          class="px-6 py-4 text-sm font-medium whitespace-nowrap transition-colors"
          :class="activeTab === tab
            ? 'border-b-[3px] border-primary text-primary font-bold -mb-px'
            : 'text-text-muted hover:text-primary'"
        >
          {{ tab }}
        </button>
      </div>
    </section>

    <!-- Records Table -->
    <div class="bg-surface border border-border-color divide-y divide-border-color flex-1">
      <div
        v-for="record in filtered"
        :key="record.id"
        class="p-6 hover:bg-background-light transition-colors flex flex-col md:flex-row md:items-center justify-between gap-6 group"
      >
        <div class="flex-1 flex flex-col gap-2">
          <div class="flex items-center gap-3">
            <span class="px-2 py-0.5 bg-blue-100 text-blue-700 text-[10px] font-bold uppercase tracking-wider rounded-sm">{{ record.id }}</span>
            <span class="text-xs text-text-muted font-medium italic">Línea: {{ record.linea }}</span>
          </div>
          <h3 class="font-display font-bold text-lg text-text-main group-hover:text-primary transition-colors cursor-pointer leading-snug">
            {{ record.titulo }}
          </h3>
          <div class="flex items-center gap-6 text-sm text-text-muted flex-wrap">
            <span class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-base">person</span>
              {{ record.autor }}
            </span>
            <span class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-base">calendar_today</span>
              Sustentada: {{ record.fecha }}
            </span>
            <span class="flex items-center gap-1.5" :class="record.estadoColor">
              <span class="material-symbols-outlined text-base">{{ record.estadoIcon }}</span>
              {{ record.estado }}
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
      <div v-if="filtered.length === 0" class="py-24 text-center">
        <span class="material-symbols-outlined text-6xl text-border-color mb-4 block">search_off</span>
        <p class="font-display font-bold text-xl text-text-muted mb-2">Sin resultados</p>
        <p class="text-text-muted text-sm">No se encontraron registros para los filtros aplicados.</p>
      </div>

      <!-- Count Footer -->
      <div v-if="filtered.length > 0" class="bg-background-light border-t border-border-color p-4 text-center">
        <p class="text-xs text-text-muted font-medium italic">
          Mostrando <strong class="text-text-main">{{ filtered.length }}</strong> de <strong class="text-text-main">{{ allRecords.length }}</strong> registros
          <template v-if="activeTab !== 'Todos'"> en la categoría '<strong>{{ activeTab }}</strong>'</template>
        </p>
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-8 flex justify-between items-center pb-8">
      <div class="text-sm text-text-muted">Página 1 de 312</div>
      <nav class="flex items-center gap-1">
        <button class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors disabled:opacity-30" disabled>
          <span class="material-symbols-outlined">chevron_left</span>
        </button>
        <button class="w-10 h-10 flex items-center justify-center bg-primary text-white font-bold text-sm shadow-md">1</button>
        <button class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors text-sm">2</button>
        <button class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors text-sm">3</button>
        <span class="px-2 text-text-muted">...</span>
        <button class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors text-sm">312</button>
        <button class="w-10 h-10 flex items-center justify-center border border-border-color text-text-muted hover:text-primary hover:border-primary transition-colors">
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
        <p class="text-[10px] font-bold uppercase tracking-widest text-secondary mb-2">{{ selectedAbstract.id }} — {{ selectedAbstract.linea }}</p>
        <h3 class="font-display font-bold text-xl text-primary mb-4 leading-snug">{{ selectedAbstract.titulo }}</h3>
        <div class="flex items-center gap-4 text-sm text-text-muted mb-6 border-b border-border-color pb-4">
          <span class="flex items-center gap-1.5">
            <span class="material-symbols-outlined text-base">person</span>
            {{ selectedAbstract.autor }}
          </span>
          <span class="flex items-center gap-1.5">
            <span class="material-symbols-outlined text-base">calendar_today</span>
            {{ selectedAbstract.fecha }}
          </span>
        </div>
        <p class="text-text-muted text-sm leading-relaxed">
          <em>Los datos del abstract se obtendrán desde el backend. Por ahora, este registro corresponde a la investigación registrada bajo el código <strong>{{ selectedAbstract.id }}</strong> con estado: <strong>{{ selectedAbstract.estado }}</strong>.</em>
        </p>
      </div>
    </div>

  </div>
</template>
