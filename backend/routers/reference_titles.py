import pandas as pd
import io
from fastapi.responses import StreamingResponse
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import or_
from sqlmodel import Session, select


from backend.database.session import get_session
from backend.models.reference_title import ReferenceTitle
from backend.schemas.reference_title import (
    ReferenceTitleCreate,
    ReferenceTitleImportResponse,
    ReferenceTitleListItem,
    ReferenceTitlePage,
    ReferenceTitleRead,
    ResearchLineCatalogItem,
    ResearchSublineCatalogItem,
    normalize_reference_line,
)
from backend.services.reference_title_importer import parse_reference_titles_excel


router = APIRouter(prefix="/api/reference-titles", tags=["reference-titles"])
PAGE_SIZE = 20


def prettify_catalog_label(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").strip().title()


def to_reference_title_read(item: ReferenceTitle) -> ReferenceTitleRead:
    return ReferenceTitleRead(
        id=item.id,
        titulo_investigacion=item.titulo_investigacion,
        linea_investigacion=item.linea_investigacion,
        sub_linea=item.sub_linea,
        created_at=item.created_at,
        authors=item.authors,
        status=item.status,
        anio=item.anio,
        nivel_investigacion=item.nivel_investigacion,
    )


def to_reference_title_list_item(item: ReferenceTitle) -> ReferenceTitleListItem:
    return ReferenceTitleListItem(
        titulo_investigacion=item.titulo_investigacion,
        linea_investigacion=item.linea_investigacion,
        sub_linea=item.sub_linea,
        authors=item.authors,
        status=item.status,
        anio=item.anio,
        nivel_investigacion=item.nivel_investigacion,
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
    updated: list[ReferenceTitle] = []

    for item in items:
        existing = session.exec(
            select(ReferenceTitle).where(
                ReferenceTitle.titulo_investigacion == item.titulo_investigacion,
                ReferenceTitle.linea_investigacion == item.linea_investigacion,
                ReferenceTitle.sub_linea == item.sub_linea
            )
        ).first()

        if existing:
            existing.anio = item.anio
            existing.nivel_investigacion = item.nivel_investigacion
            session.add(existing)
            session.flush()
            updated.append(existing)
            continue

        reference_title = ReferenceTitle(**item.model_dump())
        session.add(reference_title)
        session.flush()
        created.append(reference_title)

    session.commit()

    return ReferenceTitleImportResponse(
        created=[to_reference_title_read(item) for item in created],
        updated=[to_reference_title_read(item) for item in updated],
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


@router.get("/paged", response_model=ReferenceTitlePage)
def list_reference_titles_paged(
    linea_investigacion: str | None = Query(default=None),
    q: str | None = Query(default=None),
    anio: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    session: Session = Depends(get_session),
):
    statement = select(ReferenceTitle)
    if linea_investigacion:
        statement = statement.where(
            ReferenceTitle.linea_investigacion == normalize_reference_line(linea_investigacion)
        )
    if q and q.strip():
        search_term = f"%{q.strip()}%"
        statement = statement.where(
            or_(
                ReferenceTitle.titulo_investigacion.ilike(search_term),
                ReferenceTitle.sub_linea.ilike(search_term),
                ReferenceTitle.authors.ilike(search_term),
                ReferenceTitle.status.ilike(search_term),
            )
        )
    if anio is not None:
        statement = statement.where(ReferenceTitle.anio == anio)

    total = len(session.exec(statement).all())
    offset = (page - 1) * PAGE_SIZE
    items = session.exec(
        statement
        .order_by(
            ReferenceTitle.anio.desc(),
            ReferenceTitle.created_at.desc(),
            ReferenceTitle.titulo_investigacion.asc(),
        )
        .offset(offset)
        .limit(PAGE_SIZE)
    ).all()

    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total else 0

    return ReferenceTitlePage(
        items=[to_reference_title_list_item(item) for item in items],
        page=page,
        page_size=PAGE_SIZE,
        total=total,
        total_pages=total_pages,
    )


@router.get("/catalog", response_model=list[ResearchLineCatalogItem])
def get_reference_catalog(session: Session = Depends(get_session)):
    items = session.exec(
        select(ReferenceTitle).order_by(
            ReferenceTitle.linea_investigacion.asc(),
            ReferenceTitle.sub_linea.asc(),
        )
    ).all()

    catalog: dict[str, dict] = {}
    for item in items:
        line_key = item.linea_investigacion
        subline_key = item.sub_linea

        if line_key not in catalog:
            catalog[line_key] = {
                "value": line_key,
                "title": prettify_catalog_label(line_key),
                "description": None,
                "sublines": {},
            }

        if subline_key not in catalog[line_key]["sublines"]:
            catalog[line_key]["sublines"][subline_key] = ResearchSublineCatalogItem(
                value=subline_key,
                title=prettify_catalog_label(subline_key),
            )

    return [
        ResearchLineCatalogItem(
            value=line_data["value"],
            title=line_data["title"],
            description=line_data["description"],
            sublines=list(line_data["sublines"].values()),
        )
        for line_data in catalog.values()
    ]

@router.get("/export-excel")
def export_excel_titles(
    linea_investigacion: str | None = Query(default=None),
    q: str | None = Query(default=None),
    anio: int | None = Query(default=None),
    session: Session = Depends(get_session),
):
    # 1. Reutilizamos tu lógica de filtrado (sin paginación)
    statement = select(ReferenceTitle)
    
    if linea_investigacion:
        statement = statement.where(
            ReferenceTitle.linea_investigacion == normalize_reference_line(linea_investigacion)
        )
    if q and q.strip():
        search_term = f"%{q.strip()}%"
        statement = statement.where(
            or_(
                ReferenceTitle.titulo_investigacion.ilike(search_term),
                ReferenceTitle.sub_linea.ilike(search_term),
                ReferenceTitle.authors.ilike(search_term),
                ReferenceTitle.status.ilike(search_term),
            )
        )
    if anio is not None:
        statement = statement.where(ReferenceTitle.anio == anio)

    # 2. Ejecutar la consulta completa (sin offset ni limit)
    items = session.exec(
        statement.order_by(ReferenceTitle.anio.desc(), ReferenceTitle.created_at.desc())
    ).all()

    # 3. Convertir a una lista de diccionarios para Pandas
    # Aquí puedes personalizar los nombres de las columnas que verá el usuario
    data = [
        {
            "Título de Investigación": item.titulo_investigacion,
            "Autores": item.authors,
            "Año": item.anio,
            "Nivel": item.nivel_investigacion,
            "Línea": item.linea_investigacion,
            "Sub Línea": item.sub_linea,
            "Estado": item.status,
        }
        for item in items
    ]

    # 4. Crear el Excel en memoria usando un buffer
    df = pd.DataFrame(data)
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Títulos de Investigación')
        
    output.seek(0)

    # 5. Retornar el archivo para descarga directa
    filename = f"reporte_titulos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )