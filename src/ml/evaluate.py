from __future__ import annotations

import json
from pathlib import Path


def load_metrics(metadata_path: str) -> dict:
    path = Path(metadata_path)
    if not path.exists():
        return {"status": "missing_metadata"}
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
