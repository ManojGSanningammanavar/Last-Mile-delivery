from __future__ import annotations

from pathlib import Path

import joblib

from src.settings import get_env_settings


def missing_model_artifacts() -> list[str]:
    settings = get_env_settings()
    required = [
        settings.model_path,
        settings.preprocessor_path,
        settings.metadata_path,
    ]
    return [path for path in required if not Path(path).exists()]


def model_ready() -> bool:
    return len(missing_model_artifacts()) == 0


def artifact_load_errors() -> list[str]:
    settings = get_env_settings()
    errors: list[str] = []
    for path in [settings.model_path, settings.preprocessor_path]:
        if not Path(path).exists():
            continue
        try:
            joblib.load(path)
        except Exception:
            errors.append(path)
    return errors
