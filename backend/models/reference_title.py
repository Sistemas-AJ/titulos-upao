from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ReferenceTitle(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "titulo_investigacion",
            "linea_investigacion",
            "sub_linea",
            name="uq_reference_title_triplet",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    titulo_investigacion: str = Field(max_length=500, index=True)
    linea_investigacion: str = Field(max_length=120, index=True)
    sub_linea: str = Field(max_length=120, index=True)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    authors: str = Field(default="", max_length=255)
    status: str = Field(default="APROVADO", max_length=50, nullable=False)
    anio: int 
    nivel_investigacion: str = Field(max_length=100)

