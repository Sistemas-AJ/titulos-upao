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

  const response = await fetch('http://localhost:8000/api/title-sessions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })

  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({}))
    throw new Error(errorPayload.detail || 'No se pudieron generar las propuestas')
  }

  const data = await response.json()
  return data.proposals
}
