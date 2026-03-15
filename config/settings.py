"""
Deployment & cloud settings.
Project-specific constants live in backend/utils/config.py.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# ── Server ────────────────────────────────────────────────────────────────────
PORT = int(os.getenv("PORT", 8050))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
API_BASE = os.getenv("API_BASE", "http://localhost:8050")

# ── Security ──────────────────────────────────────────────────────────────────
# Shared secret between Dash callbacks and FastAPI endpoints.
# Generate: python -c "import secrets; print(secrets.token_hex(32))"
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "")

# ── GCS ───────────────────────────────────────────────────────────────────────
GCS_BUCKET_NAME = os.environ.get(
    "GCS_BUCKET_NAME", "where-is-waldo-artifacts"
)
GCS_MODELS_PREFIX = os.environ.get("GCS_MODELS_PREFIX", "models")
GCS_ASSETS_PREFIX = os.environ.get("GCS_ASSETS_PREFIX", "assets")
GCS_DATA_PREFIX = os.environ.get("GCS_DATA_PREFIX", "data")
