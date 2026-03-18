import unicodedata
from datetime import datetime
from uuid import UUID

from pydantic import field_validator
from sqlmodel import SQLModel


def normalize_reference_line(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.split())


class ReferenceTitleCreate(SQLModel):
    titulo_investigacion: str
    linea_investigacion: str
    sub_linea: str
    authors: str = ""
    status: str = "APROVADO"
    anio: int
    nivel_investigacion: str

    @field_validator("linea_investigacion", mode="before")
    @classmethod
    def normalize_linea_investigacion(cls, value: str) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return normalize_reference_line(value)



class ReferenceTitleRead(SQLModel):
    id: UUID
    titulo_investigacion: str
    linea_investigacion: str
    sub_linea: str
    created_at: datetime
    authors: str
    status: str
    anio: int
    nivel_investigacion: str


class ReferenceTitleListItem(SQLModel):
    titulo_investigacion: str
    linea_investigacion: str
    sub_linea: str
    authors: str
    status: str
    anio: int
    nivel_investigacion: str


class ReferenceTitlePage(SQLModel):
    items: list[ReferenceTitleListItem]
    page: int
    page_size: int
    total: int
    total_pages: int


class ReferenceTitleImportResponse(SQLModel):
    created: list[ReferenceTitleRead]
    updated: list[ReferenceTitleRead]
    total_received: int


class ResearchSublineCatalogItem(SQLModel):
    value: str
    title: str


class ResearchLineCatalogItem(SQLModel):
    value: str
    title: str
    description: str | None = None
    sublines: list[ResearchSublineCatalogItem]
