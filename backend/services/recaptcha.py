import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from backend.config import get_settings


RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


def verify_recaptcha_token(token: str | None, remote_ip: str | None = None) -> bool:
    settings = get_settings()
    if not settings.recaptcha_secret_key:
        return True

    if not token:
        return False

    payload = {
        "secret": settings.recaptcha_secret_key,
        "response": token,
    }
    if remote_ip:
        payload["remoteip"] = remote_ip

    request = Request(
        RECAPTCHA_VERIFY_URL,
        data=urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return False

    return bool(data.get("success"))
