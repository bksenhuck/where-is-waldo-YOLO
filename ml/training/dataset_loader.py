"""Synthetic dataset builder producing images and YOLO labels."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, Tuple

from tqdm import tqdm

from ml.data_generation.scene_generator import generate_scene
from backend.utils.bbox_utils import bbox_to_yolo
from backend.utils.config import get_paths, write_dataset_yaml
from backend.utils.image_utils import ensure_dir
from backend.utils.logging_utils import get_logger
from config.ml_config import (
    DATASET_DIFFICULTY_WEIGHTS,
    DATASET_TRAIN_RATIO,
    DIFFICULTY_TO_COUNT,
)

log = get_logger(__name__)


def _sample_difficulty(rng: random.Random) -> str:
    levels = list(DATASET_DIFFICULTY_WEIGHTS.keys())
    weights = list(DATASET_DIFFICULTY_WEIGHTS.values())
    return rng.choices(levels, weights=weights, k=1)[0]


def _image_label_paths(split: str, index: int) -> Tuple[Path, Path]:
    paths = get_paths()
    image_path = paths.images_dir / split / f"scene_{index:06d}.png"
    label_path = paths.labels_dir / split / f"scene_{index:06d}.txt"
    return image_path, label_path


def generate_dataset(n_images: int = 2000, seed: int = 42) -> Dict[str, int]:
    """Generate synthetic dataset in YOLO format.

    Args:
        n_images: Number of images to generate.
        seed:     Reproducibility seed.

    Returns:
        Summary dictionary with split counts.
    """
    paths = get_paths()
    rng = random.Random(seed)

    log.info(
        "Starting dataset generation  n_images=%d  seed=%d", n_images, seed,
    )

    for subdir in ("train", "val"):
        ensure_dir(paths.images_dir / subdir)
        ensure_dir(paths.labels_dir / subdir)
    write_dataset_yaml(paths.dataset_yaml, paths.data_dir)
    log.debug("Dataset YAML written → %s", paths.dataset_yaml)

    train_count = int(n_images * DATASET_TRAIN_RATIO)
    val_count = n_images - train_count
    counters: Dict[str, int] = {"easy": 0, "medium": 0, "hard": 0}

    bar = tqdm(
        range(n_images),
        desc="Generating scenes",
        unit="img",
        ncols=80,
        colour="cyan",
    )

    for idx in bar:
        split = "train" if idx < train_count else "val"
        difficulty = _sample_difficulty(rng)
        counters[difficulty] += 1

        image, waldo_bbox = generate_scene(
            num_people=DIFFICULTY_TO_COUNT[difficulty],
            difficulty=difficulty,
            seed=rng.randint(0, 10_000_000),
        )
        img_w, img_h = image.size
        x_center, y_center, width, height = bbox_to_yolo(
            waldo_bbox, img_w, img_h,
        )

        image_path, label_path = _image_label_paths(split=split, index=idx)
        image.save(image_path)
        label_path.write_text(
            f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n",
            encoding="utf-8",
        )

        if idx % 100 == 0 and idx > 0:
            bar.set_postfix(
                split=split,
                easy=counters["easy"],
                medium=counters["medium"],
                hard=counters["hard"],
            )

    summary = {
        "total": n_images,
        "train": train_count,
        "val": val_count,
        **counters,
    }
    log.info(
        "Dataset complete — total=%d  train=%d  val=%d  "
        "(easy=%d  medium=%d  hard=%d)",
        summary["total"], summary["train"], summary["val"],
        summary["easy"], summary["medium"], summary["hard"],
    )
    return summary
