from __future__ import annotations

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from src.address.confidence import address_confidence
from src.address.parser import parse_address
from src.advanced.causal_uplift import recommend_causal_action
from src.advanced.conformal import annotate_probabilities_with_uncertainty
from src.api.schemas_advanced import AdvancedOrdersBatchRequest, DigitalTwinRequest
from src.api.security import verify_api_key
from src.digital_twin.simulator import run_dispatch_digital_twin
from src.geo.geocoder import geocode_address
from src.geo.validator import validate_geo
from src.ml.features import FEATURE_CATEGORICAL, FEATURE_NUMERIC, build_inference_feature_frame
from src.ml.predict import predict_failure
from src.recommendation.action_engine import recommend_action

router = APIRouter(prefix="/advanced", tags=["advanced"], dependencies=[Depends(verify_api_key)])


def _predict_orders(orders: list) -> list[dict]:
    rows: list[dict] = []
    for order in orders:
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

    merged = model_df.copy()
    merged["failure_probability"] = pred_df["failure_probability"]
    merged["risk_label"] = pred_df["risk_label"]
    merged["recommended_action_rule_based"] = merged.apply(
        lambda row: recommend_action(float(row["failure_probability"]), float(row["address_confidence"])), axis=1
    )
    return merged.to_dict(orient="records")


@router.post("/uncertainty")
def uncertainty_route(request: AdvancedOrdersBatchRequest) -> dict:
    predicted = _predict_orders(request.orders)
    with_uncertainty = annotate_probabilities_with_uncertainty(predicted, alpha=request.alpha)
    return {
        "calibration": with_uncertainty["calibration"],
        "predictions": with_uncertainty["records"],
    }


@router.post("/causal-action")
def causal_action_route(request: AdvancedOrdersBatchRequest) -> dict:
    predicted = _predict_orders(request.orders)
    uncertainty = annotate_probabilities_with_uncertainty(predicted, alpha=request.alpha)

    out: list[dict] = []
    for row in uncertainty["records"]:
        causal = recommend_causal_action(float(row["failure_probability"]), row)
        enriched = dict(row)
        enriched["causal_policy"] = causal
        out.append(enriched)

    return {
        "calibration": uncertainty["calibration"],
        "predictions": out,
    }


@router.post("/digital-twin")
def digital_twin_route(request: DigitalTwinRequest) -> dict:
    predicted = _predict_orders(request.orders)
    uncertainty = annotate_probabilities_with_uncertainty(predicted, alpha=request.alpha)

    sim = run_dispatch_digital_twin(
        predicted_orders=uncertainty["records"],
        horizon_steps=request.horizon_steps,
        seed=request.random_seed,
    )

    return {
        "calibration": uncertainty["calibration"],
        "orders": uncertainty["records"],
        "digital_twin": sim,
    }
