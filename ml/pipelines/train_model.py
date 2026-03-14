"""CLI script for training YOLO model."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Bootstrap: add project root to sys.path before any imports.
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.utils.logging_utils import get_logger  # noqa: E402
from ml.training.train_yolo import train_model  # noqa: E402

log = get_logger(__name__)


def main() -> None:

    parser = argparse.ArgumentParser(description="Train Waldo YOLO model")
    parser.add_argument(
        "--epochs",
        type=int,
        default=30,
        help="Training epochs",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument(
        "--dataset-images",
        type=int,
        default=2000,
        help="Dataset size used when auto-generating missing data.",
    )
    parser.add_argument(
        "--no-auto-dataset",
        action="store_true",
        help="Disable automatic dataset generation when data folder is empty.",
    )
    args = parser.parse_args()

    best = train_model(
        epochs=args.epochs,
        imgsz=args.imgsz,
        auto_generate_dataset=not args.no_auto_dataset,
        dataset_images=args.dataset_images,
    )
    log.info("Training complete. Best model: %s", best)


if __name__ == "__main__":
    main()
