from __future__ import annotations


def simulate_interventions(failure_probability: float, time_slot: str) -> dict:
    base = max(0.0, min(1.0, float(failure_probability)))
    slot = str(time_slot or "").lower()

    # Use proportional reductions so expected gain scales with baseline risk.
    # This avoids nearly constant "improvement" values across very different inputs.
    reschedule_factor = 0.72 if slot in {"evening", "night"} else 0.90
    scenarios = {
        "no_change": base,
        "pre_call": max(0.0, base * 0.82),
        "reschedule_afternoon": max(0.0, base * reschedule_factor),
        "landmark_reconfirm": max(0.0, base * 0.85),
    }
    best_action = min(scenarios, key=scenarios.get)
    return {
        "scenarios": {k: round(v, 4) for k, v in scenarios.items()},
        "best_action": best_action,
        "expected_risk": round(scenarios[best_action], 4),
    }
