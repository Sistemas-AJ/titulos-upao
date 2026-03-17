<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useWizardStore } from '@/store/wizard'
import { generateProposals } from '@/services/api'
import WizardFooter from '@/components/ui/WizardFooter.vue'

const router = useRouter()
const store = useWizardStore()
const isSubmitting = ref(false)

// Local state for the form bound to Pinia defaults
const form = ref({
  scopeType: 'single',
  accessConfirmed: false,
  companyType: 'privada',
  name: '',
  count: null,
  description: '',
  sector: '',
  customSector: '',
  problem: ''
})

onMounted(() => {
  // Restore state if available
  if (store.step3.scopeType) {
    form.value = { ...store.step3 }
  }
})

watch(form, (newVal) => {
  store.setStep3(newVal)
}, { deep: true })

const isGroup = computed(() => form.value.scopeType === 'group')

const canContinue = computed(() => {
  const sectorValid = form.value.sector === 'otro' ? form.value.customSector.trim() !== '' : form.value.sector !== ''
  const baseValidation = form.value.accessConfirmed && 
                         form.value.name.trim() !== '' && 
                         form.value.description.trim() !== '' &&
                         sectorValid &&
                         form.value.problem.trim() !== ''
                         
  if (isGroup.value) {
    return baseValidation && form.value.count > 0
  }
  return baseValidation
})

const goBack = () => {
  store.setStep3(form.value) // Save progress before leaving
  router.push('/paso-2')
}

const submitForm = async () => {
  if (!canContinue.value) return

  store.setStep3(form.value)
  store.startProposalGeneration()
  isSubmitting.value = true

  await router.push('/paso-4')

  try {
    const response = await generateProposals(store.$state)
    store.setGeneratedProposals({
      proposals: response.proposals,
      sessionId: response.session_id
    })
  } catch (error) {
    console.error('Failed to generate proposals:', error)
    store.setProposalError({
      message: error.message,
      retryable: Boolean(error.retryable)
    })
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-[1000px] w-full mx-auto p-12 flex-1 flex flex-col">
    <!-- Header -->
    <header class="mb-12">
      <h2 class="font-display font-bold text-5xl text-primary mb-4">Unidad de Investigación</h2>
      <p class="text-text-muted text-xl max-w-3xl leading-relaxed">
        Defina el contexto y el acceso a la información para su estudio contable.
      </p>
      <div class="h-1 w-20 bg-accent mt-6 rounded-full"></div>
    </header>

    <!-- Form Area -->
    <form @submit.prevent="submitForm" class="w-full flex-1 flex flex-col">
      
      <!-- Row 1: Segmented Control Toggle -->
      <div class="flex items-start mb-8">
        <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">¿Dónde realizará la investigación?</label>
        <div class="flex-grow max-w-[640px]">
          <div class="inline-flex bg-background-light p-1 w-full border border-border-color">
            <label class="flex-1 flex items-center justify-center cursor-pointer font-bold text-sm h-10 transition-all"
                   :class="!isGroup ? 'bg-surface text-primary shadow-sm border border-border-color/50' : 'text-text-muted hover:text-text-main'">
              <input type="radio" v-model="form.scopeType" value="single" class="hidden" />
              Empresa en específico
            </label>
            <label class="flex-1 flex items-center justify-center cursor-pointer font-bold text-sm h-10 transition-all"
                   :class="isGroup ? 'bg-surface text-primary shadow-sm border border-border-color/50' : 'text-text-muted hover:text-text-main'">
              <input type="radio" v-model="form.scopeType" value="group" class="hidden" />
              Conjunto de empresas
            </label>
          </div>
        </div>
      </div>

      <!-- Row 2: Checkbox Acceso (Mandatory) -->
      <div class="flex items-start mb-10">
        <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">Acceso a información</label>
        <div class="flex-grow max-w-[640px]">
          <div class="flex items-start gap-4 p-5 border border-border-color bg-background-light transition-colors hover:border-primary/20">
            <div class="flex items-center h-6">
              <input 
                v-model="form.accessConfirmed"
                id="access-confirm" 
                type="checkbox" 
                class="h-5 w-5 text-primary border-border-color cursor-pointer focus:ring-primary"
              />
            </div>
            <div class="text-sm">
              <label for="access-confirm" class="font-bold text-text-main cursor-pointer">Confirmo que tengo acceso a la información necesaria para la investigación</label>
              <p class="text-text-muted mt-1.5 leading-relaxed">Si no se cuenta con acceso, se mostrará una advertencia en el reporte final sobre la viabilidad del estudio.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Common Fields Container -->
      <div class="space-y-8">
        <!-- Tipo de empresa -->
        <div class="flex items-start">
          <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">Tipo de empresa</label>
          <div class="flex-grow max-w-[640px]">
            <div class="flex gap-10 items-center py-2">
              <label class="flex items-center gap-3 cursor-pointer group">
                <input v-model="form.companyType" type="radio" value="privada" class="w-5 h-5 text-primary border-border-color focus:ring-primary" />
                <span class="text-sm font-bold group-hover:text-primary transition-colors" :class="form.companyType === 'privada' ? 'text-primary' : 'text-text-main'">Privada</span>
              </label>
              <label class="flex items-center gap-3 cursor-pointer group">
                <input v-model="form.companyType" type="radio" value="publica" class="w-5 h-5 text-primary border-border-color focus:ring-primary" />
                <span class="text-sm font-bold group-hover:text-primary transition-colors" :class="form.companyType === 'publica' ? 'text-primary' : 'text-text-main'">Pública</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Nombre / Identificación (Dynamic label) -->
        <div class="flex items-start">
          <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">
            {{ isGroup ? 'Identificación del grupo' : 'Nombre de la empresa' }}
          </label>
          <div class="flex-grow max-w-[640px] relative">
            <input 
              v-model="form.name"
              type="text" 
              class="w-full h-12 border border-border-color bg-surface px-4 text-sm text-text-main focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all outline-none"
              :placeholder="isGroup ? 'Ej. Sector Retail Norte' : 'Ej. Constructora del Norte S.A.C.'" 
            />
          </div>
        </div>

        <!-- Cantidad de empresas (Conditional - Only for Group) -->
        <div v-if="isGroup" class="flex items-start animate-fadeIn">
          <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">Cantidad aprox. de empresas</label>
          <div class="flex-grow max-w-[640px]">
            <input 
              v-model.number="form.count"
              type="number" 
              min="1"
              class="w-full h-12 border border-border-color bg-surface px-4 text-sm text-text-main focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all outline-none"
              placeholder="Ej. 15" 
            />
          </div>
        </div>

        <!-- Descripción (Dynamic label) -->
        <div class="flex items-start">
          <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">
            {{ isGroup ? 'Descripción del grupo' : 'Descripción de la empresa' }}
          </label>
          <div class="flex-grow max-w-[640px]">
            <textarea 
              v-model="form.description"
              class="w-full h-[100px] border border-border-color bg-surface p-4 text-sm text-text-main focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all outline-none resize-y"
              placeholder="Breve reseña sobre la actividad, alcance y ubicación geográfica..."
            ></textarea>
          </div>
        </div>

        <!-- Giro de negocio -->
        <div class="flex items-start">
          <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">Giro de negocio</label>
          <div class="flex-grow max-w-[640px]">
            <div class="relative">
              <select 
                v-model="form.sector"
                class="w-full h-12 border border-border-color bg-surface px-4 text-sm text-text-main focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all outline-none appearance-none cursor-pointer pr-10"
              >
                <option disabled value="">Seleccione un giro...</option>
                <option value="retail">Retail / Comercio al por menor</option>
                <option value="manufactura">Manufactura e Industria</option>
                <option value="servicios">Servicios</option>
                <option value="agronegocios">Agronegocios</option>
                <option value="construccion">Construcción e Inmobiliaria</option>
                <option value="salud">Salud</option>
                <option value="educacion">Educación</option>
                <option value="otro">Otro</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-primary">
                <span class="material-symbols-outlined">expand_more</span>
              </div>
            </div>
            
            <!-- Conditional custom sector input -->
            <div v-if="form.sector === 'otro'" class="mt-4 animate-fadeIn">
              <input 
                v-model="form.customSector"
                type="text" 
                class="w-full h-12 border border-border-color bg-surface px-4 text-sm text-text-main focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all outline-none"
                placeholder="Especifique el giro de negocio" 
              />
            </div>
          </div>
        </div>

        <!-- Principal problemática -->
        <div class="flex items-start">
          <label class="w-[240px] flex-shrink-0 font-bold pt-3 text-text-main text-sm">Principal problemática</label>
          <div class="flex-grow max-w-[640px]">
            <textarea 
              v-model="form.problem"
              class="w-full h-[160px] border border-border-color bg-surface p-4 text-sm text-text-main focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all outline-none resize-y"
              placeholder="Detalle el problema identificado, causas y efectos observados en la gestión contable o financiera..."
            ></textarea>
            <p class="text-[11px] text-text-muted mt-3 font-medium tracking-wide uppercase">Describa la situación problemática empírica que motiva su investigación.</p>
          </div>
        </div>
      </div>

    </form>

    <!-- Action Footer -->
    <WizardFooter 
      :can-continue="canContinue" 
      :is-loading="isSubmitting"
      continue-text="Generar Propuestas"
      color="secondary"
      icon="magic_button"
      :show-back="true"
      @back="goBack"
      @next="submitForm"
    />
  </div>
</template>
