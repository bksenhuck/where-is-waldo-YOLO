"""Bounding box helper utilities for CV and YOLO formats."""

from __future__ import annotations

from typing import Tuple


BBox = Tuple[int, int, int, int]


def clamp_bbox(bbox: BBox, width: int, height: int) -> BBox:
    """Clamp a bbox to image limits."""

    x1, y1, x2, y2 = bbox
    x1 = max(0, min(x1, width - 1))
    x2 = max(0, min(x2, width - 1))
    y1 = max(0, min(y1, height - 1))
    y2 = max(0, min(y2, height - 1))
    if x2 <= x1:
        x2 = min(width - 1, x1 + 1)
    if y2 <= y1:
        y2 = min(height - 1, y1 + 1)
    return x1, y1, x2, y2


def bbox_to_yolo(
    bbox: BBox,
    img_w: int,
    img_h: int,
) -> Tuple[float, float, float, float]:
    """Convert pixel bbox (x1,y1,x2,y2) to normalized YOLO format."""

    x1, y1, x2, y2 = bbox
    bw = x2 - x1
    bh = y2 - y1
    cx = x1 + bw / 2.0
    cy = y1 + bh / 2.0
    return cx / img_w, cy / img_h, bw / img_w, bh / img_h


def yolo_to_bbox(
    xc: float,
    yc: float,
    w: float,
    h: float,
    img_w: int,
    img_h: int,
) -> BBox:
    """Convert normalized YOLO format to pixel bbox (x1,y1,x2,y2)."""

    bw = w * img_w
    bh = h * img_h
    cx = xc * img_w
    cy = yc * img_h
    x1 = int(cx - bw / 2.0)
    y1 = int(cy - bh / 2.0)
    x2 = int(cx + bw / 2.0)
    y2 = int(cy + bh / 2.0)
    return clamp_bbox((x1, y1, x2, y2), img_w, img_h)


def point_in_bbox(x: float, y: float, bbox: BBox) -> bool:
    """Return True when point lies inside bbox."""

    x1, y1, x2, y2 = bbox
    return x1 <= x <= x2 and y1 <= y <= y2


def iou(b1: BBox, b2: BBox) -> float:
    """Compute Intersection over Union between two boxes."""

    x11, y11, x12, y12 = b1
    x21, y21, x22, y22 = b2

    ix1 = max(x11, x21)
    iy1 = max(y11, y21)
    ix2 = min(x12, x22)
    iy2 = min(y12, y22)

    inter_w = max(0, ix2 - ix1)
    inter_h = max(0, iy2 - iy1)
    inter = inter_w * inter_h

    a1 = max(0, (x12 - x11)) * max(0, (y12 - y11))
    a2 = max(0, (x22 - x21)) * max(0, (y22 - y21))
    union = a1 + a2 - inter
    if union <= 0:
        return 0.0
    return inter / union
