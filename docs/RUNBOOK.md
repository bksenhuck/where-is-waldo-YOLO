# Where is Waldo — Runbook

## Overview

Interactive game where users and a YOLO AI compete to find Waldo in procedurally generated crowd scenes.

```
frontend (Dash) → calls backend API → ml/ (YOLO inference / scene generation)
                                    ↑
                          ml/training (offline, not in prod)
```

---

## Prerequisites

```bash
git clone <repo>
cd where-is-waldo-YOLO
cp .env.example .env          # fill in GCS_BUCKET_NAME if deploying
```

### Python environments

| Use case | Command |
|---|---|
| Local development (GPU) | `pip install -r requirements-dev.txt` |
| Production / Cloud Run   | `pip install -r requirements-prod.txt` |
| Core only (no rembg)     | `pip install -r requirements.txt` |

---

## 1 — Generate character sprites

Produces pixel-art PNG sprites into `frontend/assets/characters/` and `frontend/assets/waldo/`.
Run this once before training or before starting the app without pre-built sprites.

```bash
python -m ml.data_generation.character_generator
python -m ml.data_generation.character_generator --count 1000 --theme mixed --seed 42
```

Options:

| Flag | Default | Description |
|---|---|---|
| `--count` | 500 | Number of character sprites |
| `--seed` | None | Reproducibility seed |
| `--theme` | mixed | `tourist` / `explorer` / `casual` / `mixed` |

---

## 2 — Generate training dataset

Builds synthetic Waldo scenes in YOLO format under `data/images/` and `data/labels/`.
Auto-called by `train_model` if the dataset is missing.

```bash
python -m ml.pipelines.generate_dataset
python -m ml.pipelines.generate_dataset --n-images 2000 --seed 42
```

Options:

| Flag | Default | Description |
|---|---|---|
| `--n-images` | 2000 | Total scenes (90% train / 10% val) |
| `--seed` | 42 | Reproducibility seed |

---

## 3 — Train the YOLO model

Trains YOLOv8n on the generated dataset. Downloads base weights automatically on first run.
Best weights land at `data/models/waldo_yolov8n/weights/best.pt`.

```bash
python -m ml.pipelines.train_model
python -m ml.pipelines.train_model --epochs 50 --imgsz 640 --dataset-images 3000
```

Options:

| Flag | Default | Description |
|---|---|---|
| `--epochs` | 30 | Training epochs |
| `--imgsz` | 640 | Image size |
| `--dataset-images` | 2000 | Auto-generate this many images if dataset is empty |
| `--no-auto-dataset` | off | Skip auto-generation |

---

## 4 — Evaluate the model

Runs YOLO validation and prints mAP50 / mAP50-95 / Precision / Recall.

```bash
python -m ml.evaluation.evaluate_yolo
python -m ml.evaluation.evaluate_yolo --weights data/models/waldo_yolov8n/weights/best.pt
```

---

## 5 — Run the application (local)

Starts FastAPI + Dash in a single process.

```bash
python main.py
# or
uvicorn main:app --host 127.0.0.1 --port 8050 --reload
```

Open: [http://localhost:8050](http://localhost:8050)

API docs: [http://localhost:8050/api/docs](http://localhost:8050/api/docs)

### API endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/scene?difficulty=medium` | Generate scene → `{img_b64, waldo_bbox, width, height, difficulty}` |
| `POST` | `/api/detect` | Detect Waldo → `{detections: [{bbox, confidence}]}` |
| `GET` | `/api/health` | Health check |

---

## 6 — Upload artifacts to GCS

Uploads trained weights, assets, and training data to Google Cloud Storage.

```bash
python -m backend.pipelines.deploy.upload_to_gcs
python -m backend.pipelines.deploy.upload_to_gcs --dry-run   # preview only
```

Requires `GCS_BUCKET_NAME` set in `.env`.

---

## 7 — Deploy to Cloud Run

```bash
gcloud builds submit --config cloudbuild.yaml
```

Set `_API_BASE` in `cloudbuild.yaml` to the Cloud Run URL after first deploy.

---

## Typical first-run sequence

```bash
# 1. Install deps
pip install -r requirements-dev.txt

# 2. Generate sprites
python -m ml.data_generation.character_generator --count 500

# 3. Train (auto-generates dataset if missing)
python -m ml.pipelines.train_model --epochs 30

# 4. Evaluate
python -m ml.evaluation.evaluate_yolo

# 5. Run app
python main.py
```

---

## Config reference

| File | Purpose |
|---|---|
| `config/settings.py` | Server (PORT, DEBUG, API_BASE) + GCS env vars |
| `config/ml_config.py` | ML constants: YOLO model name, scene size, difficulty counts, dataset split |
| `backend/utils/config.py` | `get_paths()` — single source of truth for all file system paths |

### Key paths (from `get_paths()`)

| Field | Default location |
|---|---|
| `data_dir` | `data/` |
| `images_dir` | `data/images/` |
| `labels_dir` | `data/labels/` |
| `models_dir` | `data/models/` |
| `assets_dir` | `frontend/assets/` |
| `dataset_yaml` | `ml/training/dataset_config.yaml` |

---

## Difficulty levels

| Difficulty | Characters in scene |
|---|---|
| Easy | 20 |
| Medium | 80 |
| Hard | 160 |

Configured in `config/ml_config.py` → `DIFFICULTY_TO_COUNT`.
