from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    full_name: str
    email: EmailStr


class UserRead(SQLModel):
    id: UUID
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None

