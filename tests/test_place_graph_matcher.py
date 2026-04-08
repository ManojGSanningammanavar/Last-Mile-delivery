from src.place_graph.matcher import match_place


def test_place_graph_match() -> None:
    places = [{"place_id": "P0001", "canonical_area": "btm layout", "lat": 12.9166, "lon": 77.6101}]
    matched = match_place(places, "btm layout", 12.9167, 77.6100)
    assert matched == "P0001"
