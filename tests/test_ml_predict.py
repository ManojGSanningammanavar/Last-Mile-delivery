from pathlib import Path

import pandas as pd

from src.ml.predict import predict_failure
from src.ml.train import train_model


def test_predict_output_shape(tmp_path: Path) -> None:
    model_path = tmp_path / "m.pkl"
    prep_path = tmp_path / "p.pkl"
    meta_path = tmp_path / "meta.json"

    train_model(
        orders_path="data/raw/orders_raw.csv",
        area_risk_path="data/raw/area_risk.csv",
        model_path=str(model_path),
        preprocessor_path=str(prep_path),
        metadata_path=str(meta_path),
    )

    df = pd.DataFrame(
        {
            "address_confidence": [0.7],
            "geo_confidence": [0.8],
            "past_failures": [1],
            "distance_km": [6.5],
            "area_risk_score": [0.3],
            "time_slot": ["evening"],
            "city": ["Bengaluru"],
        }
    )
    out = predict_failure(df, str(model_path))
    assert "failure_probability" in out.columns
