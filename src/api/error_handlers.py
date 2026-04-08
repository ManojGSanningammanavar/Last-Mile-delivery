from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _payload(code: str, message: str, status: int) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "status": status,
        }
    }


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Request payload validation failed",
                    "status": 422,
                    "issues": exc.errors(),
                }
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        status = int(exc.status_code)
        if status == 404:
            return JSONResponse(status_code=404, content=_payload("not_found", "Route not found", 404))

        if status == 429:
            return JSONResponse(status_code=429, content=_payload("rate_limited", "Too many requests", 429))

        if status == 401:
            return JSONResponse(status_code=401, content=_payload("unauthorized", "Unauthorized", 401))

        if status == 400:
            return JSONResponse(status_code=400, content=_payload("bad_request", "Bad request", 400))

        if status == 503:
            return JSONResponse(status_code=503, content=_payload("service_unavailable", "Service temporarily unavailable", 503))

        return JSONResponse(status_code=status, content=_payload("http_error", "Request failed", status))

    @app.exception_handler(HTTPException)
    async def fastapi_http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        status = int(exc.status_code)
        if status == 404:
            return JSONResponse(status_code=404, content=_payload("not_found", "Route not found", 404))
        if status == 429:
            return JSONResponse(status_code=429, content=_payload("rate_limited", "Too many requests", 429))
        if status == 401:
            return JSONResponse(status_code=401, content=_payload("unauthorized", "Unauthorized", 401))
        if status == 400:
            return JSONResponse(status_code=400, content=_payload("bad_request", "Bad request", 400))
        if status == 503:
            return JSONResponse(status_code=503, content=_payload("service_unavailable", "Service temporarily unavailable", 503))
        return JSONResponse(status_code=status, content=_payload("http_error", "Request failed", status))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=_payload("internal_error", "Unexpected server error", 500),
        )
