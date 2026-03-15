"""Inference utilities for detecting Waldo in an image."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from PIL import Image
from ultralytics import YOLO

from backend.utils.bbox_utils import BBox
from backend.utils.config import get_paths
from config.ml_config import YOLO_MODEL_NAME


_model_cache: dict[str, YOLO] = {}


def _default_model_path() -> Optional[Path]:
    paths = get_paths()
    primary = paths.models_dir / YOLO_MODEL_NAME / "weights" / "best.pt"
    if primary.exists():
        return primary
    candidates = sorted(paths.models_dir.rglob("*.pt"))
    return candidates[-1] if candidates else None


def _load_model(model_path: Path) -> YOLO:
    key = str(model_path)
    if key not in _model_cache:
        _model_cache[key] = YOLO(key)
    return _model_cache[key]


def _to_rgb_numpy(image: Image.Image | np.ndarray) -> np.ndarray:
    if isinstance(image, Image.Image):
        return np.array(image.convert("RGB"))
    if image.ndim == 2:
        return np.stack([image] * 3, axis=-1)
    return image


def warmup_detector() -> bool:
    """Preload model and run one tiny inference to reduce cold-start latency."""
    selected_model = _default_model_path()
    if selected_model is None or not selected_model.exists():
        return False

    model = _load_model(selected_model)
    dummy = np.zeros((64, 64, 3), dtype=np.uint8)
    model.predict(source=dummy, conf=0.25, verbose=False)
    return True


def detect_waldo(
    image: Image.Image | np.ndarray,
    model_path: str | Path | None = None,
    conf: float = 0.25,
) -> List[Dict[str, float | BBox]]:
    """Detect Waldo and return list of bbox and confidence predictions."""

    selected_model = (
        Path(model_path)
        if model_path is not None
        else _default_model_path()
    )
    if selected_model is None or not selected_model.exists():
        return []

    model = _load_model(selected_model)
    rgb = _to_rgb_numpy(image)
    results = model.predict(source=rgb, conf=conf, verbose=False)
    if not results:
        return []

    detections: List[Dict[str, float | BBox]] = []
    boxes = results[0].boxes
    if boxes is None:
        return detections

    xyxy = (
        boxes.xyxy.cpu().numpy()
        if hasattr(boxes.xyxy, "cpu")
        else boxes.xyxy
    )
    confs = (
        boxes.conf.cpu().numpy()
        if hasattr(boxes.conf, "cpu")
        else boxes.conf
    )

    for i in range(len(xyxy)):
        x1, y1, x2, y2 = xyxy[i]
        detections.append(
            {
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
                "confidence": float(confs[i]),
            }
        )

    detections.sort(key=lambda d: float(d["confidence"]), reverse=True)
    return detections
