<script setup>
import { computed, ref, watch } from 'vue'
import { loginUser, registerUser } from '@/services/api'
import { useAuthStore } from '@/store/auth'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Inicia sesion para continuar'
  },
  description: {
    type: String,
    default: 'Necesitas una cuenta para guardar tus titulos seleccionados.'
  }
})

const emit = defineEmits(['update:modelValue', 'authenticated'])

const authStore = useAuthStore()
const mode = ref('login')
const isSubmitting = ref(false)
const errorMessage = ref('')

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  full_name: '',
  email: '',
  password: ''
})

watch(
  () => props.modelValue,
  (isOpen) => {
    if (!isOpen) {
      errorMessage.value = ''
      isSubmitting.value = false
    }
  }
)

const submitLabel = computed(() => (mode.value === 'login' ? 'Ingresar' : 'Crear cuenta'))

const close = () => {
  emit('update:modelValue', false)
}

const handleSubmit = async () => {
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    if (mode.value === 'register') {
      await registerUser(registerForm.value)
      const loginResponse = await loginUser({
        email: registerForm.value.email,
        password: registerForm.value.password
      })
      authStore.setSession({
        token: loginResponse.access_token,
        user: loginResponse.user
      })
    } else {
      const loginResponse = await loginUser(loginForm.value)
      authStore.setSession({
        token: loginResponse.access_token,
        user: loginResponse.user
      })
    }

    emit('authenticated', authStore.user)
    close()
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo completar la autenticacion'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div v-if="modelValue" class="fixed inset-0 z-[80] bg-slate-950/45 backdrop-blur-sm flex items-center justify-center px-6">
    <div class="w-full max-w-xl bg-white border border-border-color shadow-2xl">
      <header class="px-8 py-6 border-b border-border-color">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.24em] text-secondary mb-2">Cuenta requerida</p>
            <h3 class="font-display text-3xl font-bold text-primary">{{ title }}</h3>
            <p class="mt-2 text-sm text-text-muted">{{ description }}</p>
          </div>
          <button class="text-text-muted hover:text-primary transition-colors" @click="close">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
      </header>

      <div class="px-8 pt-6">
        <div class="inline-flex bg-background-light p-1 border border-border-color">
          <button
            class="px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] transition-all"
            :class="mode === 'login' ? 'bg-white text-primary border border-border-color' : 'text-text-muted'"
            @click="mode = 'login'"
          >
            Iniciar sesion
          </button>
          <button
            class="px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] transition-all"
            :class="mode === 'register' ? 'bg-white text-primary border border-border-color' : 'text-text-muted'"
            @click="mode = 'register'"
          >
            Crear cuenta
          </button>
        </div>
      </div>

      <form class="px-8 py-6 space-y-5" @submit.prevent="handleSubmit">
        <div v-if="mode === 'register'">
          <label class="block text-xs font-bold uppercase tracking-[0.18em] text-text-muted mb-2">Nombre completo</label>
          <input
            v-model="registerForm.full_name"
            type="text"
            class="w-full h-12 border border-border-color bg-surface px-4 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary/20"
            placeholder="Tu nombre"
            required
          />
        </div>

        <template v-if="mode === 'login'">
          <div>
            <label class="block text-xs font-bold uppercase tracking-[0.18em] text-text-muted mb-2">Correo</label>
            <input
              v-model="loginForm.email"
              type="email"
              class="w-full h-12 border border-border-color bg-surface px-4 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary/20"
              placeholder="correo@ejemplo.com"
              required
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-[0.18em] text-text-muted mb-2">Contrasena</label>
            <input
              v-model="loginForm.password"
              type="password"
              class="w-full h-12 border border-border-color bg-surface px-4 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary/20"
              placeholder="Minimo 8 caracteres"
              required
            />
          </div>
        </template>

        <template v-else>
          <div>
            <label class="block text-xs font-bold uppercase tracking-[0.18em] text-text-muted mb-2">Correo</label>
            <input
              v-model="registerForm.email"
              type="email"
              class="w-full h-12 border border-border-color bg-surface px-4 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary/20"
              placeholder="correo@ejemplo.com"
              required
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase tracking-[0.18em] text-text-muted mb-2">Contrasena</label>
            <input
              v-model="registerForm.password"
              type="password"
              class="w-full h-12 border border-border-color bg-surface px-4 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary/20"
              placeholder="Minimo 8 caracteres"
              required
            />
          </div>
        </template>

        <div class="rounded-sm border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          reCAPTCHA queda en proceso. 
        </div>

        <p v-if="errorMessage" class="text-sm text-red-700">{{ errorMessage }}</p>

        <div class="flex items-center justify-between gap-4 pt-2">
          <button
            type="button"
            class="px-5 py-3 border border-border-color text-sm font-semibold text-text-main hover:border-primary hover:text-primary transition-colors"
            @click="close"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="px-6 py-3 bg-primary text-white text-sm font-bold uppercase tracking-[0.18em] hover:brightness-110 transition-all disabled:opacity-60"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Procesando...' : submitLabel }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
