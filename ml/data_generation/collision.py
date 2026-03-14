"""Collision checks for sprite placement."""

from __future__ import annotations

from typing import Iterable

from backend.utils.bbox_utils import BBox


def overlap_area(a: BBox, b: BBox) -> int:
    """Compute overlap area in pixels between two bboxes."""

    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    x_left = max(ax1, bx1)
    y_top = max(ay1, by1)
    x_right = min(ax2, bx2)
    y_bottom = min(ay2, by2)
    if x_right <= x_left or y_bottom <= y_top:
        return 0
    return (x_right - x_left) * (y_bottom - y_top)


def area(box: BBox) -> int:
    """Compute area for a bbox."""

    x1, y1, x2, y2 = box
    return max(0, x2 - x1) * max(0, y2 - y1)


def can_place_bbox(
    candidate: BBox,
    existing: Iterable[BBox],
    max_overlap_ratio: float = 0.35,
) -> bool:
    """Check whether candidate can be placed without excessive overlap."""

    candidate_area = area(candidate)
    if candidate_area == 0:
        return False

    for current in existing:
        overlap = overlap_area(candidate, current)
        if overlap == 0:
            continue
        if overlap / float(candidate_area) > max_overlap_ratio:
            return False
    return True
