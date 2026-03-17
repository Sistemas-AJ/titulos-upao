from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlmodel import Session, select

from backend.config import get_settings
from backend.database.session import get_session
from backend.dependencies.auth import get_current_user
from backend.models.user import User
from backend.schemas.user import AuthToken, LoginRequest, UserCreate, UserRead, UserRegister, UserUpdate
from backend.services.auth import create_access_token, hash_password, verify_password
from backend.services.login_rate_limit import login_rate_limiter
from backend.services.recaptcha import verify_recaptcha_token


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(current_user: User = Depends(get_current_user)):
    return [current_user]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    raise HTTPException(
        status_code=410,
        detail="Este endpoint fue reemplazado. Usa /api/users/register para crear cuentas con contrasena.",
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, request: Request, response: Response, session: Session = Depends(get_session)):
    settings = get_settings()
    client_ip = request.client.host if request.client else "unknown"
    rate_limit = login_rate_limiter.check(
        client_ip,
        max_attempts=settings.login_rate_limit_per_minute,
        window_seconds=60,
        min_interval_seconds=settings.login_min_interval_seconds,
    )
    if not rate_limit.allowed:
        response.headers["Retry-After"] = str(rate_limit.retry_after_seconds)
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Demasiados intentos de registro. Intenta nuevamente en breve.",
                "reason": rate_limit.reason,
                "retry_after_seconds": rate_limit.retry_after_seconds,
            },
        )

    if not verify_recaptcha_token(payload.recaptcha_token, remote_ip=client_ip):
        raise HTTPException(status_code=400, detail="No se pudo verificar reCAPTCHA")

    existing_user = session.exec(select(User).where(User.email == payload.email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con este correo")
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="La contrasena debe tener al menos 8 caracteres")

    user = User(
        full_name=payload.full_name,
        email=str(payload.email),
        password_hash=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=AuthToken)
def login_user(payload: LoginRequest, request: Request, response: Response, session: Session = Depends(get_session)):
    settings = get_settings()
    client_ip = request.client.host if request.client else "unknown"
    rate_limit = login_rate_limiter.check(
        client_ip,
        max_attempts=settings.login_rate_limit_per_minute,
        window_seconds=60,
        min_interval_seconds=settings.login_min_interval_seconds,
    )
    if not rate_limit.allowed:
        response.headers["Retry-After"] = str(rate_limit.retry_after_seconds)
        raise HTTPException(
            status_code=429,
            detail={
                "message": "Demasiados intentos de inicio de sesion. Intenta nuevamente en breve.",
                "reason": rate_limit.reason,
                "retry_after_seconds": rate_limit.retry_after_seconds,
            },
        )

    if not verify_recaptcha_token(payload.recaptcha_token, remote_ip=client_ip):
        raise HTTPException(status_code=400, detail="No se pudo verificar reCAPTCHA")

    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    user.last_login_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)

    return AuthToken(
        access_token=create_access_token(user.id),
        user=user,
    )


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return current_user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user = current_user

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
