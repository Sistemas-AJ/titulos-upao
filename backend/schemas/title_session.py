from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator
from sqlmodel import SQLModel

from backend.models.title_session import GrupoEmpresa, SessionStatus, TipoEmpresa


class TitleGenerationRequest(SQLModel):
    user_id: UUID | None = None
    linea_investigacion: str
    sub_linea: str
    nivel: str
    grupo_empresa: GrupoEmpresa
    cantidad_empresas: int | None = None
    confirmacion_data: bool
    tipo_empresa: TipoEmpresa
    nombre_empresa: str
    descripcion: str
    giro_negocio: str
    problematica: str

    @model_validator(mode="after")
    def validate_group_rules(self):
        if self.grupo_empresa == GrupoEmpresa.grupo and not self.cantidad_empresas:
            raise ValueError("cantidad_empresas es obligatoria cuando grupo_empresa es 'grupo'")
        if self.grupo_empresa == GrupoEmpresa.individual:
            self.cantidad_empresas = None
        return self


class TitleProposalRead(SQLModel):
    id: UUID
    titulo: str
    variable_1: str
    conector: str
    variable_2: str
    unidad_investigacion: str
    espacio: str
    tiempo: str


class TitleProposalFrontend(SQLModel):
    t: str
    v1: str
    c: str
    v2: str
    u: str
    s: str


class AIProposalSchema(SQLModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str
    variable_1: str
    conector: str
    variable_2: str
    unidad_investigacion: str
    espacio: str
    tiempo: str


class AIProposalPayload(SQLModel):
    model_config = ConfigDict(extra="forbid")

    proposals: list[AIProposalSchema] = Field(min_length=5, max_length=10)


class TitleSessionRead(SQLModel):
    id: UUID
    user_id: UUID | None
    linea_investigacion: str
    sub_linea: str
    nivel: str
    grupo_empresa: GrupoEmpresa
    cantidad_empresas: int | None
    confirmacion_data: bool
    tipo_empresa: TipoEmpresa
    nombre_empresa: str
    descripcion: str
    giro_negocio: str
    problematica: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
    proposals: list[TitleProposalRead] = []


class TitleGenerationResponse(SQLModel):
    session_id: UUID
    status: SessionStatus
    expires_at: datetime
    input_data: TitleSessionRead
    proposals: list[TitleProposalFrontend]


class RetryableErrorDetail(SQLModel):
    message: str
    retryable: bool = True
    reason: str
