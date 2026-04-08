from src.routing.optimizer import nearest_neighbor_route


def test_route_optimizer_returns_sequence() -> None:
    nodes = [
        {"order_id": "WAREHOUSE", "lat": 12.9716, "lon": 77.5946},
        {"order_id": "A", "lat": 12.9166, "lon": 77.6101},
        {"order_id": "B", "lat": 12.9591, "lon": 77.6974},
    ]
    result = nearest_neighbor_route(nodes)
    assert result["sequence"][0] == 0
    assert result["stop_count"] == 2
