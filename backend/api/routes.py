"""FastAPI routes for the Where is Waldo backend API."""

from __future__ import annotations

import base64
import io
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from backend.security import (
    RATE_LIMIT_DETECT,
    RATE_LIMIT_SCENE,
    limiter,
    require_api_key,
)

router = APIRouter()

# Max base64 payload: ~2.7 MB encoded ≈ 2 MB decoded
_MAX_B64_LEN = 3_000_000


# ── Request / Response models ─────────────────────────────────────────────────

class SceneResponse(BaseModel):
    img_b64: str
    waldo_bbox: List[int]
    width: int
    height: int
    difficulty: str


class DetectRequest(BaseModel):
    img_b64: str = Field(..., max_length=_MAX_B64_LEN)


class Detection(BaseModel):
    bbox: List[int]
    confidence: float


class DetectResponse(BaseModel):
    detections: List[Detection]


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get(
    "/scene",
    response_model=SceneResponse,
    dependencies=[Depends(require_api_key)],
)
@limiter.limit(RATE_LIMIT_SCENE)
def get_scene(
    request: Request,
    difficulty: str = Query("medium", max_length=10),  # noqa: B008
) -> SceneResponse:
    """Generate a Waldo scene and return the image + ground-truth bbox."""
    if difficulty not in ("easy", "medium", "hard"):
        raise HTTPException(
            status_code=422,
            detail="difficulty must be 'easy', 'medium', or 'hard'",
        )

    from ml.data_generation.scene_generator import generate_scene  # lazy

    img, waldo_bbox = generate_scene(difficulty=difficulty)
    w, h = img.size

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return SceneResponse(
        img_b64=img_b64,
        waldo_bbox=list(waldo_bbox),
        width=w,
        height=h,
        difficulty=difficulty,
    )


@router.post(
    "/detect",
    response_model=DetectResponse,
    dependencies=[Depends(require_api_key)],
)
@limiter.limit(RATE_LIMIT_DETECT)
def detect(
    request: Request,
    body: DetectRequest,
) -> DetectResponse:
    """Run YOLO inference on a base64-encoded image and return detections."""
    from PIL import Image
    from ml.models.yolo_detector import detect_waldo  # lazy

    try:
        data = base64.b64decode(body.img_b64)
        img = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid image data.")

    raw = detect_waldo(img)

    return DetectResponse(
        detections=[
            Detection(
                bbox=list(d["bbox"]),
                confidence=float(d["confidence"]),
            )
            for d in raw
        ]
    )


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}
