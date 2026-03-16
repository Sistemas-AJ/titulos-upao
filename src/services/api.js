// Mock API Layer for UPAO Thesis Wizard

export const generateProposals = async (wizardState) => {
  // Simulate a realistic 3-second minimum processing delay from the AI
  await new Promise(resolve => setTimeout(resolve, 3000));

  // In the future: const response = await axios.post('/api/generate-titles', wizardState);
  // For now: Return the hardcoded array from paso 4.html
  
  return [
    { t: "La gestión financiera y su incidencia en la rentabilidad de las empresas del sector retail en Trujillo, periodo 2023", v1: "Gestión financiera", c: "Incidencia en", v2: "Rentabilidad", u: "Empresas del sector retail", s: "Trujillo, 2023" },
    { t: "Implementación de un sistema de control interno y la optimización de recursos en la Constructora del Norte S.A.C., 2024", v1: "Sistema de control interno", c: "Optimización de", v2: "Recursos", u: "Constructora del Norte S.A.C.", s: "2024" },
    { t: "Impacto de la facturación electrónica en la eficiencia operativa de las PYMES comerciales de Piura, 2023", v1: "Facturación electrónica", c: "Impacto en", v2: "Eficiencia operativa", u: "PYMES comerciales", s: "Piura, 2023" },
    { t: "Estrategias de planeamiento tributario para la reducción de contingencias fiscales en empresas manufactureras, 2023", v1: "Planeamiento tributario", c: "Reducción de", v2: "Contingencias fiscales", u: "Empresas manufactureras", s: "2023" },
    { t: "El flujo de caja y la toma de decisiones financieras en las estaciones de servicio de la región La Libertad, 2024", v1: "Flujo de caja", c: "Toma de decisiones", v2: "Financieras", u: "Estaciones de servicio", s: "La Libertad, 2024" },
    { t: "Análisis de la cultura tributaria y su relación con el cumplimiento de obligaciones en los comerciantes de Trujillo, 2023", v1: "Cultura tributaria", c: "Relación con", v2: "Cumplimiento de obligaciones", u: "Comerciantes", s: "Trujillo, 2023" },
    { t: "Gestión de inventarios y su influencia en el capital de trabajo de las ferreterías de la ciudad de Piura, periodo 2022-2023", v1: "Gestión de inventarios", c: "Influencia en", v2: "Capital de trabajo", u: "Ferreterías", s: "Piura, 2022-2023" },
    { t: "Auditoría de cumplimiento y la gestión administrativa en las municipalidades distritales de la provincia de Trujillo, 2024", v1: "Auditoría de cumplimiento", c: "Gestión", v2: "Administrativa", u: "Municipalidades distritales", s: "Provincia de Trujillo, 2024" },
    { t: "Transformación digital contable y la productividad del personal en los estudios contables de la zona centro de Piura, 2023", v1: "Transformación digital contable", c: "Productividad", v2: "Del personal", u: "Estudios contables", s: "Zona centro de Piura, 2023" },
    { t: "Costos de producción y la fijación de precios en las empresas agroindustriales exportadoras de Chavimochic, 2023", v1: "Costos de producción", c: "Fijación de", v2: "Precios", u: "Empresas agroindustriales", s: "Chavimochic, 2023" },
    { t: "La ética profesional del contador y la transparencia de la información financiera en el sector público, 2024", v1: "Ética profesional", c: "Transparencia de", v2: "Información financiera", u: "Sector público", s: "2024" },
    { t: "Evaluación del sistema de detracciones y su efecto en la liquidez de las empresas de servicios de transporte, 2023", v1: "Sistema de detracciones", c: "Efecto en", v2: "Liquidez", u: "Empresas de transporte", s: "2023" },
    { t: "Financiamiento bancario y el crecimiento económico de las microempresas del sector calzado en El Porvenir, 2023", v1: "Financiamiento bancario", c: "Crecimiento", v2: "Económico", u: "Microempresas de calzado", s: "El Porvenir, 2023" },
    { t: "Normas Internacionales de Información Financiera (NIIF) y su impacto en la presentación de estados financieros, 2023", v1: "NIIF", c: "Impacto en", v2: "Estados financieros", u: "Empresas corporativas", s: "2023" },
    { t: "Control presupuestario y la ejecución de gastos en las instituciones educativas privadas de la provincia de Piura, 2024", v1: "Control presupuestario", c: "Ejecución de", v2: "Gastos", u: "Instituciones educativas", s: "Provincia de Piura, 2024" },
    { t: "Incidencia de la gestión por procesos en la rentabilidad operativa de las empresas logísticas del Puerto de Paita, 2023", v1: "Gestión por procesos", c: "Incidencia en", v2: "Rentabilidad operativa", u: "Empresas logísticas", s: "Puerto de Paita, 2023" },
    { t: "Análisis del apalancamiento financiero y la sostenibilidad de las empresas textiles en Trujillo Metropolitano, 2024", v1: "Apalancamiento financiero", c: "Sostenibilidad", v2: "Empresarial", u: "Empresas textiles", s: "Trujillo, 2024" },
    { t: "Gestión de cuentas por cobrar y su repercusión en la solvencia de las clínicas privadas de la ciudad de Piura, 2023", v1: "Cuentas por cobrar", c: "Repercusión en", v2: "Solvencia", u: "Clínicas privadas", s: "Piura, 2023" },
    { t: "Modernización de la gestión pública y la eficiencia del gasto en el Gobierno Regional de La Libertad, periodo 2023", v1: "Modernización gestión pública", c: "Eficiencia del", v2: "Gasto", u: "Gobierno Regional", s: "La Libertad, 2023" },
    { t: "El outsourcing contable y la reducción de costos operativos en las medianas empresas de servicios en Piura, 2024", v1: "Outsourcing contable", c: "Reducción de", v2: "Costos operativos", u: "Medianas empresas", s: "Piura, 2024" }
  ];
}
