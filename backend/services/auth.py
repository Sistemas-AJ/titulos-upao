import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from backend.config import get_settings


PBKDF2_ITERATIONS = 200_000


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded_password: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = encoded_password.split("$", 3)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    computed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(computed.hex(), digest_hex)


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def create_access_token(user_id: UUID) -> str:
    settings = get_settings()
    payload = {
        "sub": str(user_id),
        "exp": int((utc_now() + timedelta(minutes=settings.auth_token_ttl_minutes)).timestamp()),
    }
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_b64 = _b64url_encode(payload_bytes)
    signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return f"{payload_b64}.{_b64url_encode(signature)}"


def decode_access_token(token: str) -> UUID:
    settings = get_settings()

    try:
        payload_b64, signature_b64 = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Token invalido") from exc

    expected_signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_b64url_encode(expected_signature), signature_b64):
        raise ValueError("Firma de token invalida")

    payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    if int(payload["exp"]) < int(utc_now().timestamp()):
        raise ValueError("Token expirado")

    return UUID(payload["sub"])
