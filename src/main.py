from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.error_handlers import register_error_handlers
from src.api.security import enforce_rate_limit
from src.api.routes_health import router as health_router
from src.api.routes_advanced import router as advanced_router
from src.api.routes_orders import router as orders_router
from src.api.routes_predict import router as predict_router
from src.api.routes_monitoring import router as monitoring_router
from src.api.routes_route import router as counterfactual_router
from src.api.routes_route_optimize import router as route_router
from src.db.migrations import apply_migrations
from src.settings import get_allowed_origins, get_env_settings

settings = get_env_settings()


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    apply_migrations()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=app_lifespan)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    try:
        enforce_rate_limit(request)
    except HTTPException as exc:
        if int(exc.status_code) == 429:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "rate_limited",
                        "message": "Too many requests",
                        "status": 429,
                    }
                },
            )
        raise
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health_router)
app.include_router(orders_router)
app.include_router(predict_router)
app.include_router(monitoring_router)
app.include_router(route_router)
app.include_router(counterfactual_router)
app.include_router(advanced_router)

register_error_handlers(app)

frontend_path = Path("frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/app")
def app_ui() -> FileResponse:
    return FileResponse(frontend_path / "index.html")


@app.get("/")
def root() -> dict:
    return {
        "message": "Smart Last-Mile Delivery System API",
        "docs": "/docs",
        "dashboard": "/app",
    }
