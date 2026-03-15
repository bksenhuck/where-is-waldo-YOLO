"""API security helpers: key validation + rate limiter."""

from __future__ import annotations

import os
import secrets

from fastapi import Header, HTTPException

# ── Internal API key ──────────────────────────────────────────────────────────


async def require_api_key(
    x_api_key: str | None = Header(None, alias="X-Api-Key"),
) -> None:
    """Validates X-Api-Key header on /api/scene and /api/detect.

    The key is shared only between the Dash server process and FastAPI —
    it is never sent to the browser.  External callers without the key
    receive a 403 before any ML work is done.

    When INTERNAL_API_KEY is not set (local dev), all requests are allowed.
    Set it in production to enforce access control.
    """
    expected = os.getenv("INTERNAL_API_KEY", "").strip()
    if not expected:
        # Not configured — open mode (local development).
        return
    if not x_api_key or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(403, "Forbidden.")


# ── Rate limiter (slowapi) ────────────────────────────────────────────────────

RATE_LIMIT_SCENE = os.getenv("RATE_LIMIT_SCENE", "30/minute")
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
