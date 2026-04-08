from __future__ import annotations

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.run_pipeline import process_orders
from src.utils.io import read_json


if __name__ == "__main__":
    sample_orders = [
        {
            "order_id": "ORD_DEMO_001",
            "order_datetime": "2026-03-18 12:15:00",
            "address_raw": "Opp school 2nd main HSR lyt Bangalore",
            "city": "Bengaluru",
            "pincode": "560102",
            "past_failures": 2,
            "distance_km": 8.6,
            "time_slot": "evening",
            "area_risk_score": 0.29,
        }
    ]
    place_graph = read_json("data/processed/place_graph.json")
    result = process_orders(sample_orders, "models/failure_model.pkl", place_graph)
    print(json.dumps(result, indent=2))
