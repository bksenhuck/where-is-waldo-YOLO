"""End-to-end pipeline: sprites → dataset → train → evaluate.

Steps (all optional via --skip-* flags):
  1. generate_characters  — produce Waldo + crowd sprites in data/assets/
  2. generate_dataset     — render synthetic scenes + YOLO labels in data/
  3. train                — fine-tune YOLOv8 on the dataset
  4. evaluate             — compute mAP / metrics on the val split

Usage:
    python -m ml.pipelines.run_pipeline
    python -m ml.pipelines.run_pipeline --epochs 50 --n-images 5000
    python -m ml.pipelines.run_pipeline --skip-sprites --skip-dataset
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Bootstrap: add project root to sys.path before any imports.
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.utils.logging_utils import get_logger  # noqa: E402

log = get_logger(__name__)


def _hms(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _step(name: str) -> None:
    log.info("=" * 55)
    log.info("STEP: %s", name)
    log.info("=" * 55)


def run(
    n_characters: int = 500,
    character_seed: int | None = None,
    n_images: int = 2000,
    dataset_seed: int = 42,
    epochs: int = 30,
    imgsz: int = 640,
    skip_sprites: bool = False,
    skip_dataset: bool = False,
    skip_train: bool = False,
    skip_evaluate: bool = False,
) -> None:
    pipeline_start = time.time()

    # ── Step 1: generate sprites ───────────────────────────────────────────────
    if not skip_sprites:
        _step("1/4  Generate sprites")
        t0 = time.time()
        from ml.data_generation.character_generator import (
            generate_dataset as gen_sprites,
            OUTPUT_DIR,
        )
        gen_sprites(n_characters=n_characters, seed=character_seed)
        log.info("Sprites done in %s", _hms(time.time() - t0))
    else:
        log.info("Step 1/4 skipped (--skip-sprites)")

    # ── Step 2: generate dataset ───────────────────────────────────────────────
    if not skip_dataset:
        _step("2/4  Generate dataset")
        t0 = time.time()
        from ml.training.dataset_loader import generate_dataset
        summary = generate_dataset(n_images=n_images, seed=dataset_seed)
        log.info(
            "Dataset done in %s  (train=%d  val=%d)",
            _hms(time.time() - t0), summary["train"], summary["val"],
        )
    else:
        log.info("Step 2/4 skipped (--skip-dataset)")

    # ── Step 3: train ──────────────────────────────────────────────────────────
    best_weights: Path | None = None
    if not skip_train:
        _step("3/4  Train YOLO")
        t0 = time.time()
        from ml.training.train_yolo import train_model
        best_weights = train_model(
            epochs=epochs,
            imgsz=imgsz,
            auto_generate_dataset=False,
        )
        log.info("Training done in %s  → %s", _hms(time.time() - t0), best_weights)
    else:
        log.info("Step 3/4 skipped (--skip-train)")

    # ── Step 4: evaluate ───────────────────────────────────────────────────────
    if not skip_evaluate:
        _step("4/4  Evaluate")
        t0 = time.time()
        from ml.evaluation.evaluate_yolo import evaluate_model
        metrics = evaluate_model(weights=best_weights, imgsz=imgsz)
        log.info("Evaluation done in %s", _hms(time.time() - t0))
        for k, v in metrics.items():
            log.info("  %-20s %s", k, v)
    else:
        log.info("Step 4/4 skipped (--skip-evaluate)")

    log.info("=" * 55)
    log.info("Pipeline complete in %s", _hms(time.time() - pipeline_start))
    log.info("=" * 55)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="End-to-end Waldo pipeline: sprites → dataset → train → evaluate",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Sprite generation
    parser.add_argument("--n-characters", type=int, default=500,
                        help="Number of crowd sprites to generate")
    parser.add_argument("--character-seed", type=int, default=None,
                        help="Seed for sprite generation")

    # Dataset generation
    parser.add_argument("--n-images", type=int, default=2000,
                        help="Number of training scenes to generate")
    parser.add_argument("--dataset-seed", type=int, default=42,
                        help="Seed for dataset generation")

    # Training
    parser.add_argument("--epochs", type=int, default=30,
                        help="YOLO training epochs")
    parser.add_argument("--imgsz", type=int, default=640,
                        help="Image size for training and evaluation")

    # Skip flags
    parser.add_argument("--skip-sprites", action="store_true",
                        help="Skip sprite generation (use existing assets)")
    parser.add_argument("--skip-dataset", action="store_true",
                        help="Skip dataset generation (use existing data/)")
    parser.add_argument("--skip-train", action="store_true",
                        help="Skip model training")
    parser.add_argument("--skip-evaluate", action="store_true",
                        help="Skip evaluation step")

    args = parser.parse_args()

    run(
        n_characters=args.n_characters,
        character_seed=args.character_seed,
        n_images=args.n_images,
        dataset_seed=args.dataset_seed,
        epochs=args.epochs,
        imgsz=args.imgsz,
        skip_sprites=args.skip_sprites,
        skip_dataset=args.skip_dataset,
        skip_train=args.skip_train,
        skip_evaluate=args.skip_evaluate,
    )


if __name__ == "__main__":
    main()
