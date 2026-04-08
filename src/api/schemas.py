from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class OrderInput(BaseModel):
    order_id: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    order_datetime: str = "2026-03-10 09:00:00"
    address_raw: str = Field(min_length=6, max_length=512)
    city: str = Field(default="Bengaluru", min_length=2, max_length=64)
    pincode: str = Field(default="", max_length=12)
    customer_id: str = ""
    past_failures: int = 0
    distance_km: float = Field(default=0.0, ge=0.0)
    time_slot: str = "afternoon"
    area_risk_score: float = Field(default=0.25, ge=0.0, le=1.0)


class OrdersBatchRequest(BaseModel):
    orders: list[OrderInput]


class CounterfactualRequest(BaseModel):
    failure_probability: float = Field(ge=0.0, le=1.0)
    time_slot: str


class RouteCoordinate(BaseModel):
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)


class RoadPathRequest(BaseModel):
    coordinates: list[RouteCoordinate] = Field(min_length=2, max_length=64)


class PredictionRecord(BaseModel):
    order_id: str
    area: str
    landmark: str
    geo_warnings: list[str]
    failure_probability: float
    risk_label: str
    recommended_action: str
    reasons: list[str]


class PredictFailureResponse(BaseModel):
    predictions: list[PredictionRecord]


class OrdersProcessResponse(BaseModel):
    orders: list[dict[str, Any]]
    route: dict[str, Any]
    route_options: list[dict[str, Any]]
    route_selected_key: str
    impact_metrics: dict[str, Any]
    impact_simulation: dict[str, Any]
