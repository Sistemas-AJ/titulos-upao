from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def default_expiration() -> datetime:
    return utc_now() + timedelta(hours=24)


class GrupoEmpresa(str, Enum):
    individual = "individual"
    grupo = "grupo"


class TipoEmpresa(str, Enum):
    publica = "publica"
    privada = "privada"


class SessionStatus(str, Enum):
    draft = "draft"
    completed = "completed"
    failed = "failed"


class TitleSession(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", index=True)
    linea_investigacion: str = Field(max_length=120, index=True)
    sub_linea: str = Field(max_length=120, index=True)
    nivel: str = Field(max_length=80, index=True)
    grupo_empresa: GrupoEmpresa = Field(index=True)
    cantidad_empresas: Optional[int] = Field(default=None, ge=1)
    confirmacion_data: bool = Field(default=False)
    tipo_empresa: TipoEmpresa = Field(index=True)
    nombre_empresa: str = Field(max_length=180)
    descripcion: str = Field(max_length=3000)
    giro_negocio: str = Field(max_length=180)
    problematica: str = Field(max_length=4000)
    status: SessionStatus = Field(default=SessionStatus.draft, index=True)
    ai_raw_response: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True),
    )
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)
    expires_at: datetime = Field(default_factory=default_expiration, nullable=False, index=True)

    proposals: list["TitleProposal"] = Relationship(back_populates="session")


class TitleProposal(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    session_id: UUID = Field(foreign_key="titlesession.id", index=True)
    titulo: str = Field(max_length=500)
    variable_1: str = Field(max_length=180)
    conector: str = Field(max_length=120)
    variable_2: str = Field(max_length=180)
    unidad_investigacion: str = Field(max_length=220)
    espacio: str = Field(max_length=180)
    tiempo: str = Field(max_length=120)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)

    session: TitleSession = Relationship(back_populates="proposals")

