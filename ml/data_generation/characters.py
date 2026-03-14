"""Character sprite loading with synthetic fallback creation."""

from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw

from backend.utils.config import get_paths


def _list_sprite_files(directory: Path) -> List[Path]:
    if not directory.exists():
        return []
    return [
        p
        for p in directory.iterdir()
        if p.suffix.lower() in {".png", ".webp"}
    ]


def _synthetic_person(
    size: Tuple[int, int],
    rng: random.Random,
    waldo: bool = False,
) -> Image.Image:
    width, height = size
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    shirt_top = int(height * 0.33)
    shirt_bottom = int(height * 0.72)
    body_margin = int(width * 0.2)
    body_left = body_margin
    body_right = width - body_margin

    skin = (245, 206, 170, 255)
    pants = (35, 70, 150, 255)
    if waldo:
        stripe_a = (230, 35, 40, 255)
        stripe_b = (245, 245, 245, 255)
        hat_color = (230, 35, 40, 255)
    else:
        stripe_a = (
            rng.randint(40, 240),
            rng.randint(40, 240),
            rng.randint(40, 240),
            255,
        )
        stripe_b = (
            rng.randint(40, 240),
            rng.randint(40, 240),
            rng.randint(40, 240),
            255,
        )
        hat_color = stripe_a

    head_r = int(min(width, height) * 0.16)
    head_center = (width // 2, int(height * 0.2))
    d.ellipse(
        [
            head_center[0] - head_r,
            head_center[1] - head_r,
            head_center[0] + head_r,
            head_center[1] + head_r,
        ],
        fill=skin,
        outline=(20, 20, 20, 255),
    )

    stripe_h = max(3, int((shirt_bottom - shirt_top) / 8))
    toggle = True
    y = shirt_top
    while y < shirt_bottom:
        color = stripe_a if toggle else stripe_b
        d.rectangle(
            [body_left, y, body_right, min(shirt_bottom, y + stripe_h)],
            fill=color,
        )
        toggle = not toggle
        y += stripe_h

    d.rectangle(
        [body_left + 2, shirt_bottom, body_right - 2, int(height * 0.94)],
        fill=pants,
    )

    arm_w = max(4, int(width * 0.12))
    d.rectangle(
        [body_left - arm_w, shirt_top + 8, body_left, shirt_bottom - 4],
        fill=stripe_a,
    )
    d.rectangle(
        [body_right, shirt_top + 8, body_right + arm_w, shirt_bottom - 4],
        fill=stripe_a,
    )

    hat_top = int(height * 0.06)
    hat_bottom = int(height * 0.13)
    d.rectangle(
        [width // 2 - head_r, hat_top, width // 2 + head_r, hat_bottom],
        fill=hat_color,
    )
    d.rectangle(
        [
            width // 2 - head_r - 6,
            hat_bottom,
            width // 2 + head_r + 6,
            hat_bottom + 4,
        ],
        fill=(30, 30, 30, 255),
    )

    return img


def random_character_sprite(
    rng: random.Random,
    size: Tuple[int, int],
) -> Image.Image:
    """Return random non-Waldo sprite from assets or synthetic fallback."""

    paths = get_paths()
    files = _list_sprite_files(paths.characters_dir)
    if files:
        sprite = Image.open(rng.choice(files)).convert("RGBA")
        return sprite.resize(size, Image.Resampling.LANCZOS)
    return _synthetic_person(size, rng, waldo=False)


def waldo_sprite(rng: random.Random, size: Tuple[int, int]) -> Image.Image:
    """Return waldo sprite from assets or synthetic fallback."""

    paths = get_paths()
    files = _list_sprite_files(paths.waldo_dir)
    if files:
        sprite = Image.open(rng.choice(files)).convert("RGBA")
        return sprite.resize(size, Image.Resampling.LANCZOS)
    return _synthetic_person(size, rng, waldo=True)
