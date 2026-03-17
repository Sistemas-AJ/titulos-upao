from datetime import datetime, timezone
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main() -> int:
    cleanup_url = os.getenv(
        "CLEANUP_URL",
        "http://backend:8000/api/title-sessions/expired",
    )
    request = Request(cleanup_url, method="DELETE")
    started_at = datetime.now(timezone.utc).isoformat()

    try:
        with urlopen(request, timeout=30) as response:
            print(
                f"[{started_at}] cleanup completed with status {response.status}",
                flush=True,
            )
            return 0
    except HTTPError as exc:
        print(
            f"[{started_at}] cleanup failed with HTTP {exc.code}: {exc.reason}",
            file=sys.stderr,
            flush=True,
        )
    except URLError as exc:
        print(
            f"[{started_at}] cleanup failed: {exc.reason}",
            file=sys.stderr,
            flush=True,
        )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
