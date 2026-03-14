"""Background loading and synthetic fallback generation."""

from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw

from backend.utils.config import get_paths


def list_background_files() -> List[Path]:
    """List available background files from assets folder."""

    paths = get_paths()
    if not paths.backgrounds_dir.exists():
        return []
    return [
        p
        for p in paths.backgrounds_dir.iterdir()
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]


def synthetic_background(
    size: Tuple[int, int],
    rng: random.Random,
) -> Image.Image:
    """Create a synthetic noisy city-like background."""

    width, height = size
    base = Image.new("RGB", (width, height), color=(220, 230, 240))
    draw = ImageDraw.Draw(base)

    for _ in range(260):
        x1 = rng.randint(0, width - 1)
        y1 = rng.randint(0, height - 1)
        w = rng.randint(20, 120)
        h = rng.randint(20, 140)
        color = (
            rng.randint(120, 240),
            rng.randint(120, 240),
            rng.randint(120, 240),
        )
        draw.rectangle(
            [x1, y1, min(width, x1 + w), min(height, y1 + h)],
            outline=color,
        )

    for _ in range(120):
        x = rng.randint(0, width - 1)
        y = rng.randint(0, height - 1)
        r = rng.randint(4, 12)
        color = (
            rng.randint(80, 180),
            rng.randint(80, 180),
            rng.randint(80, 180),
        )
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

    return base


def get_background(size: Tuple[int, int], rng: random.Random) -> Image.Image:
    """Load random background from assets or fallback to synthetic one."""

    files = list_background_files()
    if not files:
        return synthetic_background(size, rng)

    chosen = rng.choice(files)
    image = Image.open(chosen).convert("RGB")
    return image.resize(size, Image.Resampling.LANCZOS)
