from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import OrdersBatchRequest, OrdersProcessResponse
from src.api.security import verify_api_key
from src.pipeline.run_pipeline import process_orders
from src.utils.io import read_json

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_api_key)])


@router.post("/process", response_model=OrdersProcessResponse)
def process_orders_route(request: OrdersBatchRequest) -> dict:
    try:
        place_graph = read_json("data/processed/place_graph.json")
        return process_orders(
            orders=[order.model_dump() for order in request.orders],
            model_path="models/failure_model.pkl",
            place_graph_payload=place_graph,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail="missing_resource") from exc
