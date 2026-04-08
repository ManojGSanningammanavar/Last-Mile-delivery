from __future__ import annotations


def eta_minutes(distance_km: float, average_speed_kmph: float = 22.0) -> int:
    if average_speed_kmph <= 0:
        average_speed_kmph = 22.0
    return int((distance_km / average_speed_kmph) * 60)
