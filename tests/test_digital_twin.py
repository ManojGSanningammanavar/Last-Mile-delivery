import pytest

from src.digital_twin.simulator import run_dispatch_digital_twin


def test_digital_twin_summary_rates_match_weighted_timeline() -> None:
    orders = [
        {
            "order_id": f"ORD_{idx}",
            "failure_probability": 0.45,
            "distance_km": 6.0,
            "area_risk_score": 0.3,
            "address_confidence": 0.7,
            "geo_confidence": 0.8,
            "time_slot": "evening",
            "past_failures": 1,
        }
        for idx in range(10)
    ]

    out = run_dispatch_digital_twin(predicted_orders=orders, horizon_steps=2, seed=42)
    summary = out["summary"]
    timeline = out["timeline"]

    processed = int(summary["orders_processed"])
    pending = int(summary["orders_pending"])

    assert processed + pending == len(orders)
    assert processed > 0

    weighted_before = sum(step["avg_risk_before"] * step["processed"] for step in timeline) / processed
    weighted_after = sum(step["avg_risk_after"] * step["processed"] for step in timeline) / processed

    assert summary["expected_failure_rate_before"] == pytest.approx(weighted_before, abs=1e-4)
    assert summary["expected_failure_rate_after"] == pytest.approx(weighted_after, abs=1e-4)
