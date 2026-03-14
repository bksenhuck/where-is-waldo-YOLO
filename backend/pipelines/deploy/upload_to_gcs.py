"""
Upload Where-is-Waldo artifacts to Google Cloud Storage.

Uploads:
  [1/3] YOLO model weights  → gs://<bucket>/models/
  [2/3] Generated assets    → gs://<bucket>/assets/
  [3/3] Training data       → gs://<bucket>/data/

Usage:
    python -m backend.pipelines.deploy.upload_to_gcs
    python -m backend.pipelines.deploy.upload_to_gcs --dry-run
"""
from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# GCS configuration — single source of truth is config/settings.py
from config.settings import (  # noqa: E402
    GCS_ASSETS_PREFIX,
    GCS_BUCKET_NAME,
    GCS_DATA_PREFIX,
    GCS_MODELS_PREFIX,
)
from backend.utils.config import get_paths  # noqa: E402
from backend.utils.logging_utils import get_logger  # noqa: E402

log = get_logger(__name__)

_MODEL_EXT = (".pt", ".onnx", ".pkl", ".joblib")
_ASSET_EXT = (".png", ".jpg", ".jpeg", ".webp")
_DATA_EXT  = (".png", ".jpg", ".jpeg", ".txt", ".yaml")


# ── Helpers ────────────────────────────────────────────────────────────────────

def _upload_file(
    bucket, local: Path, blob_path: str, dry_run: bool
) -> None:
    size_mb = local.stat().st_size / 1_048_576
    tag = "[dry-run]" if dry_run else "uploaded "
    log.info(
        "%s %s  →  gs://%s/%s  (%.2f MB)",
        tag, local.name, bucket.name, blob_path, size_mb,
    )
    if not dry_run:
        bucket.blob(blob_path).upload_from_filename(str(local))


def _upload_dir(
    bucket,
    local_dir: Path,
    prefix: str,
    dry_run: bool,
    extensions: tuple[str, ...] | None = None,
) -> int:
    count = 0
    for f in sorted(local_dir.rglob("*")):
        if not f.is_file():
            continue
        if extensions and f.suffix.lower() not in extensions:
            continue
        blob = f"{prefix}/{f.relative_to(local_dir).as_posix()}"
        _upload_file(bucket, f, blob, dry_run)
        count += 1
    return count


# ── Main ───────────────────────────────────────────────────────────────────────

def run(dry_run: bool = False) -> None:
    if not GCS_BUCKET_NAME:
        raise EnvironmentError(
            "GCS_BUCKET_NAME not set — fill in .env first."
        )
    try:
        from google.cloud import storage
    except ImportError:
        raise ImportError("Run: pip install google-cloud-storage")

    paths = get_paths()
    bucket = storage.Client().bucket(GCS_BUCKET_NAME)
    log.info("Target bucket: gs://%s", GCS_BUCKET_NAME)

    # [1/3] YOLO model weights
    log.info("[1/3] Model weights")
    if paths.models_dir.exists():
        count = _upload_dir(
            bucket, paths.models_dir, GCS_MODELS_PREFIX,
            dry_run, extensions=_MODEL_EXT,
        )
    else:
        count = 0
    if count == 0:
        log.warning(
            "No model files found — "
            "train first with model/pipelines/train_model.py"
        )

    # [2/3] Generated assets
    log.info("[2/3] Generated assets")
    if paths.assets_dir.exists():
        n = _upload_dir(
            bucket, paths.assets_dir, GCS_ASSETS_PREFIX,
            dry_run, extensions=_ASSET_EXT,
        )
        log.info("%d asset file(s) processed", n)
    else:
        log.warning("Assets dir not found at %s", paths.assets_dir)

    # [3/3] Training data
    log.info("[3/3] Training data (images & labels)")
    if paths.data_dir.exists():
        n = _upload_dir(
            bucket, paths.data_dir, GCS_DATA_PREFIX,
            dry_run, extensions=_DATA_EXT,
        )
        log.info("%d data file(s) processed", n)
    else:
        log.warning("Data dir not found at %s", paths.data_dir)

    log.info("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload Where-is-Waldo artifacts to GCS."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be uploaded without uploading.",
    )
    run(dry_run=parser.parse_args().dry_run)
