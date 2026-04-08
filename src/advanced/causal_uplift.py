from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActionEstimate:
    action: str
    uplift_abs: float
    uplift_pct: float
    expected_risk_after: float
    confidence: str


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _confidence_bucket(address_confidence: float, geo_confidence: float) -> str:
    blend = 0.6 * address_confidence + 0.4 * geo_confidence
    if blend >= 0.8:
        return "high"
    if blend >= 0.6:
        return "medium"
    return "low"


def _action_uplift(action: str, base_risk: float, context: dict) -> float:
    address_conf = float(context.get("address_confidence", 0.7))
    geo_conf = float(context.get("geo_confidence", 0.8))
    past_failures = float(context.get("past_failures", 0.0))
    distance_km = float(context.get("distance_km", 0.0))
    area_risk = float(context.get("area_risk_score", 0.25))
    time_slot = str(context.get("time_slot", "afternoon")).lower()

    if action == "pre_call":
        uplift = 0.03 + 0.12 * max(0.0, 1.0 - address_conf) + 0.03 * min(past_failures, 3.0) / 3.0
    elif action == "reschedule_day_slot":
        slot_penalty = 0.12 if time_slot in {"evening", "night"} else 0.04
        uplift = 0.02 + slot_penalty + 0.05 * area_risk
    elif action == "address_reconfirm":
        uplift = 0.04 + 0.14 * max(0.0, 0.9 - address_conf) + 0.03 * max(0.0, 0.85 - geo_conf)
    elif action == "driver_note_enrichment":
        uplift = 0.015 + 0.02 * (distance_km / 12.0) + 0.04 * area_risk
    else:
        uplift = 0.0

    # Smaller headroom when baseline risk is already low.
    headroom = 0.2 + 0.8 * base_risk
    return _clamp(uplift * headroom, 0.0, 0.35)


def rank_actions(base_risk: float, context: dict) -> list[ActionEstimate]:
    base = _clamp(float(base_risk))
    confidence = _confidence_bucket(
        float(context.get("address_confidence", 0.7)),
        float(context.get("geo_confidence", 0.8)),
    )

    actions = [
        "no_change",
        "pre_call",
        "reschedule_day_slot",
        "address_reconfirm",
        "driver_note_enrichment",
    ]

    ranked: list[ActionEstimate] = []
    for action in actions:
        uplift = 0.0 if action == "no_change" else _action_uplift(action, base, context)
        expected_after = _clamp(base - uplift)
        uplift_pct = 0.0 if base <= 1e-8 else uplift / base
        ranked.append(
            ActionEstimate(
                action=action,
                uplift_abs=round(uplift, 4),
                uplift_pct=round(uplift_pct, 4),
                expected_risk_after=round(expected_after, 4),
                confidence=confidence,
            )
        )

    ranked.sort(key=lambda item: (item.expected_risk_after, -item.uplift_abs, item.action))
    return ranked


def recommend_causal_action(base_risk: float, context: dict) -> dict:
    ranked = rank_actions(base_risk, context)
    best = ranked[0]
    return {
        "base_risk": round(float(base_risk), 4),
        "best_action": {
            "action": best.action,
            "expected_risk_after": best.expected_risk_after,
            "uplift_abs": best.uplift_abs,
            "uplift_pct": best.uplift_pct,
            "confidence": best.confidence,
        },
        "ranked_actions": [
            {
                "action": item.action,
                "expected_risk_after": item.expected_risk_after,
                "uplift_abs": item.uplift_abs,
                "uplift_pct": item.uplift_pct,
                "confidence": item.confidence,
            }
            for item in ranked
        ],
    }
