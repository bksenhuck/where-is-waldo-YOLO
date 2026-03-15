"""FastAPI application factory."""

from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router
from backend.security import SLOWAPI_AVAILABLE, limiter


def _get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ALLOW_ORIGINS", "").strip()
    if not raw:
        return []
    return [o.strip() for o in raw.split(",") if o.strip()]


def create_app() -> FastAPI:
    enable_docs = (
        os.getenv("ENABLE_API_DOCS", "false").lower() == "true"
    )

    app = FastAPI(
        title="Where is Waldo — API",
        version="1.0.0",
        docs_url="/api/docs" if enable_docs else None,
        redoc_url="/api/redoc" if enable_docs else None,
    )

    # ── Security headers ──────────────────────────────────────────────
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api"):
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Cache-Control"] = "no-store"
            response.headers["Referrer-Policy"] = (
                "strict-origin-when-cross-origin"
            )
            response.headers["Permissions-Policy"] = (
                "geolocation=(), microphone=(), camera=()"
            )
        return response

    # ── CORS ──────────────────────────────────────────────────────────
    origins = _get_cors_origins()
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type", "X-Api-Key"],
        )

    # ── Rate limiting ─────────────────────────────────────────────────
    if SLOWAPI_AVAILABLE:
        from slowapi import _rate_limit_exceeded_handler
        from slowapi.errors import RateLimitExceeded
        from slowapi.middleware import SlowAPIMiddleware

        app.state.limiter = limiter
        app.add_exception_handler(
            RateLimitExceeded, _rate_limit_exceeded_handler
        )
        app.add_middleware(SlowAPIMiddleware)

    app.include_router(router, prefix="/api")
    return app
