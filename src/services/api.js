import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
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
    const { data } = await apiClient.post('/api/title-sessions', payload)
    return data
  } catch (error) {
    const message = error.response?.data?.detail || 'No se pudieron generar las propuestas'
    throw new Error(message)
  }
}
