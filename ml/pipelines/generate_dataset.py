"""CLI script to generate synthetic Waldo dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Bootstrap: add project root to sys.path before any imports.
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.utils.logging_utils import get_logger  # noqa: E402
from ml.training.dataset_loader import generate_dataset  # noqa: E402

log = get_logger(__name__)


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Generate Waldo synthetic dataset"
    )
    parser.add_argument(
        "--n-images",
        type=int,
        default=2000,
        help="Number of scenes to generate",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    summary = generate_dataset(n_images=args.n_images, seed=args.seed)
    log.info("Dataset generation complete:")
    for key, value in summary.items():
        log.info("  %-10s %s", key, value)


if __name__ == "__main__":
    main()
