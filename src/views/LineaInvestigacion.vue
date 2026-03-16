<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWizardStore } from '@/store/wizard'
import { getResearchCatalog } from '@/services/api'
import DomainCard from '@/components/ui/DomainCard.vue'
import SublineCard from '@/components/ui/SublineCard.vue'
import WizardFooter from '@/components/ui/WizardFooter.vue'

const router = useRouter()
const store = useWizardStore()

const selectedDomain = ref('')
const selectedSubline = ref('')
const dynamicDomains = ref([])

const domainFallbackMap = {
  tributacion: {
    title: 'Tributación',
    description: 'Análisis crítico de la política fiscal y su impacto empresarial. Enfocada en el cumplimiento normativo, estrategias de planeamiento legal y la defensa del contribuyente ante la administración.',
    icon: 'account_balance'
  },
  finanzas: {
    title: 'Finanzas',
    description: 'Investigación sobre la gestión de recursos de capital, valoración de empresas y mercados financieros. Fundamental para el desarrollo de modelos de inversión y sostenibilidad corporativa.',
    icon: 'analytics'
  },
  auditoria: {
    title: 'Auditoría',
    description: 'Examen sistemático de la información y procesos para garantizar la transparencia. Abarca el control interno preventivo y la detección de riesgos en diversos entornos organizacionales.',
    icon: 'fact_check'
  },
  contabilidad: {
    title: 'Contabilidad',
    description: 'Estudio de la doctrina contable y las NIIF. Se centra en la arquitectura de la información financiera y su utilidad para la toma de decisiones económicas en un entorno globalizado.',
    icon: 'menu_book'
  },
  costos: {
    title: 'Costos',
    description: 'Optimización de la cadena de valor y gestión estratégica de recursos. Esencial para la determinación de precios, rentabilidad de procesos y control de eficiencia operativa.',
    icon: 'calculate'
  }
}

const sublineFallbackMap = {
  forense: { title: 'Auditoría Forense', icon: 'policy' },
  cumplimiento: { title: 'Cumplimiento Normativo', icon: 'gavel' },
  operativa: { title: 'Auditoría Operativa', icon: 'settings_suggest' },
  gestion: { title: 'Auditoría de Gestión', icon: 'admin_panel_settings' },
  gubernamental: { title: 'Auditoría Gubernamental', icon: 'account_balance_wallet' },
  interna: { title: 'Control Interno', icon: 'verified' },
  sistemas: { title: 'Auditoría de Sistemas', icon: 'database' },
  tributaria: { title: 'Auditoría Tributaria', icon: 'receipt_long' },
  ambiental: { title: 'Auditoría Ambiental', icon: 'eco' },
  etica: { title: 'Ética y Responsabilidad', icon: 'balance' }
}

onMounted(() => {
  // Restore state if returning from step 2
  if (store.step1.domain) {
    selectedDomain.value = store.step1.domain
    selectedSubline.value = store.step1.subline
  }
  loadResearchCatalog()
})

const buildFallbackCatalog = () => (
  Object.entries(domainFallbackMap).map(([value, meta]) => ({
    value,
    title: meta.title,
    description: meta.description,
    icon: meta.icon,
    sublines: Object.entries(sublineFallbackMap).map(([subValue, subMeta]) => ({
      value: subValue,
      title: subMeta.title,
      icon: subMeta.icon
    }))
  }))
)

const enrichCatalog = (catalog) => {
  if (!catalog.length) return buildFallbackCatalog()

  return catalog.map((domain) => {
    const fallbackDomain = domainFallbackMap[domain.value] || {}
    return {
      value: domain.value,
      title: domain.title || fallbackDomain.title || domain.value,
      description: domain.description || fallbackDomain.description || 'Línea de investigación disponible en el catálogo institucional.',
      icon: fallbackDomain.icon || 'menu_book',
      sublines: (domain.sublines || []).map((subline) => {
        const fallbackSubline = sublineFallbackMap[subline.value] || {}
        return {
          value: subline.value,
          title: subline.title || fallbackSubline.title || subline.value,
          icon: fallbackSubline.icon || 'sell'
        }
      })
    }
  })
}

const loadResearchCatalog = async () => {
  const catalog = await getResearchCatalog()
  dynamicDomains.value = enrichCatalog(catalog)
}

const domains = computed(() => dynamicDomains.value.length ? dynamicDomains.value : buildFallbackCatalog())

const sublines = computed(() => {
  const selected = domains.value.find((domain) => domain.value === selectedDomain.value)
  return selected?.sublines || []
})

const canContinue = computed(() => {
  return selectedDomain.value !== '' && selectedSubline.value !== ''
})

const handleDomainSelection = (value) => {
  if (selectedDomain.value !== value) {
    selectedDomain.value = value
    // Reset secondary selection when primary changes
    selectedSubline.value = ''
  }
}

const submitForm = () => {
  if (!canContinue.value) return
  
  // Save to store
  store.setStep1(selectedDomain.value, selectedSubline.value)
  
  // Route to step 2
  router.push('/paso-2')
}

</script>

<template>
  <div class="max-w-[1200px] w-full mx-auto p-12 flex-1 flex flex-col">
    <!-- Header -->
    <header class="mb-12">
      <h2 class="font-display font-bold text-5xl text-primary mb-4">Selección de Línea de Investigación</h2>
      <p class="text-text-muted text-xl max-w-3xl leading-relaxed">
          Para iniciar su proceso de graduación, elija el área de especialización contable en la que desea centrar su estudio. Esta elección determinará las variables y el marco normativo aplicable a su investigación académica.
      </p>
    </header>

    <!-- Form -->
    <form class="flex-1 flex flex-col" @submit.prevent="submitForm">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <DomainCard 
          v-for="domain in domains" 
          :key="domain.value"
          :value="domain.value"
          :title="domain.title"
          :description="domain.description"
          :icon="domain.icon"
          :modelValue="selectedDomain"
          @update:modelValue="handleDomainSelection"
        />
      </div>

      <!-- Sub-lines Section (Visible when main line selected) -->
      <transition 
        enter-active-class="transition ease-out duration-400"
        enter-from-class="opacity-0 translate-y-[10px]"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-[10px]"
      >
        <div v-show="selectedDomain" class="mb-16 border-t-2 border-primary/10 pt-12">
          <div class="flex items-center gap-4 mb-8">
            <div class="h-px bg-primary/20 flex-1"></div>
            <h4 class="font-display text-xl font-bold text-primary uppercase tracking-wider text-center px-4">Especifique su Sub-línea de Investigación</h4>
            <div class="h-px bg-primary/20 flex-1"></div>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
            <SublineCard 
              v-for="subline in sublines"
              :key="subline.value"
              :value="subline.value"
              :title="subline.title"
              :icon="subline.icon"
              v-model="selectedSubline"
            />
          </div>
        </div>
      </transition>

      <!-- Action Area -->
      <WizardFooter 
        :can-continue="canContinue" 
        continue-text="Continuar Proceso"
        @next="submitForm"
      >
        <template #info>
          <div class="flex items-center gap-3 text-muted">
            <span class="material-symbols-outlined text-primary text-xl">info</span>
            <div class="text-xs font-body leading-tight">
              <p class="font-bold text-text-main">Flujo de Selección:</p>
              <p class="italic">1. Elija Línea Principal &nbsp;&rarr;&nbsp; 2. Especifique Sub-línea &nbsp;&rarr;&nbsp; 3. Continuar</p>
            </div>
          </div>
        </template>
      </WizardFooter>
    </form>
  </div>
</template>
