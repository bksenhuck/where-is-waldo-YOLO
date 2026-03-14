"""
Deployment & cloud settings — project constants + env vars for server/GCS.
Project-specific constants (paths, scene sizes, etc.) live in backend/utils/config.py.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Server ────────────────────────────────────────────────────────────────────
PORT     = int(os.getenv("PORT", 8050))
DEBUG    = os.getenv("DEBUG", "false").lower() == "true"
API_BASE = os.getenv("API_BASE", "http://localhost:8050")

# ── GCS ───────────────────────────────────────────────────────────────────────
GCS_BUCKET_NAME    = os.environ.get("GCS_BUCKET_NAME", "where-is-waldo-artifacts")
GCS_MODELS_PREFIX  = os.environ.get("GCS_MODELS_PREFIX",  "models")
GCS_ASSETS_PREFIX  = os.environ.get("GCS_ASSETS_PREFIX",  "assets")
GCS_DATA_PREFIX    = os.environ.get("GCS_DATA_PREFIX",    "data")
