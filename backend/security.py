"""API security helpers: key validation + rate limiter."""

from __future__ import annotations

import os
import secrets

from fastapi import Header, HTTPException

# ── Internal API key ──────────────────────────────────────────────────────────

async def require_api_key(x_api_key: str = Header(..., alias="X-Api-Key")) -> None:
    """Validates X-Api-Key header on every call to /api/scene and /api/detect.

    The key is shared only between the Dash backend process and FastAPI — it is
    never sent to the browser.  External callers that don't know the key receive
    a 403 immediately, before any ML work is done.

    Returns 503 when INTERNAL_API_KEY env var is not set (safe default).
    """
    expected = os.getenv("INTERNAL_API_KEY", "").strip()
    if not expected:
        raise HTTPException(503, "API is not configured on this server.")
    if not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(403, "Forbidden.")


# ── Rate limiter (slowapi) ────────────────────────────────────────────────────

RATE_LIMIT_SCENE  = os.getenv("RATE_LIMIT_SCENE",  "30/minute")
RATE_LIMIT_DETECT = os.getenv("RATE_LIMIT_DETECT", "30/minute")

try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
    SLOWAPI_AVAILABLE = True
except ImportError:  # pragma: no cover
    class _NoOpLimiter:  # type: ignore[no-redef]
        def limit(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
    limiter = _NoOpLimiter()  # type: ignore[assignment]
    SLOWAPI_AVAILABLE = False
