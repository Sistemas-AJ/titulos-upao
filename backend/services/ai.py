import json

from openai import OpenAI

from backend.config import get_settings
from backend.schemas.title_session import AIProposalPayload, TitleGenerationRequest


SYSTEM_PROMPT = """
Eres un asesor metodologico de tesis en contabilidad de UPAO.
Responde solo JSON valido con esta estructura exacta:
{
  "proposals": [
    {
      "titulo": "string",
      "variable_1": "string",
      "conector": "string",
      "variable_2": "string",
      "unidad_investigacion": "string",
      "espacio": "string",
      "tiempo": "string"
    }
  ]
}
Genera exactamente 10 propuestas.
No agregues markdown ni explicaciones.
""".strip()


def build_user_prompt(payload: TitleGenerationRequest, reference_titles: list[str] | None = None) -> str:
    example_block = ""
    if reference_titles:
        formatted_examples = "\n".join(f"- {title}" for title in reference_titles)
        example_block = f"""

Titulos de referencia registrados para esta linea y sublinea:
{formatted_examples}

Usalos solo como referencia de estilo, estructura y enfoque. No los copies literalmente.
""".rstrip()

    return f"""
Genera titulos de investigacion contable con estos datos:
- linea_investigacion: {payload.linea_investigacion}
- sub_linea: {payload.sub_linea}
- nivel: {payload.nivel}
- grupo_empresa: {payload.grupo_empresa.value}
- cantidad_empresas: {payload.cantidad_empresas}
- confirmacion_data: {payload.confirmacion_data}
- tipo_empresa: {payload.tipo_empresa.value}
- nombre_empresa: {payload.nombre_empresa}
- descripcion: {payload.descripcion}
- giro_negocio: {payload.giro_negocio}
- problematica: {payload.problematica}

Condiciones:
- Titulos realistas para tesis de contabilidad.
- Mantener coherencia metodologica con el nivel de investigacion.
- El campo tiempo debe ser un anio o periodo concreto.
- El campo espacio debe ser una ubicacion o ambito delimitado.
{example_block}
""".strip()


def generate_title_proposals(
    payload: TitleGenerationRequest,
    reference_titles: list[str] | None = None,
) -> dict:
    settings = get_settings()
    client = OpenAI(api_key=settings.api_open_ia)
    model_name = settings.model_ia.replace(" ", "-")
    reference_count = len(reference_titles or [])

    print(
        "[AI] generate_title_proposals",
        f"linea={payload.linea_investigacion}",
        f"sub_linea={payload.sub_linea}",
        f"reference_titles={reference_count}",
    )

    response = client.responses.create(

        model=model_name,
        timeout=60,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(payload, reference_titles)},
        ],
    )

    raw_output = response.output_text
    parsed_output = json.loads(raw_output)
    validated_output = AIProposalPayload.model_validate(parsed_output)
    return {
        "request": payload.model_dump(mode="json"),
        "response": validated_output.model_dump(mode="json"),
        "response_id": response.id,
        "model": model_name,
        "raw_output": raw_output,
        "reference_titles": reference_titles or [],
    }
