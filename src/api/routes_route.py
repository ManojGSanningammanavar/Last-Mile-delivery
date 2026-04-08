from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.schemas import CounterfactualRequest
from src.api.security import verify_api_key
from src.counterfactual.simulator import simulate_interventions

router = APIRouter(prefix="/counterfactual", tags=["counterfactual"], dependencies=[Depends(verify_api_key)])


@router.post("/simulate")
def simulate_route(request: CounterfactualRequest) -> dict:
    return simulate_interventions(request.failure_probability, request.time_slot)
