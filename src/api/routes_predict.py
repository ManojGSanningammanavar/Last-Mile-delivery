from __future__ import annotations

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from src.address.confidence import address_confidence
from src.address.parser import parse_address
from src.geo.geocoder import geocode_address
from src.geo.validator import validate_geo
from src.api.schemas import OrdersBatchRequest, PredictFailureResponse
from src.db.repository import save_prediction
from src.api.security import verify_api_key
from src.ml.explain import top_reasons
from src.ml.features import FEATURE_CATEGORICAL, FEATURE_NUMERIC, build_inference_feature_frame
from src.ml.predict import predict_failure
from src.recommendation.action_engine import recommend_action

router = APIRouter(prefix="/predict", tags=["predict"], dependencies=[Depends(verify_api_key)])


@router.post("/failure", response_model=PredictFailureResponse)
def predict_failure_route(request: OrdersBatchRequest) -> dict:
    rows: list[dict] = []
    for order in request.orders:
        parsed = parse_address(order.address_raw, order.pincode)
        addr_conf = address_confidence(parsed)
        lat, lon, geo_base_conf = geocode_address(
            parsed.area,
            order.city,
            raw_address=order.address_raw,
            pincode=parsed.pincode,
        )
        geo = validate_geo(lat, lon, geo_base_conf, parsed.pincode, order.city)

        rows.append(
            {
                "order_id": order.order_id,
                "order_datetime": order.order_datetime,
                "address_confidence": addr_conf,
                "geo_confidence": geo.geo_confidence,
                "past_failures": order.past_failures,
                "distance_km": order.distance_km,
                "area_risk_score": order.area_risk_score,
                "time_slot": order.time_slot,
                "city": order.city,
                "area": parsed.area,
                "landmark": parsed.landmark,
                "geo_warnings": geo.warnings,
            }
        )

    model_df = pd.DataFrame(rows)
    feature_df = build_inference_feature_frame(model_df)
    model_input = feature_df[FEATURE_NUMERIC + FEATURE_CATEGORICAL]
    try:
        pred_df = predict_failure(model_input, "models/failure_model.pkl", features_ready=True)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="prediction_unavailable") from exc

    merged = model_df[["order_id", "area", "landmark", "geo_warnings", "address_confidence"]].copy()
    merged["failure_probability"] = pred_df["failure_probability"]
    merged["risk_label"] = pred_df["risk_label"]
    merged["recommended_action"] = merged.apply(
        lambda row: recommend_action(float(row["failure_probability"]), float(row["address_confidence"])), axis=1
    )
    merged["reasons"] = merged.apply(lambda row: top_reasons(row.to_dict()), axis=1)

    for record in merged[["order_id", "failure_probability", "risk_label"]].to_dict(orient="records"):
        save_prediction(
            order_id=str(record["order_id"]),
            failure_probability=float(record["failure_probability"]),
            risk_label=str(record["risk_label"]),
        )

    merged = merged.drop(columns=["address_confidence"])
    return {"predictions": merged.to_dict(orient="records")}
