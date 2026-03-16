<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from './Sidebar.vue'
import MainHeader from './MainHeader.vue'
import { useWizardStore } from '@/store/wizard'

const store = useWizardStore()

const handleBeforeUnload = (e) => {
  if (store.hasProgress) {
    e.preventDefault()
    e.returnValue = '' // Required for the browser to show the dialog
  }
}

onMounted(() => window.addEventListener('beforeunload', handleBeforeUnload))
onBeforeUnmount(() => window.removeEventListener('beforeunload', handleBeforeUnload))
</script>

<template>
  <div class="flex h-full w-full overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 overflow-y-auto bg-background-light flex flex-col">
      <MainHeader />
      <RouterView />
    </main>
  </div>
</template>
