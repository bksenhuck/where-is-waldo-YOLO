"""Unified FastAPI + Dash entrypoint.

FastAPI serves /api/* endpoints; Dash is mounted at / via WSGIMiddleware.

Run:
    python main.py
    uvicorn main:app --host 0.0.0.0 --port 8050 --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from a2wsgi import WSGIMiddleware
from fastapi import FastAPI

from backend.app import create_app as create_api
from backend.utils.logging_utils import get_logger
from config.settings import PORT
from frontend.dash_app.app import app as dash_app

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    log.info("Where-is-Waldo starting on port %d", PORT)
    yield
    log.info("Where-is-Waldo shutting down")


api = create_api()
api.router.lifespan_context = lifespan

# Mount Dash WSGI app under FastAPI at root "/"
api.mount("/", WSGIMiddleware(dash_app.server))

app = api


def main() -> None:
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
        reload=False,
        access_log=False,
    )


if __name__ == "__main__":
    main()
