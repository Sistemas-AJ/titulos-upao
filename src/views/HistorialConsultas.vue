<script setup>
import { computed, onMounted, ref } from 'vue'
import AuthDialog from '@/components/ui/AuthDialog.vue'
import { deleteSavedTitle, listSavedTitles } from '@/services/api'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const showAuthDialog = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const searchQuery = ref('')
const savedCollections = ref([])

const filtered = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return savedCollections.value

  return savedCollections.value.filter((collection) => {
    return (
      collection.linea_investigacion.toLowerCase().includes(query) ||
      collection.sub_linea.toLowerCase().includes(query) ||
      collection.items.some((item) => item.t.toLowerCase().includes(query))
    )
  })
})

const loadHistory = async () => {
  if (!authStore.isAuthenticated) return
  isLoading.value = true
  errorMessage.value = ''
  try {
    savedCollections.value = await listSavedTitles()
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo cargar tu historial'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadHistory)

const formatDate = (value) => new Date(value).toLocaleString('es-PE', {
  dateStyle: 'medium',
  timeStyle: 'short'
})

const copyItem = async (item) => {
  await navigator.clipboard.writeText(item.t)
  alert('Titulo copiado al portapapeles')
}

const downloadCollection = (collection) => {
  const rows = collection.items.map((item, index) => `
    <tr>
      <td>${index + 1}</td>
      <td>${item.t}</td>
      <td>${item.v1}</td>
      <td>${item.c}</td>
      <td>${item.v2}</td>
      <td>${item.u}</td>
      <td>${item.s}</td>
    </tr>
  `).join('')

  const html = `
    <html>
      <head><meta charset="UTF-8" /></head>
      <body>
        <table border="1">
          <tr>
            <th>N</th>
            <th>Titulo</th>
            <th>Variable 1</th>
            <th>Conector</th>
            <th>Variable 2</th>
            <th>Unidad</th>
            <th>Espacio / Tiempo</th>
          </tr>
          ${rows}
        </table>
      </body>
    </html>
  `

  const blob = new Blob([html], { type: 'application/vnd.ms-excel;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `titulos_guardados_${collection.id}.xls`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

const removeCollection = async (collectionId) => {
  if (!window.confirm('Se eliminara este bloque de titulos guardados.')) return
  try {
    await deleteSavedTitle(collectionId)
    savedCollections.value = savedCollections.value.filter((item) => item.id !== collectionId)
  } catch (error) {
    errorMessage.value = error.message || 'No se pudo eliminar el registro'
  }
}

const handleAuthenticated = async () => {
  await loadHistory()
}
</script>

<template>
  <div class="max-w-[1100px] w-full mx-auto py-12 px-12 flex-1 flex flex-col">
    <div class="mb-10">
      <h2 class="font-display font-bold text-4xl text-primary leading-tight mb-3">Titulos Guardados</h2>
      <p class="text-text-muted text-lg max-w-2xl leading-relaxed">
        Aqui solo aparecen los titulos que guardaste manualmente desde las recomendaciones generadas.
      </p>
      <div class="h-1 w-20 bg-secondary mt-6 rounded-full"></div>
    </div>

    <div v-if="!authStore.isAuthenticated" class="border border-border-color bg-surface p-10 text-center">
      <span class="material-symbols-outlined text-5xl text-primary mb-4 block">lock</span>
      <h3 class="font-display text-2xl font-bold text-primary mb-3">Inicia sesion para ver tu historial</h3>
      <p class="text-sm text-text-muted max-w-xl mx-auto mb-6">
        El historial esta ligado a tu usuario. Las propuestas de IA no se conservan automaticamente; solo se listan las que decidiste guardar.
      </p>
      <button
        class="px-6 py-3 bg-primary text-white font-bold uppercase tracking-[0.18em] text-xs hover:brightness-110 transition-all"
        @click="showAuthDialog = true"
      >
        Iniciar sesion o crear cuenta
      </button>
    </div>

    <template v-else>
      <div class="flex flex-col md:flex-row gap-4 mb-8">
        <div class="flex-1 relative group">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors">search</span>
          <input
            v-model="searchQuery"
            class="w-full pl-10 pr-4 py-3 bg-surface border border-border-color focus:ring-1 focus:ring-primary/20 focus:border-primary text-sm transition-all outline-none placeholder:text-text-muted"
            placeholder="Buscar por titulo, linea o sublinea"
            type="text"
          />
        </div>
        <div class="flex items-center gap-3">
          <div class="px-4 py-3 bg-primary/5 border border-primary/10 text-sm text-primary font-semibold">
            {{ filtered.length }} registros
          </div>
          <button
            class="px-4 py-3 border border-border-color text-sm font-semibold hover:border-primary hover:text-primary transition-colors"
            @click="authStore.clearSession()"
          >
            Cerrar sesion
          </button>
        </div>
      </div>

      <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border-l-4 border-red-400 text-sm text-red-800">
        {{ errorMessage }}
      </div>

      <div v-if="isLoading" class="flex-1 flex items-center justify-center py-20">
        <p class="text-sm text-text-muted">Cargando historial...</p>
      </div>

      <div v-else class="space-y-5">
        <div
          v-for="collection in filtered"
          :key="collection.id"
          class="bg-surface border border-border-color p-6 hover:border-primary/30 transition-colors"
        >
          <div class="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
            <div class="flex-1">
              <div class="flex flex-wrap items-center gap-3 mb-4">
                <span class="px-2 py-1 text-[10px] font-bold uppercase tracking-widest rounded-sm bg-primary/10 text-primary">
                  {{ collection.linea_investigacion }}
                </span>
                <span class="px-2 py-1 text-[10px] font-bold uppercase tracking-widest rounded-sm bg-secondary/10 text-secondary">
                  {{ collection.sub_linea }}
                </span>
                <span class="text-text-muted text-xs flex items-center gap-1">
                  <span class="material-symbols-outlined text-sm">schedule</span>
                  {{ formatDate(collection.created_at) }}
                </span>
              </div>

              <div class="space-y-3">
                <article
                  v-for="item in collection.items"
                  :key="item.id"
                  class="border border-border-color bg-background-light px-4 py-4"
                >
                  <div class="flex items-start justify-between gap-4">
                    <div>
                      <h4 class="font-display font-bold text-[17px] text-text-main leading-snug">{{ item.t }}</h4>
                      <p class="mt-2 text-sm text-text-muted">
                        {{ item.v1 }} {{ item.c }} {{ item.v2 }} · {{ item.u }} · {{ item.s }}
                      </p>
                    </div>
                    <button class="p-2 text-text-muted hover:text-primary transition-colors" @click="copyItem(item)">
                      <span class="material-symbols-outlined">content_copy</span>
                    </button>
                  </div>
                </article>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button
                class="p-2.5 text-text-muted hover:text-primary transition-colors hover:bg-primary/5"
                title="Descargar"
                @click="downloadCollection(collection)"
              >
                <span class="material-symbols-outlined">download</span>
              </button>
              <button
                class="p-2.5 text-text-muted hover:text-red-500 transition-colors hover:bg-red-50"
                title="Eliminar"
                @click="removeCollection(collection.id)"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
          </div>
        </div>

        <div v-if="!filtered.length" class="flex flex-col items-center justify-center py-24 text-center border border-dashed border-border-color bg-background-light">
          <span class="material-symbols-outlined text-6xl text-border-color mb-4">bookmarks</span>
          <p class="font-display font-bold text-xl text-text-muted mb-2">Aun no tienes titulos guardados</p>
          <p class="text-text-muted text-sm max-w-md">
            Genera propuestas con IA, elige las que realmente quieras conservar y guardalas con tu cuenta.
          </p>
        </div>
      </div>
    </template>
  </div>

  <AuthDialog
    v-model="showAuthDialog"
    title="Accede a tu historial"
    description="Necesitas autenticarte para ver y conservar los titulos guardados en tu cuenta."
    @authenticated="handleAuthenticated"
  />
</template>
