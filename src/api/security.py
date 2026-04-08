from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass

from fastapi import Header, HTTPException, Request

from src.settings import get_env_settings, is_auth_required, is_rate_limit_enabled


@dataclass
class RateLimitState:
    hits: dict[str, deque[float]]


RATE_STATE = RateLimitState(hits=defaultdict(deque))


def _is_exempt_path(path: str) -> bool:
    exempt_prefixes = (
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/app",
        "/",
        "/static",
    )
    if path in {"/", "/health", "/app"}:
        return True
    return any(path.startswith(prefix) for prefix in exempt_prefixes if prefix not in {"/", "/health", "/app"})


def enforce_rate_limit(request: Request) -> None:
    settings = get_env_settings()
    if not is_rate_limit_enabled():
        return
    if _is_exempt_path(request.url.path):
        return

    now = time.time()
    window_seconds = max(1, settings.rate_limit_window_seconds)
    max_requests = max(1, settings.rate_limit_requests)

    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{request.url.path}"
    queue = RATE_STATE.hits[key]

    while queue and now - queue[0] > window_seconds:
        queue.popleft()

    if len(queue) >= max_requests:
        raise HTTPException(status_code=429, detail="rate_limit_exceeded")

    queue.append(now)


def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    settings = get_env_settings()
    if not is_auth_required():
        return

    expected = settings.api_key.strip()
    provided = (x_api_key or "").strip()
    if not expected:
        raise HTTPException(status_code=500, detail="server_auth_not_configured")
    if provided != expected:
        raise HTTPException(status_code=401, detail="unauthorized")
