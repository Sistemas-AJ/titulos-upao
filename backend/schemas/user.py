from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    full_name: str
    email: EmailStr


class UserRegister(SQLModel):
    full_name: str
    email: EmailStr
    password: str
    recaptcha_token: str | None = None


class UserRead(SQLModel):
    id: UUID
    full_name: str
    email: EmailStr
    is_active: bool
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class LoginRequest(SQLModel):
    email: EmailStr
    password: str
    recaptcha_token: str | None = None


class AuthToken(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
