from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    full_name: str = Field(index=True, max_length=120)
    email: str = Field(index=True, unique=True, max_length=120)
    password_hash: str = Field(default="", nullable=False, max_length=255)
    is_active: bool = Field(default=True)
    last_login_at: datetime | None = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime = Field(default_factory=utc_now, nullable=False)
