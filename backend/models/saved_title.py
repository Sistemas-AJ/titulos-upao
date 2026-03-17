from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SavedTitleCollection(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    source_session_id: Optional[UUID] = Field(default=None, index=True)
    linea_investigacion: str = Field(max_length=120, index=True)
    sub_linea: str = Field(max_length=120, index=True)
    created_at: datetime = Field(default_factory=utc_now, nullable=False, index=True)

    items: list["SavedTitleItem"] = Relationship(back_populates="collection")


class SavedTitleItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    collection_id: UUID = Field(foreign_key="savedtitlecollection.id", index=True)
    titulo: str = Field(max_length=500)
    variable_1: str = Field(max_length=180)
    conector: str = Field(max_length=120)
    variable_2: str = Field(max_length=180)
    unidad_investigacion: str = Field(max_length=220)
    espacio: str = Field(max_length=180)
    tiempo: str = Field(max_length=120)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)

    collection: SavedTitleCollection = Relationship(back_populates="items")
