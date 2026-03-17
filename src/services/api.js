import axios from 'axios'
import { AUTH_STORAGE_KEY } from '@/store/auth'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use((config) => {
  try {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      if (parsed?.token) {
        config.headers.Authorization = `Bearer ${parsed.token}`
      }
    }
  } catch {}
  return config
})

const extractError = (error, fallbackMessage) => {
  const detail = error.response?.data?.detail

  if (detail && typeof detail === 'object') {
    const enrichedError = new Error(detail.message || fallbackMessage)
    enrichedError.retryable = Boolean(detail.retryable)
    enrichedError.reason = detail.reason || 'unknown'
    enrichedError.retryAfterSeconds = detail.retry_after_seconds || 0
    throw enrichedError
  }

  throw new Error(detail || fallbackMessage)
}

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
    const { data } = await apiClient.post('/api/title-sessions', payload)
    return data
  } catch (error) {
    extractError(error, 'No se pudieron generar las propuestas')
  }
}

export const getResearchCatalog = async () => {
  try {
    const { data } = await apiClient.get('/api/reference-titles/catalog')
    return data
  } catch {
    return []
  }
}

export const registerUser = async (payload) => {
  try {
    const { data } = await apiClient.post('/api/users/register', payload)
    return data
  } catch (error) {
    extractError(error, 'No se pudo crear la cuenta')
  }
}

export const loginUser = async (payload) => {
  try {
    const { data } = await apiClient.post('/api/users/login', payload)
    return data
  } catch (error) {
    extractError(error, 'No se pudo iniciar sesion')
  }
}

export const saveTitles = async (payload) => {
  try {
    const { data } = await apiClient.post('/api/saved-titles', payload)
    return data
  } catch (error) {
    extractError(error, 'No se pudo guardar la seleccion')
  }
}

export const listSavedTitles = async () => {
  try {
    const { data } = await apiClient.get('/api/saved-titles')
    return data
  } catch (error) {
    extractError(error, 'No se pudo cargar el historial')
  }
}

export const deleteSavedTitle = async (savedTitleId) => {
  try {
    await apiClient.delete(`/api/saved-titles/${savedTitleId}`)
  } catch (error) {
    extractError(error, 'No se pudo eliminar el titulo guardado')
  }
}
