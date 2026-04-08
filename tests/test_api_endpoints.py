from fastapi.testclient import TestClient
from types import SimpleNamespace

from src.main import app
import src.api.routes_advanced as routes_advanced
import src.api.security as api_security


client = TestClient(app)


SAMPLE_ORDER = {
    "order_id": "ORD_API_001",
    "order_datetime": "2026-03-18 11:30:00",
    "address_raw": "Near temple 3rd cross BTM Layout Bengaluru",
    "city": "Bengaluru",
    "pincode": "560076",
    "past_failures": 1,
    "distance_km": 5.4,
    "time_slot": "evening",
    "area_risk_score": 0.3,
}


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_predict_endpoint_shape() -> None:
    response = client.post("/predict/failure", json={"orders": [SAMPLE_ORDER]})
    assert response.status_code == 200
    body = response.json()
    assert "predictions" in body
    assert len(body["predictions"]) == 1
    first = body["predictions"][0]
    assert "failure_probability" in first
    assert "risk_label" in first


def test_route_optimize_endpoint_shape() -> None:
    response = client.post("/route/optimize", json={"orders": [SAMPLE_ORDER]})
    assert response.status_code == 200
    body = response.json()
    assert "route_selected_key" in body
    assert "route_options" in body
    assert len(body["route_options"]) == 3
    assert "sequence_order_ids" in body
    assert "distance_km" in body
    assert "geo_notes" in body
    assert "traffic_signal" in body
    assert "traffic_level" in body["traffic_signal"]
    assert len(body["sequence_order_ids"]) >= 2
    assert len(body["route_options"]) == 3
    for option in body["route_options"]:
        assert "traffic_signal" in option
        assert "traffic_level" in option["traffic_signal"]


def test_process_orders_endpoint_shape() -> None:
    response = client.post("/orders/process", json={"orders": [SAMPLE_ORDER]})
    assert response.status_code == 200
    body = response.json()
    assert "orders" in body
    assert "route" in body
    assert len(body["orders"]) == 1
    assert "weather_signal" in body["orders"][0]
    assert "traffic_signal" in body["route"]


def test_monitoring_summary_endpoint_shape() -> None:
    response = client.get("/monitoring/summary")
    assert response.status_code == 200
    body = response.json()
    assert "model" in body
    assert "predictions" in body
    assert "geocode_enrichment" in body


def test_advanced_uncertainty_endpoint_shape() -> None:
    response = client.post("/advanced/uncertainty", json={"orders": [SAMPLE_ORDER], "alpha": 0.1})
    assert response.status_code == 200
    body = response.json()
    assert "calibration" in body
    assert "predictions" in body
    assert len(body["predictions"]) == 1
    assert "risk_band" in body["predictions"][0]


def test_advanced_causal_action_endpoint_shape() -> None:
    response = client.post("/advanced/causal-action", json={"orders": [SAMPLE_ORDER], "alpha": 0.1})
    assert response.status_code == 200
    body = response.json()
    assert "calibration" in body
    assert "predictions" in body
    assert len(body["predictions"]) == 1
    assert "causal_policy" in body["predictions"][0]


def test_advanced_digital_twin_endpoint_shape() -> None:
    response = client.post(
        "/advanced/digital-twin",
        json={"orders": [SAMPLE_ORDER], "alpha": 0.1, "horizon_steps": 8, "random_seed": 42},
    )
    assert response.status_code == 200
    body = response.json()
    assert "calibration" in body
    assert "orders" in body
    assert "digital_twin" in body
    assert "summary" in body["digital_twin"]
    assert "orders_processed" in body["digital_twin"]["summary"]
    assert "orders_pending" in body["digital_twin"]["summary"]


def test_advanced_endpoint_returns_503_when_model_unavailable(monkeypatch) -> None:
    def _raise(*args, **kwargs):
        raise FileNotFoundError("model missing")

    monkeypatch.setattr(routes_advanced, "predict_failure", _raise)
    response = client.post("/advanced/uncertainty", json={"orders": [SAMPLE_ORDER], "alpha": 0.1})
    assert response.status_code == 503
    assert response.json().get("error", {}).get("code") == "service_unavailable"


def test_unknown_route_uses_standard_error_envelope() -> None:
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    body = response.json()
    assert body.get("error", {}).get("code") == "not_found"


def test_invalid_order_payload_returns_422_with_issues() -> None:
    bad_order = dict(SAMPLE_ORDER)
    bad_order["order_id"] = "x"
    response = client.post("/predict/failure", json={"orders": [bad_order]})
    assert response.status_code == 422
    body = response.json()
    assert body.get("error", {}).get("code") == "validation_error"
    assert isinstance(body.get("error", {}).get("issues"), list)


def test_auth_guard_rejects_missing_api_key_when_enabled(monkeypatch) -> None:
    monkeypatch.setattr(api_security, "is_rate_limit_enabled", lambda: False)
    monkeypatch.setattr(api_security, "is_auth_required", lambda: True)
    monkeypatch.setattr(api_security, "get_env_settings", lambda: SimpleNamespace(api_key="expected-key"))

    response = client.post("/predict/failure", json={"orders": [SAMPLE_ORDER]})
    assert response.status_code == 401
    assert response.json().get("error", {}).get("code") == "unauthorized"


def test_rate_limit_returns_429_when_threshold_exceeded(monkeypatch) -> None:
    api_security.RATE_STATE.hits.clear()
    monkeypatch.setattr(api_security, "is_rate_limit_enabled", lambda: True)
    monkeypatch.setattr(api_security, "is_auth_required", lambda: False)
    monkeypatch.setattr(
        api_security,
        "get_env_settings",
        lambda: SimpleNamespace(rate_limit_window_seconds=60, rate_limit_requests=1, api_key="dev-local-key"),
    )

    first = client.post("/predict/failure", json={"orders": [SAMPLE_ORDER]})
    second = client.post("/predict/failure", json={"orders": [SAMPLE_ORDER]})

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.json().get("error", {}).get("code") == "rate_limited"
