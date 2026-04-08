from __future__ import annotations


def traffic_signal(distance_km: float, duration_min: float) -> dict:
    distance = float(distance_km or 0.0)
    duration = float(duration_min or 0.0)
    if distance <= 0 or duration <= 0:
        return {
            "traffic_level": "unknown",
            "traffic_multiplier": 1.0,
            "effective_speed_kmph": 0.0,
            "source": "derived_route_signal",
        }

    effective_speed = (distance / duration) * 60.0
    if effective_speed >= 24.0:
        level = "low"
        multiplier = 1.0
    elif effective_speed >= 18.0:
        level = "moderate"
        multiplier = 1.07
    elif effective_speed >= 12.0:
        level = "heavy"
        multiplier = 1.14
    else:
        level = "severe"
        multiplier = 1.25

    return {
        "traffic_level": level,
        "traffic_multiplier": multiplier,
        "effective_speed_kmph": round(effective_speed, 2),
        "source": "derived_route_signal",
    }
