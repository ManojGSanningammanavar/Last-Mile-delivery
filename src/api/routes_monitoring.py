from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from src.api.security import verify_api_key
from src.db.repository import prediction_monitoring_summary
from src.geo.geocoder import geocode_enrichment_stats
from src.utils.io import read_json

router = APIRouter(prefix="/monitoring", tags=["monitoring"], dependencies=[Depends(verify_api_key)])


@router.get("/summary")
def monitoring_summary(window_hours: int = 24) -> dict:
    try:
        metadata = read_json("models/metadata.json")
    except Exception:
        metadata = {}

    return {
        "model": {
            "name": str(metadata.get("model_name", "unknown")),
            "f1": float(metadata.get("f1", 0.0) or 0.0),
            "roc_auc": float(metadata.get("roc_auc", 0.0) or 0.0),
            "rows": int(metadata.get("rows", 0) or 0),
        },
        "predictions": prediction_monitoring_summary(window_hours=window_hours),
        "geocode_enrichment": geocode_enrichment_stats(),
    }
