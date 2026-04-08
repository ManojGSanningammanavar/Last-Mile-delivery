from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.geo.geocoder import warmup_geocode_cache


def _load_candidates() -> list[dict]:
    for path in [Path("data/processed/orders_clean.csv"), Path("data/raw/orders_raw.csv")]:
        if path.exists():
            frame = pd.read_csv(path)
            return frame.to_dict(orient="records")
    return []


def main() -> None:
    records = _load_candidates()
    result = warmup_geocode_cache(records, limit=800)
    print("Geocode warm-up summary:")
    print(result)


if __name__ == "__main__":
    main()
