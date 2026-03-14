"""ML-specific constants — all tunable ML parameters live here.

Rules:
- YOLO architecture / training hyperparameters → this file
- Scene generation parameters → this file
- Dataset split ratios → this file
- Character sprite parameters → this file
- File paths → backend/utils/config.py (get_paths)
- Server / GCS env vars → config/settings.py
"""
from typing import Dict, Tuple

# ── YOLO model ─────────────────────────────────────────────────────────────────
YOLO_BASE_MODEL_NAME: str = "yolov8n.pt"
YOLO_BASE_MODEL_URL: str = (
    "https://github.com/ultralytics/assets/releases/download/"
    "v8.4.0/yolov8n.pt"
)
YOLO_MODEL_NAME: str = "waldo_yolov8n"   # project / run name used by ultralytics

# ── Scene generation ───────────────────────────────────────────────────────────
SCENE_SIZE: Tuple[int, int] = (640, 640)

DIFFICULTY_TO_COUNT: Dict[str, int] = {
    "easy":   20,
    "medium": 80,
    "hard":   160,
}

# ── Dataset split ──────────────────────────────────────────────────────────────
DATASET_TRAIN_RATIO: float = 0.9   # 90 % train / 10 % val

DATASET_DIFFICULTY_WEIGHTS: Dict[str, float] = {
    "easy":   0.3,
    "medium": 0.4,
    "hard":   0.3,
}

# ── Character sprite generator ─────────────────────────────────────────────────
CHARACTER_BASE_SIZE: int = 32       # pixels before upscale
CHARACTER_SCALE: int = 4            # nearest-neighbor upscale factor → 128 px
CHARACTER_DEFAULT_COUNT: int = 500

# Probability weights for theme selection (tourist / explorer / casual)
CHARACTER_THEME_MIX_WEIGHTS: Tuple[int, int, int] = (35, 25, 40)
