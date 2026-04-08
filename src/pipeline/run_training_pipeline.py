from __future__ import annotations

from src.ml.train import train_model


def run_training() -> dict:
    return train_model(
        orders_path="data/raw/orders_raw.csv",
        area_risk_path="data/raw/area_risk.csv",
        model_path="models/failure_model.pkl",
        preprocessor_path="models/preprocessor.pkl",
        metadata_path="models/metadata.json",
    )
