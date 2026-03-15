"""CLI script to generate Waldo and character sprites."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Bootstrap: add project root to sys.path before any imports.
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.utils.logging_utils import get_logger  # noqa: E402
from ml.data_generation.character_generator import (  # noqa: E402
    generate_dataset,
    OUTPUT_DIR,
)

log = get_logger(__name__)


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Generate Waldo and crowd character sprites"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=500,
        help="Number of character sprites to generate",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional deterministic seed",
    )
    parser.add_argument(
        "--theme",
        type=str,
        default="mixed",
        choices=["mixed", "tourist", "explorer", "casual"],
        help="Theme profile for generated characters",
    )
    args = parser.parse_args()

    generate_dataset(
        n_characters=args.count,
        output_dir=OUTPUT_DIR,
        seed=args.seed,
        theme=args.theme,
    )


if __name__ == "__main__":
    main()
