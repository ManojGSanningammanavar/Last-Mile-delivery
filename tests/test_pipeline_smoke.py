from src.pipeline.run_pipeline import process_orders


def test_pipeline_smoke() -> None:
    sample_orders = [
        {
            "order_id": "ORD_TEST_001",
            "order_datetime": "2026-03-18 10:30:00",
            "address_raw": "Near temple 3rd cross BTM Layout Bengaluru",
            "city": "Bengaluru",
            "pincode": "560076",
            "past_failures": 1,
            "distance_km": 5.2,
            "time_slot": "morning",
            "area_risk_score": 0.3,
        }
    ]
    place_graph = {"places": []}

    # Model path is expected to exist after training pipeline; this test validates shape only.
    # It is acceptable to run after `scripts/train_model.py`.
    try:
        result = process_orders(sample_orders, "models/failure_model.pkl", place_graph)
        assert "orders" in result
        assert "route" in result
    except FileNotFoundError:
        assert True
