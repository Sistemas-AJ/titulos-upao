from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class SavedTitleProposalCreate(SQLModel):
    t: str
    v1: str
    c: str
    v2: str
    u: str
    s: str


class SavedTitleCreate(SQLModel):
    session_id: UUID | None = None
    linea_investigacion: str
    sub_linea: str
    items: list[SavedTitleProposalCreate]


class SavedTitleProposalRead(SQLModel):
    id: UUID
    t: str
    v1: str
    c: str
    v2: str
    u: str
    s: str


class SavedTitleRead(SQLModel):
    id: UUID
    user_id: UUID
    session_id: UUID | None
    linea_investigacion: str
    sub_linea: str
    created_at: datetime
    items: list[SavedTitleProposalRead]
