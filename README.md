# Waldo AI Project

Interactive computer vision game inspired by "Where is Waldo", built with synthetic data generation, YOLO training, and a Dash dashboard.

## Features

- Procedural crowded scene generation with a hidden Waldo-like character.
- Automatic synthetic dataset generation in YOLO format.
- YOLOv8 training pipeline using Ultralytics.
- Interactive Dash + Plotly app to compare:
  - Ground truth Waldo location
  - User click guess
  - YOLO prediction

## Architecture

waldo-ai-project/

- README.md
- requirements.txt
- backend/
  - scene_generation/
    - __init__.py
    - backgrounds.py
    - characters.py
    - collision.py
    - generate_scene.py
  - vision/
    - dataset/
      - __init__.py
      - dataset_builder.py
      - dataset_config.yaml
    - training/
      - __init__.py
      - train_yolo.py
    - inference/
      - __init__.py
      - detect_waldo.py
  - utils/
    - __init__.py
    - image_utils.py
    - bbox_utils.py
    - config.py
- frontend/
  - dash_app/
    - app.py
    - layout.py
    - callbacks.py
  - assets/
    - backgrounds/
    - characters/
    - waldo/
  - data/
    - images/
    - labels/
  - models/
  - notebooks/
    - exploration.ipynb
- scripts/
  - generate_dataset.py
  - train_model.py
  - run_app.py

## Installation

1. Create and activate your Python virtual environment.
2. Install dependencies:

pip install -r requirements.txt

## Usage

Generate synthetic dataset:

python model/pipelines/generate_dataset.py

Train model:

python model/pipelines/train_model.py

Run dashboard:

python scripts/run_app.py

## Notes

- If no assets are found in `frontend/assets`, the project generates synthetic backgrounds and character sprites automatically.
- Trained models are saved under `model/models`.
- Dataset files are written under `model/data/images` and `model/data/labels`.
