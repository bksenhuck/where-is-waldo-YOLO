"""Ultralytics YOLO training entrypoint."""

from __future__ import annotations

import shutil
import time
import urllib.request
from pathlib import Path

from ultralytics import YOLO
from ultralytics.utils import SETTINGS

from backend.utils.config import get_paths, write_dataset_yaml
from backend.utils.image_utils import ensure_dir
from backend.utils.logging_utils import get_logger
from config.ml_config import (
    YOLO_BASE_MODEL_NAME,
    YOLO_BASE_MODEL_URL,
    YOLO_BATCH,
    YOLO_DEVICE,
    YOLO_MODEL_NAME,
    YOLO_WORKERS,
)

log = get_logger(__name__)

BASE_MODEL_NAME = YOLO_BASE_MODEL_NAME
BASE_MODEL_URL = YOLO_BASE_MODEL_URL

_SEP = "─" * 55


def _hms(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _section(title: str) -> None:
    log.info(_SEP)
    log.info("  %s", title)
    log.info(_SEP)


def _prepare_base_model(models_dir: Path, root_dir: Path) -> Path:
    """Ensure the base checkpoint lives under models_dir."""
    ensure_dir(models_dir)
    model_path = models_dir / BASE_MODEL_NAME
    root_model = root_dir / BASE_MODEL_NAME

    if root_model.exists() and not model_path.exists():
        shutil.move(str(root_model), str(model_path))
        log.info("  Moved base model → %s", model_path)

    if not model_path.exists():
        log.info("  Downloading %s …", BASE_MODEL_NAME)
        t0 = time.time()
        urllib.request.urlretrieve(BASE_MODEL_URL, str(model_path))
        size_mb = model_path.stat().st_size / 1_048_576
        log.info(
            "  Downloaded %.1f MB in %s → %s",
            size_mb, _hms(time.time() - t0), model_path,
        )
    else:
        size_mb = model_path.stat().st_size / 1_048_576
        log.info(
            "  Base model found (%.1f MB) → %s", size_mb, model_path,
        )

    return model_path


def _dataset_has_images(images_dir: Path) -> bool:
    """Return True when at least one image exists under train split."""
    train_dir = images_dir / "train"
    if not train_dir.exists():
        return False
    return any(train_dir.glob("*.png")) or any(train_dir.glob("*.jpg"))


def _count_split(images_dir: Path, split: str) -> int:
    split_dir = images_dir / split
    if not split_dir.exists():
        return 0
    return sum(1 for _ in split_dir.glob("*.png")) + sum(
        1 for _ in split_dir.glob("*.jpg")
    )


def train_model(
    data_config: str | Path | None = None,
    epochs: int = 30,
    imgsz: int = 640,
    auto_generate_dataset: bool = True,
    dataset_images: int = 2000,
) -> Path:
    """Train YOLOv8 model and return path to the best weights file."""
    pipeline_start = time.time()
    paths = get_paths()
    ensure_dir(paths.models_dir)

    log.info(_SEP)
    log.info("  WHERE IS WALDO — YOLO Training Pipeline")
    log.info(_SEP)
    log.info("  model    : %s", BASE_MODEL_NAME)
    log.info("  run name : %s", YOLO_MODEL_NAME)
    log.info("  epochs   : %d", epochs)
    log.info("  imgsz    : %d", imgsz)
    log.info("  batch    : %d", YOLO_BATCH)
    log.info("  workers  : %d", YOLO_WORKERS)
    log.info("  device   : %s", YOLO_DEVICE or "auto")
    log.info("  output   : %s", paths.models_dir)
    log.info(_SEP)

    # ── Step 1: dataset ───────────────────────────────────────────────────
    _section("STEP 1/3  Dataset")
    if auto_generate_dataset and not _dataset_has_images(paths.images_dir):
        log.info(
            "  No training images found — generating dataset "
            "(n_images=%d) …",
            dataset_images,
        )
        t0 = time.time()
        from ml.training.dataset_loader import generate_dataset
        generate_dataset(n_images=dataset_images)
        log.info("  Dataset generated in %s", _hms(time.time() - t0))
    else:
        n_train = _count_split(paths.images_dir, "train")
        n_val = _count_split(paths.images_dir, "val")
        log.info("  Using existing dataset")
        log.info("  train images : %d", n_train)
        log.info("  val   images : %d", n_val)

    data_path = (
        Path(data_config) if data_config is not None else paths.dataset_yaml
    )
    write_dataset_yaml(paths.dataset_yaml, paths.data_dir)
    log.info("  Config YAML  : %s", data_path)

    # ── Step 2: base model ────────────────────────────────────────────────
    _section("STEP 2/3  Base model")
    SETTINGS.update({"weights_dir": str(paths.models_dir)})
    base_model_path = _prepare_base_model(paths.models_dir, paths.root_dir)

    # ── Step 3: train ─────────────────────────────────────────────────────
    _section("STEP 3/3  Training")
    log.info("  Starting Ultralytics YOLO training …")
    log.info("  (Ultralytics progress bars will appear below)")
    log.info(_SEP)

    t_train = time.time()
    model = YOLO(str(base_model_path))
    model.train(
        data=str(data_path),
        epochs=epochs,
        imgsz=imgsz,
        batch=YOLO_BATCH,
        workers=YOLO_WORKERS,
        project=str(paths.models_dir),
        name=YOLO_MODEL_NAME,
        exist_ok=True,
        device=YOLO_DEVICE,
    )
    train_elapsed = time.time() - t_train

    # ── Summary ───────────────────────────────────────────────────────────
    _section("Training complete")
    best = paths.models_dir / YOLO_MODEL_NAME / "weights" / "best.pt"
    if best.exists():
        size_mb = best.stat().st_size / 1_048_576
        log.info("  Best weights : %s (%.1f MB)", best, size_mb)
    else:
        log.warning("  best.pt not found at %s", best)

    log.info("  Training time    : %s", _hms(train_elapsed))
    log.info("  Total pipeline   : %s", _hms(time.time() - pipeline_start))
    log.info(_SEP)

    return best


if __name__ == "__main__":
    best_weights = train_model()
    log.info("Best model saved at: %s", best_weights)
