from sqlalchemy import func
from sqlmodel import Session, select

from backend.models.reference_title import ReferenceTitle


def get_reference_examples(
    session: Session,
    linea_investigacion: str,
    sub_linea: str,
    nivel_investigacion: str,
    limit: int = 10,
) -> list[str]:
    normalized_nivel = nivel_investigacion.strip().lower()

    examples = session.exec(
        select(ReferenceTitle.titulo_investigacion)
        .where(
            ReferenceTitle.linea_investigacion == linea_investigacion,
            ReferenceTitle.sub_linea == sub_linea,
            func.lower(ReferenceTitle.nivel_investigacion) == normalized_nivel,
        )
        .order_by(ReferenceTitle.created_at.desc())
        .limit(limit)
    ).all()
    return list(examples)
