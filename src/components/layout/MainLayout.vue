<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { RouterView } from 'vue-router'
import Sidebar from './Sidebar.vue'
import MainHeader from './MainHeader.vue'
import { useWizardStore } from '@/store/wizard'

const store = useWizardStore()
const route = useRoute()
const isSidebarOpen = ref(false)

const handleBeforeUnload = (e) => {
  if (store.hasProgress) {
    e.preventDefault()
    e.returnValue = '' // Required for the browser to show the dialog
  }
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

onMounted(() => window.addEventListener('beforeunload', handleBeforeUnload))
onBeforeUnmount(() => window.removeEventListener('beforeunload', handleBeforeUnload))

watch(() => route.fullPath, closeSidebar)
</script>

<template>
  <div class="flex h-full w-full overflow-hidden">
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 z-30 bg-slate-950/45 lg:hidden"
      @click="closeSidebar"
    ></div>

    <Sidebar
      :is-open="isSidebarOpen"
      @close="closeSidebar"
    />
    
    <main class="flex-1 overflow-y-auto bg-background-light flex flex-col">
      <MainHeader
        :is-sidebar-open="isSidebarOpen"
        @toggle-sidebar="toggleSidebar"
      />
      <RouterView />
    </main>
  </div>
</template>
