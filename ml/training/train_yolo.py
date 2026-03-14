"""Ultralytics YOLO training entrypoint."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

from ultralytics import YOLO

from backend.utils.config import get_paths, write_dataset_yaml
from backend.utils.image_utils import ensure_dir
from backend.utils.logging_utils import get_logger
from config.ml_config import (
    YOLO_BASE_MODEL_NAME,
    YOLO_BASE_MODEL_URL,
    YOLO_MODEL_NAME,
)

log = get_logger(__name__)

BASE_MODEL_NAME = YOLO_BASE_MODEL_NAME
BASE_MODEL_URL = YOLO_BASE_MODEL_URL


def _prepare_base_model(models_dir: Path, root_dir: Path) -> Path:
    """Ensure the base yolov8n checkpoint lives under models/."""
    ensure_dir(models_dir)
    model_path = models_dir / BASE_MODEL_NAME
    root_model = root_dir / BASE_MODEL_NAME

    if root_model.exists() and not model_path.exists():
        shutil.move(str(root_model), str(model_path))
        log.debug("Moved base model %s → %s", root_model, model_path)

    if not model_path.exists():
        log.info("Downloading base model %s …", BASE_MODEL_NAME)
        urllib.request.urlretrieve(BASE_MODEL_URL, str(model_path))
        log.info("Base model saved → %s", model_path)
    else:
        log.debug("Base model found → %s", model_path)

    return model_path


def _dataset_has_images(images_dir: Path) -> bool:
    """Return True when at least one image exists under train split."""
    train_dir = images_dir / "train"
    if not train_dir.exists():
        return False
    return any(train_dir.glob("*.png")) or any(train_dir.glob("*.jpg"))


def train_model(
    data_config: str | Path | None = None,
    epochs: int = 30,
    imgsz: int = 640,
    auto_generate_dataset: bool = True,
    dataset_images: int = 2000,
) -> Path:
    """Train YOLOv8 model and return path to the best weights file."""
    paths = get_paths()
    ensure_dir(paths.models_dir)

    if auto_generate_dataset and not _dataset_has_images(paths.images_dir):
        log.info(
            "No training images found — auto-generating dataset "
            "(n_images=%d) …",
            dataset_images,
        )
        from ml.training.dataset_loader import generate_dataset
        generate_dataset(n_images=dataset_images)
    else:
        train_count = sum(
            1 for _ in (paths.images_dir / "train").glob("*.png")
        )
        log.info(
            "Using existing dataset — %d train images found.", train_count,
        )

    write_dataset_yaml(paths.dataset_yaml, paths.data_dir)
    log.debug("Dataset YAML written → %s", paths.dataset_yaml)

    data_path = (
        Path(data_config) if data_config is not None else paths.dataset_yaml
    )
    base_model_path = _prepare_base_model(paths.models_dir, paths.root_dir)

    log.info(
        "Starting YOLO training  model=%s  epochs=%d  imgsz=%d",
        BASE_MODEL_NAME, epochs, imgsz,
    )
    model = YOLO(str(base_model_path))
    model.train(
        data=str(data_path),
        epochs=epochs,
        imgsz=imgsz,
        project=str(paths.models_dir),
        name=YOLO_MODEL_NAME,
        exist_ok=True,
    )

    best = paths.models_dir / YOLO_MODEL_NAME / "weights" / "best.pt"
    if best.exists():
        log.info("Training complete — best weights → %s", best)
    else:
        log.warning("Training finished but best.pt not found at %s", best)
    return best


if __name__ == "__main__":
    best_weights = train_model()
    log.info("Best model saved at: %s", best_weights)
