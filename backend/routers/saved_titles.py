from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, delete, select

from backend.database.session import get_session
from backend.dependencies.auth import get_current_user
from backend.models.saved_title import SavedTitleCollection, SavedTitleItem
from backend.models.user import User
from backend.schemas.saved_title import SavedTitleCreate, SavedTitleProposalRead, SavedTitleRead


router = APIRouter(prefix="/api/saved-titles", tags=["saved-titles"])


def _combine_spatial_temporal(espacio: str, tiempo: str) -> str:
    if espacio and tiempo:
        return f"{espacio}, {tiempo}"
    return espacio or tiempo


def to_saved_title_read(collection: SavedTitleCollection) -> SavedTitleRead:
    return SavedTitleRead(
        id=collection.id,
        user_id=collection.user_id,
        session_id=collection.source_session_id,
        linea_investigacion=collection.linea_investigacion,
        sub_linea=collection.sub_linea,
        created_at=collection.created_at,
        items=[
            SavedTitleProposalRead(
                id=item.id,
                t=item.titulo,
                v1=item.variable_1,
                c=item.conector,
                v2=item.variable_2,
                u=item.unidad_investigacion,
                s=_combine_spatial_temporal(item.espacio, item.tiempo),
            )
            for item in collection.items
        ],
    )


@router.get("", response_model=list[SavedTitleRead])
def list_saved_titles(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    collections = session.exec(
        select(SavedTitleCollection)
        .where(SavedTitleCollection.user_id == current_user.id)
        .order_by(SavedTitleCollection.created_at.desc())
    ).all()
    return [to_saved_title_read(item) for item in collections]


@router.post("", response_model=SavedTitleRead, status_code=status.HTTP_201_CREATED)
def create_saved_title(
    payload: SavedTitleCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Debes seleccionar al menos un titulo")

    collection = SavedTitleCollection(
        user_id=current_user.id,
        source_session_id=payload.session_id,
        linea_investigacion=payload.linea_investigacion,
        sub_linea=payload.sub_linea,
    )
    session.add(collection)
    session.flush()

    for item in payload.items:
        espacio, tiempo = _split_spatial_temporal(item.s)
        session.add(
            SavedTitleItem(
                collection_id=collection.id,
                titulo=item.t,
                variable_1=item.v1,
                conector=item.c,
                variable_2=item.v2,
                unidad_investigacion=item.u,
                espacio=espacio,
                tiempo=tiempo,
            )
        )

    session.commit()
    session.refresh(collection)
    return to_saved_title_read(collection)


def _split_spatial_temporal(value: str) -> tuple[str, str]:
    raw = (value or "").strip()
    if not raw:
        return "", ""
    last_comma_index = raw.rfind(",")
    if last_comma_index == -1:
        return raw, ""
    return raw[:last_comma_index].strip(), raw[last_comma_index + 1 :].strip()


@router.delete("/{saved_title_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_title(
    saved_title_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    collection = session.get(SavedTitleCollection, saved_title_id)
    if not collection or collection.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    session.exec(delete(SavedTitleItem).where(SavedTitleItem.collection_id == collection.id))
    session.delete(collection)
    session.commit()
