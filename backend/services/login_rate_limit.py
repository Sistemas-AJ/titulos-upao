from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock
from time import time


@dataclass
class LoginRateLimitStatus:
    allowed: bool
    retry_after_seconds: int
    reason: str | None = None


class LoginRateLimiter:
    def __init__(self) -> None:
        self._attempts: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, ip: str, max_attempts: int, window_seconds: int, min_interval_seconds: int) -> LoginRateLimitStatus:
        now = time()
        with self._lock:
            attempts = self._attempts[ip]
            while attempts and now - attempts[0] > window_seconds:
                attempts.popleft()

            if attempts and now - attempts[-1] < min_interval_seconds:
                retry_after = max(1, int(min_interval_seconds - (now - attempts[-1])))
                return LoginRateLimitStatus(
                    allowed=False,
                    retry_after_seconds=retry_after,
                    reason="burst_detected",
                )

            if len(attempts) >= max_attempts:
                retry_after = max(1, int(window_seconds - (now - attempts[0])))
                return LoginRateLimitStatus(
                    allowed=False,
                    retry_after_seconds=retry_after,
                    reason="rate_limit_exceeded",
                )

            attempts.append(now)
            return LoginRateLimitStatus(allowed=True, retry_after_seconds=0)


login_rate_limiter = LoginRateLimiter()
