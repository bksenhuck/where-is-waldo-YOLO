"""Procedural retro pixel-art character generator.

This script creates unique 128x128 transparent PNG sprites using a
modular body-part system with optional accessories.

Usage:
    python -m ml.data_generation.character_generator
    python -m ml.data_generation.character_generator --count 500
"""

from __future__ import annotations

import argparse
import sys
import random
from pathlib import Path
from typing import Dict, List, Tuple, TypedDict

from PIL import Image, ImageDraw
from tqdm import tqdm

from backend.utils.logging_utils import get_logger
from config.ml_config import (
    CHARACTER_BASE_SIZE,
    CHARACTER_DEFAULT_COUNT,
    CHARACTER_SCALE,
    CHARACTER_THEME_MIX_WEIGHTS,
)

log = get_logger(__name__)

# ── Project root on sys.path so backend imports work ────────────────────────
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# ----------------------------------------------------------------------------
# Constants and palette
# ----------------------------------------------------------------------------

ASSETS_DIR = _ROOT / "frontend" / "assets"
OUTPUT_DIR = ASSETS_DIR / "characters"
WALDO_DIR = ASSETS_DIR / "waldo"

DEFAULT_COUNT = CHARACTER_DEFAULT_COUNT
BASE_SIZE = CHARACTER_BASE_SIZE
SCALE = CHARACTER_SCALE
SPRITE_SIZE = BASE_SIZE * SCALE
OUTLINE = (0, 0, 0, 255)

SKIN_TONES: List[Tuple[int, int, int, int]] = [
    (255, 224, 189, 255),
    (241, 194, 125, 255),
    (224, 172, 105, 255),
    (198, 134, 66, 255),
    (141, 85, 36, 255),
]

HAIR_COLORS: List[Tuple[int, int, int, int]] = [
    (34, 24, 20, 255),
    (82, 53, 40, 255),
    (141, 101, 58, 255),
    (210, 180, 95, 255),
    (125, 125, 125, 255),
    (196, 98, 73, 255),
]

CLOTH_MAIN: List[Tuple[int, int, int, int]] = [
    (54, 96, 187, 255),
    (42, 135, 74, 255),
    (192, 62, 62, 255),
    (149, 89, 196, 255),
    (197, 145, 51, 255),
    (60, 60, 72, 255),
    (87, 158, 172, 255),
]

PANTS_COLORS: List[Tuple[int, int, int, int]] = [
    (34, 51, 94, 255),
    (72, 72, 84, 255),
    (88, 59, 40, 255),
    (48, 77, 56, 255),
]

SHOE_COLORS: List[Tuple[int, int, int, int]] = [
    (32, 32, 32, 255),
    (68, 45, 36, 255),
    (28, 41, 66, 255),
]

HAT_COLORS: List[Tuple[int, int, int, int]] = [
    (204, 62, 62, 255),
    (54, 96, 187, 255),
    (57, 128, 73, 255),
    (188, 132, 48, 255),
    (96, 81, 151, 255),
    (74, 74, 74, 255),
]

THEMES = ("tourist", "explorer", "casual")


class ThemeSpec(TypedDict):
    """Configuration bundle for one character theme profile."""

    main_palette: List[Tuple[int, int, int, int]]
    pants_palette: List[Tuple[int, int, int, int]]
    hat_palette: List[Tuple[int, int, int, int]]
    backpack_palette: List[Tuple[int, int, int, int]]
    body_weights: Tuple[int, int, int]
    leg_weights: Tuple[int, int, int]
    shoe_weights: Tuple[int, int]
    hat_prob: float
    hair_prob: float
    beard_prob: float
    glasses_prob: float
    backpack_prob: float
    scarf_prob: float


THEME_PROFILES: Dict[str, ThemeSpec] = {
    "tourist": {
        "main_palette": [
            CLOTH_MAIN[0],
            CLOTH_MAIN[2],
            CLOTH_MAIN[4],
            CLOTH_MAIN[6],
        ],
        "pants_palette": [PANTS_COLORS[0], PANTS_COLORS[1], PANTS_COLORS[3]],
        "hat_palette": [HAT_COLORS[0], HAT_COLORS[1], HAT_COLORS[3]],
        "backpack_palette": [CLOTH_MAIN[4], CLOTH_MAIN[6], CLOTH_MAIN[0]],
        "body_weights": (20, 35, 45),
        "leg_weights": (20, 55, 25),
        "shoe_weights": (50, 50),
        "hat_prob": 0.48,
        "hair_prob": 0.65,
        "beard_prob": 0.12,
        "glasses_prob": 0.42,
        "backpack_prob": 0.34,
        "scarf_prob": 0.10,
    },
    "explorer": {
        "main_palette": [
            CLOTH_MAIN[1],
            CLOTH_MAIN[4],
            CLOTH_MAIN[5],
            CLOTH_MAIN[6],
        ],
        "pants_palette": [PANTS_COLORS[2], PANTS_COLORS[3], PANTS_COLORS[1]],
        "hat_palette": [HAT_COLORS[3], HAT_COLORS[2], HAT_COLORS[5]],
        "backpack_palette": [CLOTH_MAIN[1], CLOTH_MAIN[4], CLOTH_MAIN[5]],
        "body_weights": (35, 25, 40),
        "leg_weights": (50, 20, 30),
        "shoe_weights": (70, 30),
        "hat_prob": 0.52,
        "hair_prob": 0.42,
        "beard_prob": 0.36,
        "glasses_prob": 0.16,
        "backpack_prob": 0.58,
        "scarf_prob": 0.24,
    },
    "casual": {
        "main_palette": CLOTH_MAIN,
        "pants_palette": PANTS_COLORS,
        "hat_palette": HAT_COLORS,
        "backpack_palette": CLOTH_MAIN,
        "body_weights": (34, 33, 33),
        "leg_weights": (38, 28, 34),
        "shoe_weights": (55, 45),
        "hat_prob": 0.24,
        "hair_prob": 0.58,
        "beard_prob": 0.18,
        "glasses_prob": 0.20,
        "backpack_prob": 0.20,
        "scarf_prob": 0.16,
    },
}

THEME_MIX_WEIGHTS = CHARACTER_THEME_MIX_WEIGHTS


def ensure_output_dir() -> None:
    """Ensure sprite output directories exist."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    WALDO_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------
# Low-level helpers
# ----------------------------------------------------------------------------

def _shade(
    color: Tuple[int, int, int, int],
    delta: int,
) -> Tuple[int, int, int, int]:
    r, g, b, a = color
    return (
        max(0, min(255, r + delta)),
        max(0, min(255, g + delta)),
        max(0, min(255, b + delta)),
        a,
    )


def _rect(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    fill: Tuple[int, int, int, int],
    outline: bool = True,
) -> None:
    draw.rectangle(box, fill=fill)
    if outline:
        draw.rectangle(box, outline=OUTLINE)


# ----------------------------------------------------------------------------
# Body-part drawing functions
# ----------------------------------------------------------------------------

def draw_head(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    skin: Tuple[int, int, int, int],
) -> None:
    """Draw head and face details."""

    _rect(draw, (x_center - 4, 4, x_center + 4, 10), skin)
    eye = (25, 25, 25, 255)
    draw.point((x_center - 2, 7), fill=eye)
    draw.point((x_center + 2, 7), fill=eye)
    draw.line((x_center - 1, 9, x_center + 1, 9), fill=_shade(skin, -30))


def draw_body(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    main_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw torso in different clothing styles."""

    if style == 0:
        _rect(draw, (x_center - 5, 11, x_center + 5, 19), main_color)
        _rect(
            draw,
            (x_center - 2, 14, x_center + 2, 15),
            _shade(main_color, 25),
        )
    elif style == 1:
        _rect(draw, (x_center - 5, 11, x_center + 5, 19), main_color)
        draw.line((x_center, 11, x_center, 19), fill=_shade(main_color, 30))
    else:
        _rect(draw, (x_center - 5, 11, x_center + 5, 19), main_color)
        for yy in range(12, 19, 2):
            draw.line(
                (x_center - 4, yy, x_center + 4, yy),
                fill=_shade(main_color, -18),
            )


def draw_arms(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    sleeve_color: Tuple[int, int, int, int],
    skin: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw arms with small style variation."""

    if style == 0:
        _rect(draw, (x_center - 8, 12, x_center - 6, 19), sleeve_color)
        _rect(draw, (x_center + 6, 12, x_center + 8, 19), sleeve_color)
    else:
        _rect(draw, (x_center - 8, 13, x_center - 6, 20), sleeve_color)
        _rect(draw, (x_center + 6, 13, x_center + 8, 20), sleeve_color)

    _rect(draw, (x_center - 8, 20, x_center - 6, 21), skin)
    _rect(draw, (x_center + 6, 20, x_center + 8, 21), skin)


def draw_legs(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    leg_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw legs with shorts or pants."""

    if style == 0:
        _rect(draw, (x_center - 5, 20, x_center - 1, 28), leg_color)
        _rect(draw, (x_center + 1, 20, x_center + 5, 28), leg_color)
    elif style == 1:
        _rect(draw, (x_center - 5, 20, x_center - 1, 26), leg_color)
        _rect(draw, (x_center + 1, 20, x_center + 5, 26), leg_color)
    else:
        _rect(
            draw,
            (x_center - 5, 20, x_center - 1, 28),
            _shade(leg_color, -15),
        )
        _rect(draw, (x_center + 1, 20, x_center + 5, 28), leg_color)


def draw_shoes(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    shoe_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw shoes at sprite base."""

    if style == 0:
        _rect(draw, (x_center - 6, 28, x_center - 1, 30), shoe_color)
        _rect(draw, (x_center + 1, 28, x_center + 6, 30), shoe_color)
    else:
        _rect(draw, (x_center - 6, 28, x_center - 1, 29), shoe_color)
        _rect(draw, (x_center + 1, 28, x_center + 6, 29), shoe_color)


def draw_hair(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    hair_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw one of 6 hair styles."""

    if style == 0:
        _rect(draw, (x_center - 4, 2, x_center + 4, 4), hair_color)
    elif style == 1:
        _rect(draw, (x_center - 5, 2, x_center + 5, 4), hair_color)
        _rect(draw, (x_center - 5, 5, x_center - 4, 8), hair_color)
        _rect(draw, (x_center + 4, 5, x_center + 5, 8), hair_color)
    elif style == 2:
        _rect(draw, (x_center - 3, 2, x_center + 3, 3), hair_color)
    elif style == 3:
        _rect(draw, (x_center - 4, 2, x_center + 4, 5), hair_color)
        _rect(draw, (x_center - 5, 6, x_center - 4, 8), hair_color)
    elif style == 4:
        _rect(draw, (x_center - 5, 3, x_center + 5, 5), hair_color)
    else:
        _rect(draw, (x_center - 4, 2, x_center + 4, 3), hair_color)
        _rect(draw, (x_center - 2, 4, x_center + 2, 4), hair_color)


def draw_hat(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    hat_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw one of 6 hat styles."""

    if style == 0:
        _rect(draw, (x_center - 5, 1, x_center + 5, 3), hat_color)
        _rect(
            draw,
            (x_center - 6, 4, x_center + 6, 4),
            _shade(hat_color, -18),
        )
    elif style == 1:
        _rect(draw, (x_center - 4, 0, x_center + 4, 3), hat_color)
        _rect(
            draw,
            (x_center - 6, 4, x_center + 6, 4),
            _shade(hat_color, -12),
        )
    elif style == 2:
        _rect(draw, (x_center - 4, 1, x_center + 4, 4), hat_color)
        draw.polygon(
            [(x_center - 2, 1), (x_center + 2, 1), (x_center, 0)],
            fill=_shade(hat_color, 15),
            outline=OUTLINE,
        )
    elif style == 3:
        _rect(draw, (x_center - 5, 2, x_center + 5, 4), hat_color)
    elif style == 4:
        _rect(draw, (x_center - 4, 1, x_center + 4, 4), hat_color)
        draw.line(
            (x_center - 4, 3, x_center + 4, 3),
            fill=_shade(hat_color, 20),
        )
    else:
        _rect(draw, (x_center - 3, 0, x_center + 3, 4), hat_color)
        _rect(
            draw,
            (x_center - 6, 4, x_center + 6, 4),
            _shade(hat_color, -15),
        )


def draw_glasses(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    style: int,
) -> None:
    """Draw one of 3 glasses styles."""

    frame = (24, 24, 24, 255)
    lens = (180, 220, 240, 180)

    if style == 0:
        _rect(draw, (x_center - 3, 6, x_center - 1, 8), lens, outline=True)
        _rect(draw, (x_center + 1, 6, x_center + 3, 8), lens, outline=True)
        draw.line((x_center - 1, 7, x_center + 1, 7), fill=frame)
    elif style == 1:
        _rect(draw, (x_center - 4, 6, x_center - 2, 8), lens, outline=True)
        _rect(draw, (x_center + 2, 6, x_center + 4, 8), lens, outline=True)
        draw.line((x_center - 2, 7, x_center + 2, 7), fill=frame)
    else:
        _rect(draw, (x_center - 3, 6, x_center + 3, 8), lens, outline=True)


def draw_beard(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    beard_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw one of 4 beard styles."""

    if style == 0:
        _rect(draw, (x_center - 2, 9, x_center + 2, 10), beard_color)
    elif style == 1:
        _rect(draw, (x_center - 3, 9, x_center + 3, 11), beard_color)
    elif style == 2:
        _rect(draw, (x_center - 1, 9, x_center + 1, 10), beard_color)
    else:
        _rect(draw, (x_center - 4, 9, x_center + 4, 10), beard_color)


def draw_backpack(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    backpack_color: Tuple[int, int, int, int],
    style: int,
) -> None:
    """Draw one of 3 backpack styles."""

    if style == 0:
        _rect(draw, (x_center + 6, 12, x_center + 8, 19), backpack_color)
    elif style == 1:
        _rect(draw, (x_center - 8, 12, x_center - 6, 19), backpack_color)
    else:
        _rect(draw, (x_center + 6, 13, x_center + 9, 19), backpack_color)


def draw_scarf(
    draw: ImageDraw.ImageDraw,
    x_center: int,
    scarf_color: Tuple[int, int, int, int],
) -> None:
    """Draw optional scarf."""

    _rect(draw, (x_center - 5, 10, x_center + 5, 11), scarf_color)
    _rect(draw, (x_center + 2, 12, x_center + 3, 16), scarf_color)


# ----------------------------------------------------------------------------
# Generator logic
# ----------------------------------------------------------------------------

def _weighted_choice(
    rng: random.Random,
    values: List[int],
    weights: Tuple[int, ...],
) -> int:
    """Pick one value using integer weights."""

    return rng.choices(values, weights=weights, k=1)[0]


def _resolve_theme(rng: random.Random, theme: str) -> str:
    """Resolve requested theme name to a concrete profile."""

    if theme in THEMES:
        return theme
    return rng.choices(list(THEMES), weights=THEME_MIX_WEIGHTS, k=1)[0]


def _build_theme_palette(
    rng: random.Random,
    profile: ThemeSpec,
) -> Dict[str, Tuple[int, int, int, int]]:
    """Build palette constrained by current theme profile."""

    return {
        "skin": rng.choice(SKIN_TONES),
        "hair": rng.choice(HAIR_COLORS),
        "main": rng.choice(profile["main_palette"]),
        "pants": rng.choice(profile["pants_palette"]),
        "shoes": rng.choice(SHOE_COLORS),
        "hat": rng.choice(profile["hat_palette"]),
        "backpack": rng.choice(profile["backpack_palette"]),
        "scarf": rng.choice(profile["main_palette"]),
    }


def generate_character(
    rng: random.Random | None = None,
    theme: str = "mixed",
) -> Image.Image:
    """Generate one 128x128 RGBA character sprite on transparent background."""

    rng = rng or random.Random()
    selected_theme = _resolve_theme(rng, theme)
    profile = THEME_PROFILES[selected_theme]
    palette = _build_theme_palette(rng, profile)

    base = Image.new("RGBA", (BASE_SIZE, BASE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    cx = BASE_SIZE // 2

    body_style = _weighted_choice(rng, [0, 1, 2], profile["body_weights"])
    arms_style = rng.randint(0, 1)
    leg_style = _weighted_choice(rng, [0, 1, 2], profile["leg_weights"])
    shoe_style = _weighted_choice(rng, [0, 1], profile["shoe_weights"])

    draw_legs(draw, cx, palette["pants"], leg_style)
    draw_shoes(draw, cx, palette["shoes"], shoe_style)
    draw_body(draw, cx, palette["main"], body_style)
    draw_arms(draw, cx, palette["main"], palette["skin"], arms_style)
    draw_head(draw, cx, palette["skin"])

    if rng.random() < profile["hair_prob"]:
        draw_hair(draw, cx, palette["hair"], rng.randint(0, 5))
    if rng.random() < profile["hat_prob"]:
        draw_hat(draw, cx, palette["hat"], rng.randint(0, 5))
    if rng.random() < profile["glasses_prob"]:
        draw_glasses(draw, cx, rng.randint(0, 2))
    if rng.random() < profile["beard_prob"]:
        draw_beard(draw, cx, palette["hair"], rng.randint(0, 3))
    if rng.random() < profile["backpack_prob"]:
        draw_backpack(draw, cx, palette["backpack"], rng.randint(0, 2))
    if rng.random() < profile["scarf_prob"]:
        draw_scarf(draw, cx, palette["scarf"])

    sprite = base.resize((SPRITE_SIZE, SPRITE_SIZE), Image.Resampling.NEAREST)
    return sprite


def generate_waldo_fixed() -> Image.Image:
    """Generate a canonical fixed Waldo sprite with deterministic outfit."""

    base = Image.new("RGBA", (BASE_SIZE, BASE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    cx = BASE_SIZE // 2

    skin = SKIN_TONES[1]
    red = (210, 45, 45, 255)
    white = (245, 245, 245, 255)
    blue = (46, 76, 160, 255)
    brown = (72, 50, 35, 255)

    draw_legs(draw, cx, blue, style=0)
    draw_shoes(draw, cx, brown, style=0)
    draw_body(draw, cx, white, style=2)

    for yy in (12, 14, 16, 18):
        draw.line((cx - 5, yy, cx + 5, yy), fill=red)
    draw_arms(draw, cx, white, skin, style=0)
    draw_head(draw, cx, skin)

    draw_hair(draw, cx, HAIR_COLORS[0], style=0)
    draw_glasses(draw, cx, style=0)
    draw_hat(draw, cx, red, style=0)
    draw.line((cx - 5, 4, cx + 5, 4), fill=white)

    return base.resize((SPRITE_SIZE, SPRITE_SIZE), Image.Resampling.NEAREST)


def generate_dataset(
    n_characters: int = DEFAULT_COUNT,
    output_dir: Path = OUTPUT_DIR,
    seed: int | None = None,
    theme: str = "mixed",
) -> None:
    """Generate fixed Waldo plus procedural characters in assets folders."""

    output_dir.mkdir(parents=True, exist_ok=True)
    WALDO_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    log.info(
        "Generating sprites  n=%d  theme=%s  seed=%s  → %s",
        n_characters, theme, seed, output_dir,
    )

    waldo_image = generate_waldo_fixed()
    waldo_path = WALDO_DIR / "waldo_fixed.png"
    waldo_image.save(waldo_path, format="PNG")
    log.info("Fixed Waldo sprite saved → %s", waldo_path)

    theme_counts: Dict[str, int] = {t: 0 for t in THEMES}

    bar = tqdm(
        range(1, n_characters + 1),
        desc="Sprites",
        unit="sprite",
        ncols=80,
        colour="green",
    )
    for i in bar:
        selected = _resolve_theme(rng, theme)
        theme_counts[selected] += 1
        image = generate_character(rng, theme=selected)
        file_name = f"character_{i:04d}.png"
        image.save(output_dir / file_name, format="PNG")

        if i % 50 == 0:
            bar.set_postfix(**{t[0]: v for t, v in theme_counts.items()})

    log.info(
        "Done — %d sprites saved  (tourist=%d  explorer=%d  casual=%d)",
        n_characters,
        theme_counts.get("tourist", 0),
        theme_counts.get("explorer", 0),
        theme_counts.get("casual", 0),
    )


def _validate_sample(output_dir: Path) -> None:
    sample = output_dir / "character_0001.png"
    if not sample.exists():
        return
    img = Image.open(sample)
    w, h = img.size
    ok = (
        "✓"
        if (w == SPRITE_SIZE and h == SPRITE_SIZE and img.mode == "RGBA")
        else "⚠"
    )
    log.info(
        "Sample check %s  %s | mode=%s | size=%dx%d",
        ok, sample.name, img.mode, w, h,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate retro pixel-art character sprites procedurally.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help="Number of characters to generate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional deterministic seed for reproducible datasets.",
    )
    parser.add_argument(
        "--theme",
        type=str,
        default="mixed",
        choices=["mixed", "tourist", "explorer", "casual"],
        help="Theme profile. 'mixed' samples across all profiles.",
    )
    args = parser.parse_args()

    ensure_output_dir()
    log.info("─" * 55)
    log.info("Where-is-Waldo  —  character sprite generator")
    log.info(
        "count=%d  theme=%s  seed=%s", args.count, args.theme, args.seed,
    )
    log.info("─" * 55)
    generate_dataset(
        n_characters=args.count,
        seed=args.seed,
        theme=args.theme,
    )
    _validate_sample(OUTPUT_DIR)


if __name__ == "__main__":
    main()
