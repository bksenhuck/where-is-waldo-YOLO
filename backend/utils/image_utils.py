"""Image conversion and file utilities."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def ensure_dir(path: Path) -> None:
    """Create a directory recursively if it does not exist."""

    path.mkdir(parents=True, exist_ok=True)


def load_rgba_image(path: Path) -> Image.Image:
    """Load an image as RGBA with Pillow."""

    return Image.open(path).convert("RGBA")


def pil_to_numpy_bgr(image: Image.Image) -> np.ndarray:
    """Convert PIL image to OpenCV BGR numpy array."""

    rgb = image.convert("RGB")
    np_rgb = np.array(rgb, dtype=np.uint8)
    return cv2.cvtColor(np_rgb, cv2.COLOR_RGB2BGR)


def numpy_bgr_to_pil(image: np.ndarray) -> Image.Image:
    """Convert OpenCV BGR numpy array to PIL RGB image."""

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)
