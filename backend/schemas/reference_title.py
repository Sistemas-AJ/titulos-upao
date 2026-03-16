from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class ReferenceTitleCreate(SQLModel):
    titulo_investigacion: str
    linea_investigacion: str
    sub_linea: str


class ReferenceTitleRead(SQLModel):
    id: UUID
    titulo_investigacion: str
    linea_investigacion: str
    sub_linea: str
    created_at: datetime


class ReferenceTitleImportResponse(SQLModel):
    created: list[ReferenceTitleRead]
    duplicates: list[ReferenceTitleRead]
    total_received: int


class ResearchSublineCatalogItem(SQLModel):
    value: str
    title: str


class ResearchLineCatalogItem(SQLModel):
    value: str
    title: str
    description: str | None = None
    sublines: list[ResearchSublineCatalogItem]
