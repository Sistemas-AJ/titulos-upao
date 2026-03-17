import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const generateProposals = async (wizardState) => {
  const payload = {
    linea_investigacion: wizardState.step1.domain,
    sub_linea: wizardState.step1.subline,
    nivel: wizardState.step2.level,
    grupo_empresa: wizardState.step3.scopeType === 'group' ? 'grupo' : 'individual',
    cantidad_empresas: wizardState.step3.scopeType === 'group' ? wizardState.step3.count : null,
    confirmacion_data: wizardState.step3.accessConfirmed,
    tipo_empresa: wizardState.step3.companyType,
    nombre_empresa: wizardState.step3.name,
    descripcion: wizardState.step3.description,
    giro_negocio: wizardState.step3.sector === 'otro'
      ? wizardState.step3.customSector
      : wizardState.step3.sector,
    problematica: wizardState.step3.problem
  }

  try {
    const { data } = await apiClient.post('/title-sessions', payload)
    return data
  } catch (error) {
    const detail = error.response?.data?.detail

    if (detail && typeof detail === 'object') {
      const retryError = new Error(detail.message || 'No se pudieron generar las propuestas')
      retryError.retryable = Boolean(detail.retryable)
      retryError.reason = detail.reason || 'unknown'
      throw retryError
    }

    const fallbackError = new Error(detail || 'No se pudieron generar las propuestas')
    fallbackError.retryable = false
    fallbackError.reason = 'unknown'
    throw fallbackError
  }
}

export const getResearchCatalog = async () => {
  try {
    const { data } = await apiClient.get('/reference-titles/catalog')
    return data
  } catch {
    return []
  }
}

export const getReferenceTitlesPaged = async ({ page = 1, linea_investigacion = null, q = null } = {}) => {
  try {
    const params = { page }
    if (linea_investigacion) {
      params.linea_investigacion = linea_investigacion
    }
    if (q && q.trim() !== '') {
      params.q = q.trim()
    }
    const { data } = await apiClient.get('/reference-titles/paged', { params })
    return data
  } catch (error) {
    console.error('Failed to fetch reference titles:', error)
    return { items: [], total: 0, page: 1, size: 10, pages: 1 }
  }
}
