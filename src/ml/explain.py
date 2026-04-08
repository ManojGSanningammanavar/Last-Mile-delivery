from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


def top_reasons(row: dict) -> list[str]:
    reasons: list[str] = []
    if float(row.get("address_confidence", 1.0)) < 0.55:
        reasons.append("low_address_confidence")
    if float(row.get("geo_confidence", 1.0)) < 0.55:
        reasons.append("low_geo_confidence")
    if float(row.get("past_failures", 0)) >= 2:
        reasons.append("historical_failures")
    if float(row.get("distance_km", 0)) >= 10:
        reasons.append("long_distance")
    return reasons[:3]


def explain_prediction(features_df: pd.DataFrame, model_path: str, top_n: int = 3) -> list[dict]:
    model_file = Path(model_path)
    if not model_file.exists():
        return []

    pipeline = joblib.load(model_file)
    preprocessor = pipeline.named_steps.get("preprocessor")
    estimator = pipeline.named_steps.get("model")

    if preprocessor is None or estimator is None:
        return []
    if not hasattr(estimator, "feature_importances_"):
        return []

    names = preprocessor.get_feature_names_out()
    scores = estimator.feature_importances_
    ranked = sorted(zip(names, scores), key=lambda x: float(x[1]), reverse=True)[:top_n]
    out: list[dict] = []
    for name, score in ranked:
        out.append(
            {
                "feature": str(name).replace("num__", "").replace("cat__", ""),
                "importance": round(float(score), 4),
            }
        )
    return out
