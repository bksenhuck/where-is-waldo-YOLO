"""Main procedural scene generation for the Waldo game."""

from __future__ import annotations

import random
from typing import List, Optional, Tuple

from PIL import Image

from ml.data_generation.backgrounds import get_background
from ml.data_generation.characters import (
    random_character_sprite,
    waldo_sprite,
)
from ml.data_generation.collision import can_place_bbox
from backend.utils.bbox_utils import BBox
from backend.utils.config import DIFFICULTY_TO_COUNT, SCENE_SIZE


def _pick_character_size(
    rng: random.Random,
    difficulty: str,
) -> Tuple[int, int]:
    if difficulty == "easy":
        h = rng.randint(55, 85)
    elif difficulty == "medium":
        h = rng.randint(40, 70)
    else:
        h = rng.randint(28, 60)
    w = int(h * rng.uniform(0.55, 0.8))
    return max(18, w), max(26, h)


def _place_sprite(
    canvas: Image.Image,
    sprite: Image.Image,
    placed_bboxes: List[BBox],
    rng: random.Random,
    max_overlap_ratio: float,
    max_attempts: int = 120,
) -> Optional[BBox]:
    width, height = canvas.size
    sw, sh = sprite.size
    if sw >= width or sh >= height:
        return None

    for _ in range(max_attempts):
        x = rng.randint(0, width - sw)
        y = rng.randint(0, height - sh)
        candidate = (x, y, x + sw, y + sh)
        if can_place_bbox(
            candidate,
            placed_bboxes,
            max_overlap_ratio=max_overlap_ratio,
        ):
            canvas.paste(sprite, (x, y), mask=sprite)
            placed_bboxes.append(candidate)
            return candidate
    return None


def generate_scene(
    num_people: int = 80,
    difficulty: str = "medium",
    image_size: Tuple[int, int] = SCENE_SIZE,
    seed: Optional[int] = None,
) -> Tuple[Image.Image, BBox]:
    """Generate a crowded scene with hidden Waldo and return gt bbox."""

    rng = random.Random(seed)
    if difficulty in DIFFICULTY_TO_COUNT:
        num_people = DIFFICULTY_TO_COUNT[difficulty]

    canvas = get_background(image_size, rng).convert("RGBA")
    placed: List[BBox] = []

    waldo_size = _pick_character_size(rng, difficulty)
    waldo = waldo_sprite(rng, waldo_size)
    waldo_bbox = _place_sprite(
        canvas,
        waldo,
        placed,
        rng,
        max_overlap_ratio=0.1,
    )
    if waldo_bbox is None:
        waldo_bbox = (10, 10, 10 + waldo.width, 10 + waldo.height)
        canvas.paste(waldo, (10, 10), mask=waldo)
        placed.append(waldo_bbox)

    for _ in range(num_people):
        char_size = _pick_character_size(rng, difficulty)
        character = random_character_sprite(rng, char_size)
        _place_sprite(
            canvas, character, placed, rng, max_overlap_ratio=0.4,
        )

    return canvas.convert("RGB"), waldo_bbox
