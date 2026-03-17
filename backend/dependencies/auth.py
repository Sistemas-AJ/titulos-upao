from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session

from backend.database.session import get_session
from backend.models.user import User
from backend.services.auth import decode_access_token


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token requerido")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
    return token


def get_current_user(
    authorization: str | None = Header(default=None),
    session: Session = Depends(get_session),
) -> User:
    token = _extract_bearer_token(authorization)
    try:
        user_id = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado")
    return user


def get_optional_current_user(
    authorization: str | None = Header(default=None),
    session: Session = Depends(get_session),
) -> User | None:
    if not authorization:
        return None
    return get_current_user(authorization=authorization, session=session)
