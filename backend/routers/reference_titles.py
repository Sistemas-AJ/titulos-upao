from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlmodel import Session, select

from backend.database.session import get_session
from backend.models.reference_title import ReferenceTitle
from backend.schemas.reference_title import (
    ReferenceTitleCreate,
    ReferenceTitleImportResponse,
    ReferenceTitleRead,
)
from backend.services.reference_title_importer import parse_reference_titles_excel


router = APIRouter(prefix="/api/reference-titles", tags=["reference-titles"])


def to_reference_title_read(item: ReferenceTitle) -> ReferenceTitleRead:
    return ReferenceTitleRead(
        id=item.id,
        titulo_investigacion=item.titulo_investigacion,
        linea_investigacion=item.linea_investigacion,
        sub_linea=item.sub_linea,
        created_at=item.created_at,
    )


@router.post("/import", response_model=ReferenceTitleImportResponse, status_code=status.HTTP_201_CREATED)
async def import_reference_titles(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Debes enviar un archivo Excel")

    if not file.filename.lower().endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos Excel .xlsx/.xlsm")

    try:
        items = parse_reference_titles_excel(await file.read())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="No se pudo procesar el archivo Excel") from exc

    created: list[ReferenceTitle] = []
    duplicates: list[ReferenceTitle] = []

    for item in items:
        existing = session.exec(
            select(ReferenceTitle).where(
                ReferenceTitle.titulo_investigacion == item.titulo_investigacion,
                ReferenceTitle.linea_investigacion == item.linea_investigacion,
                ReferenceTitle.sub_linea == item.sub_linea,
            )
        ).first()

        if existing:
            duplicates.append(existing)
            continue

        reference_title = ReferenceTitle(**item.model_dump())
        session.add(reference_title)
        session.flush()
        created.append(reference_title)

    session.commit()

    return ReferenceTitleImportResponse(
        created=[to_reference_title_read(item) for item in created],
        duplicates=[to_reference_title_read(item) for item in duplicates],
        total_received=len(items),
    )


@router.post("", response_model=ReferenceTitleRead, status_code=status.HTTP_201_CREATED)
def create_reference_title(
    payload: ReferenceTitleCreate,
    session: Session = Depends(get_session),
):
    reference_title = ReferenceTitle(**payload.model_dump())
    session.add(reference_title)
    session.commit()
    session.refresh(reference_title)
    return to_reference_title_read(reference_title)


@router.get("", response_model=list[ReferenceTitleRead])
def list_reference_titles(
    linea_investigacion: str | None = Query(default=None),
    sub_linea: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    statement = select(ReferenceTitle)
    if linea_investigacion:
        statement = statement.where(ReferenceTitle.linea_investigacion == linea_investigacion)
    if sub_linea:
        statement = statement.where(ReferenceTitle.sub_linea == sub_linea)

    items = session.exec(statement.order_by(ReferenceTitle.created_at.desc()).limit(limit)).all()
    return [to_reference_title_read(item) for item in items]
