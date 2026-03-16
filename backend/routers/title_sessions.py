from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, delete, select

from backend.config import get_settings
from backend.database.session import get_session
from backend.models.title_session import SessionStatus, TitleProposal, TitleSession
from backend.models.user import User
from backend.schemas.title_session import (
    RetryableErrorDetail,
    TitleGenerationRequest,
    TitleGenerationResponse,
    TitleProposalFrontend,
    TitleProposalRead,
    TitleSessionRead,
)
from backend.services.ai import generate_title_proposals
from backend.services.reference_titles import get_reference_examples


router = APIRouter(prefix="/api/title-sessions", tags=["title-sessions"])


def to_title_session_read(db_session: TitleSession) -> TitleSessionRead:
    return TitleSessionRead(
        id=db_session.id,
        user_id=db_session.user_id,
        linea_investigacion=db_session.linea_investigacion,
        sub_linea=db_session.sub_linea,
        nivel=db_session.nivel,
        grupo_empresa=db_session.grupo_empresa,
        cantidad_empresas=db_session.cantidad_empresas,
        confirmacion_data=db_session.confirmacion_data,
        tipo_empresa=db_session.tipo_empresa,
        nombre_empresa=db_session.nombre_empresa,
        descripcion=db_session.descripcion,
        giro_negocio=db_session.giro_negocio,
        problematica=db_session.problematica,
        status=db_session.status,
        created_at=db_session.created_at,
        updated_at=db_session.updated_at,
        expires_at=db_session.expires_at,
        proposals=[
            TitleProposalRead(
                id=proposal.id,
                titulo=proposal.titulo,
                variable_1=proposal.variable_1,
                conector=proposal.conector,
                variable_2=proposal.variable_2,
                unidad_investigacion=proposal.unidad_investigacion,
                espacio=proposal.espacio,
                tiempo=proposal.tiempo,
            )
            for proposal in db_session.proposals
        ],
    )


def to_frontend_proposals(proposals: list[TitleProposal]) -> list[TitleProposalFrontend]:
    return [
        TitleProposalFrontend(
            t=proposal.titulo,
            v1=proposal.variable_1,
            c=proposal.conector,
            v2=proposal.variable_2,
            u=proposal.unidad_investigacion,
            s=f"{proposal.espacio}, {proposal.tiempo}".strip(", "),
        )
        for proposal in proposals
    ]


@router.post("", response_model=TitleGenerationResponse, status_code=status.HTTP_201_CREATED)
def create_title_session(
    payload: TitleGenerationRequest,
    session: Session = Depends(get_session),
):
    if payload.user_id and not session.get(User, payload.user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reference_titles = get_reference_examples(
        session,
        linea_investigacion=payload.linea_investigacion,
        sub_linea=payload.sub_linea,
    )

    try:
        ai_result = generate_title_proposals(payload, reference_titles=reference_titles)
        proposals_payload = ai_result["response"]["proposals"]
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=RetryableErrorDetail(
                message="La IA no devolvio un formato valido. Intenta nuevamente.",
                reason="invalid_ai_response",
            ).model_dump(),
        ) from exc

    settings = get_settings()
    db_session = TitleSession(
        **payload.model_dump(),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=settings.session_ttl_hours),
    )
    session.add(db_session)
    session.flush()

    for proposal in proposals_payload:
        session.add(
            TitleProposal(
                session_id=db_session.id,
                titulo=proposal["titulo"],
                variable_1=proposal["variable_1"],
                conector=proposal["conector"],
                variable_2=proposal["variable_2"],
                unidad_investigacion=proposal["unidad_investigacion"],
                espacio=proposal["espacio"],
                tiempo=proposal["tiempo"],
            )
        )

    db_session.ai_raw_response = ai_result
    db_session.status = SessionStatus.completed
    db_session.updated_at = datetime.now(timezone.utc)
    session.add(db_session)
    session.commit()
    session.refresh(db_session)

    return TitleGenerationResponse(
        session_id=db_session.id,
        status=db_session.status,
        expires_at=db_session.expires_at,
        input_data=to_title_session_read(db_session),
        proposals=to_frontend_proposals(db_session.proposals),
    )


@router.get("/{session_id}", response_model=TitleSessionRead)
def get_title_session(session_id: UUID, session: Session = Depends(get_session)):
    db_session = session.exec(
        select(TitleSession).where(TitleSession.id == session_id)
    ).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    return to_title_session_read(db_session)


@router.get("/{session_id}/proposals", response_model=list[TitleProposalFrontend])
def get_title_session_proposals(session_id: UUID, session: Session = Depends(get_session)):
    db_session = session.exec(
        select(TitleSession).where(TitleSession.id == session_id)
    ).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Sesion no encontrada")
    return to_frontend_proposals(db_session.proposals)


@router.delete("/expired", status_code=status.HTTP_204_NO_CONTENT)
def delete_expired_sessions(session: Session = Depends(get_session)):
    now = datetime.now(timezone.utc)
    expired_sessions = session.exec(
        select(TitleSession).where(TitleSession.expires_at < now)
    ).all()
    for expired_session in expired_sessions:
        session.exec(delete(TitleProposal).where(TitleProposal.session_id == expired_session.id))
        session.delete(expired_session)
    session.commit()
