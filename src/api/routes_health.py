from __future__ import annotations

from fastapi import APIRouter
from fastapi import Response
from pydantic import BaseModel, Field

from src.ml.artifacts import artifact_load_errors, missing_model_artifacts

router = APIRouter(prefix="", tags=["health"])


class ClientTelemetryEvent(BaseModel):
    level: str = Field(default="error", max_length=16)
    message: str = Field(min_length=1, max_length=512)
    context: dict = Field(default_factory=dict)


@router.get("/health")
def health(response: Response) -> dict:
    missing = missing_model_artifacts()
    load_errors = artifact_load_errors()
    if missing or load_errors:
        response.status_code = 503
        return {
            "status": "degraded",
            "missing_artifacts": missing,
            "unreadable_artifacts": load_errors,
        }
    return {"status": "ok"}


@router.post("/health/client-log")
def client_log(event: ClientTelemetryEvent) -> dict:
    # Keep logging lightweight for local deployment while preserving diagnostics.
    print(f"[client:{event.level}] {event.message} | context={event.context}")
    return {"status": "accepted"}
