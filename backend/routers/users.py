from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.database.session import get_session
from backend.models.user import User
from backend.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User).order_by(User.created_at.desc())).all()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == payload.email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con este correo")

    user = User(full_name=payload.full_name, email=str(payload.email))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, payload: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = payload.model_dump(exclude_unset=True)
    if "email" in data:
        existing_user = session.exec(
            select(User).where(User.email == str(data["email"]), User.id != user_id)
        ).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Ya existe un usuario con este correo")
        data["email"] = str(data["email"])

    for key, value in data.items():
        setattr(user, key, value)

    user.updated_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

