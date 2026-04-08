from __future__ import annotations

import random
from pathlib import Path

import pandas as pd


AREAS = [
    "btm layout",
    "hsr layout",
    "indiranagar",
    "whitefield",
    "jayanagar",
    "electronic city",
    "marathahalli",
    "jp nagar",
    "kengeri",
    "bellandur",
]

AREA_PINCODE = {
    "btm layout": "560076",
    "hsr layout": "560102",
    "indiranagar": "560038",
    "whitefield": "560066",
    "jayanagar": "560011",
    "electronic city": "560100",
    "marathahalli": "560037",
    "jp nagar": "560078",
    "kengeri": "560060",
    "bellandur": "560103",
}

LANDMARKS = ["near temple", "opp school", "behind mall", "beside park", "near metro", "close to lake"]
TIME_SLOTS = ["morning", "afternoon", "evening", "night"]
FAIL_REASONS = ["wrong_address", "customer_unavailable", "rescheduled", "out_of_zone", "pincode_mismatch"]


def _noisy_address(area: str) -> str:
    base = f"{random.choice(LANDMARKS)} {random.randint(1, 12)}th cross {area} bengaluru"
    if random.random() < 0.16:
        base = base.replace("cross", "crs").replace("bengaluru", "blru")
    if random.random() < 0.08:
        base = " ".join(base.split()[:-1])
    if random.random() < 0.06:
        base = f"{base} ???"
    return base


def _row(index: int) -> dict:
    area = random.choice(AREAS)
    hour = random.choice([9, 11, 13, 16, 18, 20])
    minute = random.choice([5, 15, 25, 35, 45, 55])
    day = random.randint(1, 28)
    time_slot = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening" if hour < 20 else "night"
    if random.random() < 0.1:
        time_slot = random.choice(TIME_SLOTS)

    past_failures = random.choices([0, 1, 2, 3, 4], weights=[0.42, 0.26, 0.18, 0.09, 0.05])[0]
    distance_km = round(random.uniform(1.0, 20.0), 1)
    bad_pincode = random.random() < 0.08
    missing_pincode = random.random() < 0.1

    pincode = "" if missing_pincode else ("560000" if bad_pincode else AREA_PINCODE[area])

    base_fail = 0.07
    base_fail += 0.03 * past_failures
    base_fail += 0.015 * max(distance_km - 6.0, 0)
    if time_slot in {"evening", "night"}:
        base_fail += 0.08
    if bad_pincode or missing_pincode:
        base_fail += 0.14
    address_raw = _noisy_address(area)
    if "???" in address_raw:
        base_fail += 0.06

    failed = random.random() < min(base_fail, 0.85)

    return {
        "order_id": f"ORD{index:05d}",
        "order_datetime": f"2026-03-{day:02d} {hour:02d}:{minute:02d}:00",
        "address_raw": address_raw,
        "city": "Bengaluru",
        "pincode": pincode,
        "customer_id": f"C{random.randint(1, 1200):04d}",
        "past_failures": past_failures,
        "distance_km": distance_km,
        "time_slot": time_slot,
        "delivery_status": "failed" if failed else "delivered",
        "failure_reason": random.choice(FAIL_REASONS) if failed else "",
    }


def main() -> None:
    random.seed(42)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    generated = [_row(i) for i in range(1, 6001)]
    orders = pd.DataFrame(generated)

    orders.to_csv("data/raw/orders_raw.csv", index=False)
    orders.to_csv("data/processed/orders_clean.csv", index=False)
    print(f"Generated synthetic dataset with {len(orders)} rows.")


if __name__ == "__main__":
    main()
