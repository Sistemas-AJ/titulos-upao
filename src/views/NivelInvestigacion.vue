<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWizardStore } from '@/store/wizard'
import LevelOption from '@/components/ui/LevelOption.vue'
import WizardFooter from '@/components/ui/WizardFooter.vue'

const router = useRouter()
const store = useWizardStore()

const selectedLevel = ref('correlacional')

onMounted(() => {
  // Restore selection if previously made
  if (store.step2.level) {
    selectedLevel.value = store.step2.level
  }
})

// Data derived from paso 2.html
const levels = [
  { value: 'correlacional', title: 'Correlacional', subtitle: 'Relación entre variables' },
  { value: 'explicativo', title: 'Explicativo / Causal', subtitle: 'Causa y efecto' },
  { value: 'aplicativo', title: 'Aplicativo / Propuesta', subtitle: 'Solución a problemas' }
]

const levelDetails = {
  correlacional: {
    number: '01',
    title: 'Base Metodológica: Correlacional',
    description: 'Este nivel tiene como propósito evaluar la relación que existe entre dos o más conceptos, categorías o variables en un contexto en particular. En el ámbito de la Auditoría, suele medir cómo una práctica afecta un resultado financiero.',
    requirements: [
      'Mínimo dos variables claramente definibles (V1 y V2).',
      'Necesidad de data histórica o encuestas validadas estadísticamente.',
      'Prueba de hipótesis mediante estadísticos de correlación (Pearson / Spearman).'
    ],
    examples: [
      '"El control interno de inventarios y su relación con la liquidez en empresas del sector retail en Trujillo, 2023."',
      '"Auditoría tributaria preventiva y el cumplimiento de obligaciones fiscales en MYPEs manufactureras de La Libertad."'
    ]
  },
  explicativo: {
    number: '02',
    title: 'Base Metodológica: Explicativo',
    description: 'Está dirigido a responder por las causas de los eventos y fenómenos. Se enfoca en explicar por qué ocurre un fenómeno y en qué condiciones se manifiesta.',
    requirements: [
      'Identificación clara de variables dependientes e independientes.',
      'Diseño cuasi-experimental o experimental.',
      'Análisis de regresión o ANOVA para confirmar causalidad.'
    ],
    examples: [
      '"Determinantes de la evasión fiscal en las empresas de servicios de transporte interprovincial."',
      '"Impacto de la auditoría continua en la reducción de fraudes corporativos en el sector bancario."'
    ]
  },
  aplicativo: {
    number: '03',
    title: 'Base Metodológica: Aplicativo',
    description: 'Investigación orientada a resolver problemas prácticos con finalidades de desarrollo metodológico. Busca implementar mejoras a un proceso específico.',
    requirements: [
      'Diagnóstico inicial del problema en una entidad real.',
      'Diseño de una propuesta metodológica documentada.',
      'Proyección de resultados o validación por expertos de la propuesta.'
    ],
    examples: [
      '"Propuesta de un sistema de control de costos basado en actividades para mejorar la rentabilidad de la Clínica San José."',
      '"Modelo de auditoría forense digital para la detección de lavado de activos en cooperativas de ahorro y crédito."'
    ]
  }
}

const currentDetails = computed(() => levelDetails[selectedLevel.value])

const goBack = () => {
  router.push('/paso-1')
}

const goNext = () => {
  store.setStep2(selectedLevel.value)
  router.push('/paso-3')
}
</script>

<template>
  <div class="max-w-[1200px] w-full mx-auto p-12 flex-1 flex flex-col">
    <!-- Header -->
    <header class="mb-12">
      <h2 class="font-display font-bold text-5xl text-primary mb-4">Defina el Nivel de Investigación</h2>
      <p class="text-text-muted text-xl max-w-3xl leading-relaxed">
        Seleccione el alcance metodológico para su tesis en {{ store.step1.subline || 'Auditoría' }}. Esto determinará la profundidad del análisis y la estructura de su marco teórico.
      </p>
    </header>

    <!-- Disclaimer -->
    <div class="mb-10 flex items-center gap-4 p-5 bg-primary/5 border-l-4 border-primary">
      <span class="material-symbols-outlined text-primary">info</span>
      <p class="text-sm text-text-main">
        <strong class="font-bold">Nota Académica:</strong> La IA proporciona sugerencias basadas en patrones de investigación. Valide siempre la elección con su director de tesis según la normativa vigente de la UPAO.
      </p>
    </div>

    <!-- Split Layout -->
    <div class="flex-1 grid grid-cols-[1fr_1.5fr] gap-12 items-start h-full pb-10">
      
      <!-- Left Column: Selection List -->
      <div class="flex flex-col gap-5">
        <LevelOption 
          v-for="level in levels" 
          :key="level.value"
          :value="level.value"
          :title="level.title"
          :subtitle="level.subtitle"
          v-model="selectedLevel"
        />
      </div>

      <!-- Right Column: Context Panel -->
      <transition 
        enter-active-class="transition ease-out duration-300 transform"
        enter-from-class="opacity-0 translate-x-4"
        enter-to-class="opacity-100 translate-x-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0 hidden"
        mode="out-in"
      >
        <div :key="selectedLevel" class="bg-surface p-12 border-2 border-border-color shadow-2xl relative h-full flex flex-col justify-center">
          <div class="absolute top-0 right-0 p-4">
            <span class="text-primary/10 font-display text-8xl font-black select-none">{{ currentDetails.number }}</span>
          </div>

          <div class="relative z-10 flex-1 flex flex-col">
            <div class="mb-10">
              <h3 class="font-display font-bold text-3xl text-primary mb-6">{{ currentDetails.title }}</h3>
              <p class="text-text-main leading-relaxed text-sm">
                {{ currentDetails.description }}
              </p>
            </div>

            <div class="mb-12">
              <h4 class="text-xs font-black uppercase tracking-[0.25em] text-accent mb-6 pb-2 border-b-2 border-accent/20 inline-block">
                Requisitos Académicos
              </h4>
              <ul class="space-y-4">
                <li v-for="(req, idx) in currentDetails.requirements" :key="idx" class="flex items-start gap-4 text-text-main">
                  <span class="material-symbols-outlined text-primary text-xl mt-0.5">check_circle</span>
                  <span class="text-sm font-medium">{{ req }}</span>
                </li>
              </ul>
            </div>

            <div class="mt-auto">
              <h4 class="text-xs font-black uppercase tracking-[0.25em] text-accent mb-8 pb-2 border-b-2 border-accent/20 inline-block">
                Ejemplos de Títulos UPAO
              </h4>
              <div class="space-y-6">
                <div v-for="(example, idx) in currentDetails.examples" :key="idx" class="pl-6 border-l-4 border-primary">
                  <p class="font-display italic text-lg text-text-main leading-tight">
                    {{ example }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
      
    </div>

    <!-- Action Footer -->
    <WizardFooter 
      :can-continue="true" 
      continue-text="Continuar al Alcance"
      :show-back="true"
      @back="goBack"
      @next="goNext"
    />
  </div>
</template>
