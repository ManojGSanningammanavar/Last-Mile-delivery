from __future__ import annotations

from pydantic import BaseModel, Field

from src.api.schemas import OrderInput


class AdvancedOrdersBatchRequest(BaseModel):
    orders: list[OrderInput]
    alpha: float = Field(default=0.1, ge=0.01, le=0.3)


class DigitalTwinRequest(BaseModel):
    orders: list[OrderInput]
    alpha: float = Field(default=0.1, ge=0.01, le=0.3)
    horizon_steps: int = Field(default=8, ge=2, le=48)
    random_seed: int = Field(default=42, ge=0, le=999999)
