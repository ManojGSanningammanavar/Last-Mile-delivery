from __future__ import annotations


def weather_risk_adjustment(base_risk: float, weather_risk_score: float) -> float:
    adjusted = base_risk + 0.2 * weather_risk_score
    return round(min(1.0, adjusted), 4)
