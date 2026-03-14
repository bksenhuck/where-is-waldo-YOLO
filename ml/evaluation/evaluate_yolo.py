"""YOLO model evaluation utilities.

Computes mAP and per-class metrics on the validation split.

Usage:
    python -m ml.evaluation.evaluate_yolo
    python -m ml.evaluation.evaluate_yolo --weights path/to/best.pt
"""

from __future__ import annotations

import argparse
from pathlib import Path

from backend.utils.config import get_paths
from backend.utils.logging_utils import get_logger

log = get_logger(__name__)


def evaluate_model(
    weights: str | Path | None = None,
    imgsz: int = 640,
    conf: float = 0.25,
    iou: float = 0.6,
) -> dict:
    """Run YOLO validation and return metrics dictionary.

    Args:
        weights: Path to model weights. Defaults to best trained weights.
        imgsz:   Inference image size.
        conf:    Confidence threshold.
        iou:     IoU threshold for NMS.

    Returns:
        Dictionary with mAP50, mAP50-95, precision, recall.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        raise ImportError("Run: pip install ultralytics")

    paths = get_paths()

    if weights is None:
        candidate = paths.models_dir / "waldo_yolov8n" / "weights" / "best.pt"
        if not candidate.exists():
            log.warning("No trained weights found at %s", candidate)
            return {}
        weights = candidate

    weights = Path(weights)
    if not weights.exists():
        log.error("Weights file not found: %s", weights)
        return {}

    log.info("Evaluating model: %s", weights)
    model = YOLO(str(weights))
    results = model.val(
        data=str(paths.dataset_yaml),
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        verbose=False,
    )

    metrics = {
        "mAP50":    float(results.box.map50),
        "mAP50-95": float(results.box.map),
        "precision": float(results.box.mp),
        "recall":   float(results.box.mr),
    }
    log.info(
        "mAP50=%.4f  mAP50-95=%.4f  P=%.4f  R=%.4f",
        metrics["mAP50"], metrics["mAP50-95"],
        metrics["precision"], metrics["recall"],
    )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate trained Waldo YOLO model."
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="Path to model weights (default: best trained weights).",
    )
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--iou", type=float, default=0.6)
    args = parser.parse_args()

    metrics = evaluate_model(
        weights=args.weights,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
    )
    if metrics:
        for k, v in metrics.items():
            log.info("  %-12s %.4f", k, v)


if __name__ == "__main__":
    main()
