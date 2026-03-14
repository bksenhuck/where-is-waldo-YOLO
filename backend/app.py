"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Where is Waldo — API",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    app.include_router(router, prefix="/api")
    return app
