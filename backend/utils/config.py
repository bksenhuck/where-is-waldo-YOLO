"""Project-wide configuration and canonical path helpers."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

# Re-export ML constants so existing importers need no changes
from config.ml_config import DIFFICULTY_TO_COUNT, SCENE_SIZE  # noqa: F401


@dataclass(frozen=True)
class ProjectPaths:
    """Container for frequently used absolute project paths."""

    root_dir: Path
    backend_dir: Path
    frontend_dir: Path
    ml_dir: Path
    assets_dir: Path
    backgrounds_dir: Path
    characters_dir: Path
    waldo_dir: Path
    data_dir: Path
    images_dir: Path
    labels_dir: Path
    models_dir: Path
    notebooks_dir: Path
    dataset_yaml: Path


def get_paths() -> ProjectPaths:
    """Return canonical project paths based on this module location."""

    root_dir = Path(__file__).resolve().parents[2]
    backend_dir = root_dir / "backend"
    frontend_dir = root_dir / "frontend"
    ml_dir = root_dir / "ml"
    assets_dir = frontend_dir / "assets"
    backgrounds_dir = assets_dir / "backgrounds"
    characters_dir = assets_dir / "characters"
    waldo_dir = assets_dir / "waldo"
    data_dir = root_dir / "data"
    images_dir = data_dir / "images"
    labels_dir = data_dir / "labels"
    models_dir = data_dir / "models"
    notebooks_dir = frontend_dir / "notebooks"
    dataset_yaml = ml_dir / "training" / "dataset_config.yaml"

    return ProjectPaths(
        root_dir=root_dir,
        backend_dir=backend_dir,
        frontend_dir=frontend_dir,
        ml_dir=ml_dir,
        assets_dir=assets_dir,
        backgrounds_dir=backgrounds_dir,
        characters_dir=characters_dir,
        waldo_dir=waldo_dir,
        data_dir=data_dir,
        images_dir=images_dir,
        labels_dir=labels_dir,
        models_dir=models_dir,
        notebooks_dir=notebooks_dir,
        dataset_yaml=dataset_yaml,
    )


def bootstrap_project_root() -> Path:
    """
    Add the project root to sys.path and return it.

    Call this at the top of any standalone script that lives inside a
    sub-package (e.g. model/pipelines/) before importing from ``backend``.
    Safe to call multiple times.
    """
    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


def write_dataset_yaml(dataset_yaml: Path, data_root: Path) -> None:
    """
    Write (or overwrite) the YOLO dataset YAML file.

    Shared by ``dataset_builder`` and ``train_yolo`` to avoid duplication.

    Parameters
    ----------
    dataset_yaml:  Destination path for the YAML file.
    data_root:     Absolute path that YOLO uses as the dataset root
                   (``path`` key in the YAML).
    """
    import yaml  # local import — yaml only needed here

    content = {
        "path": str(data_root.resolve()),
        "train": "images/train",
        "val": "images/val",
        "names": ["waldo"],
        "nc": 1,
    }
    dataset_yaml.parent.mkdir(parents=True, exist_ok=True)
    dataset_yaml.write_text(yaml.safe_dump(content, sort_keys=False), encoding="utf-8")
