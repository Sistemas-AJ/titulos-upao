import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import LineaInvestigacion from '@/views/LineaInvestigacion.vue'
import NivelInvestigacion from '@/views/NivelInvestigacion.vue'
import AlcanceEmpresarial from '@/views/AlcanceEmpresarial.vue'
import PropuestasTitulos from '@/views/PropuestasTitulos.vue'
import HistorialConsultas from '@/views/HistorialConsultas.vue'
import BaseDatosTesis from '@/views/BaseDatosTesis.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      redirect: '/paso-1',
      children: [
        {
          path: 'paso-1',
          name: 'Paso1',
          component: LineaInvestigacion
        },
        {
          path: 'paso-2',
          name: 'Paso2',
          component: NivelInvestigacion
        },
        {
          path: 'paso-3',
          name: 'Paso3',
          component: AlcanceEmpresarial
        },
        {
          path: 'paso-4',
          name: 'Paso4',
          component: PropuestasTitulos
        },
        {
          path: 'herramientas/base-datos',
          name: 'BaseDatos',
          component: BaseDatosTesis
        }
      ]
    }
  ]
})

export default router
