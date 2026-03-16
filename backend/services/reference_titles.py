from sqlmodel import Session, select

from backend.models.reference_title import ReferenceTitle


def get_reference_examples(
    session: Session,
    linea_investigacion: str,
    sub_linea: str,
    limit: int = 5,
) -> list[str]:
    examples = session.exec(
        select(ReferenceTitle.titulo_investigacion)
        .where(
            ReferenceTitle.linea_investigacion == linea_investigacion,
            ReferenceTitle.sub_linea == sub_linea,
        )
        .order_by(ReferenceTitle.created_at.desc())
        .limit(limit)
    ).all()
    return list(examples)
