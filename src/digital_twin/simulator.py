from __future__ import annotations

import random

from src.advanced.causal_uplift import recommend_causal_action


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def run_dispatch_digital_twin(predicted_orders: list[dict], horizon_steps: int = 8, seed: int = 42) -> dict:
    rng = random.Random(seed)
    steps = max(2, min(int(horizon_steps), 48))

    pending = [dict(order) for order in predicted_orders]
    timeline: list[dict] = []

    expected_fail_before = 0.0
    expected_fail_after = 0.0
    delivered_count = 0
    processed_count = 0

    for tick in range(1, steps + 1):
        if not pending:
            timeline.append(
                {
                    "step": tick,
                    "pending": 0,
                    "processed": 0,
                    "delivered": 0,
                    "avg_risk_before": 0.0,
                    "avg_risk_after": 0.0,
                    "interventions": {},
                    "weather_shock": 0.0,
                    "traffic_shock": 0.0,
                }
            )
            continue

        weather_shock = rng.uniform(-0.03, 0.08)
        traffic_shock = rng.uniform(-0.02, 0.06)

        processed_now = max(1, int(len(pending) * 0.35))
        current_batch = pending[:processed_now]
        pending = pending[processed_now:]
        processed_count += len(current_batch)

        interventions: dict[str, int] = {}
        before_values: list[float] = []
        after_values: list[float] = []
        delivered_now = 0

        for order in current_batch:
            base_risk = float(order.get("failure_probability", 0.35))
            distance = float(order.get("distance_km", 0.0))
            area_risk = float(order.get("area_risk_score", 0.25))

            runtime_risk = _clamp(
                base_risk
                + weather_shock * (0.65 + area_risk)
                + traffic_shock * (0.5 + min(distance, 15.0) / 15.0)
            )

            policy = recommend_causal_action(runtime_risk, order)
            best = policy["best_action"]
            action = str(best["action"])
            adjusted_risk = _clamp(float(best["expected_risk_after"]))

            expected_fail_before += runtime_risk
            expected_fail_after += adjusted_risk
            before_values.append(runtime_risk)
            after_values.append(adjusted_risk)

            interventions[action] = interventions.get(action, 0) + 1

            # Realization step for simulation timeline only.
            if rng.random() < (1.0 - adjusted_risk):
                delivered_now += 1

        delivered_count += delivered_now

        timeline.append(
            {
                "step": tick,
                "pending": len(pending),
                "processed": len(current_batch),
                "delivered": delivered_now,
                "avg_risk_before": round(sum(before_values) / max(len(before_values), 1), 4),
                "avg_risk_after": round(sum(after_values) / max(len(after_values), 1), 4),
                "interventions": interventions,
                "weather_shock": round(weather_shock, 4),
                "traffic_shock": round(traffic_shock, 4),
            }
        )

    processed_total = max(processed_count, 1)
    baseline_rate = expected_fail_before / processed_total
    optimized_rate = expected_fail_after / processed_total

    return {
        "config": {
            "horizon_steps": steps,
            "seed": seed,
            "orders_total": len(predicted_orders),
        },
        "summary": {
            "expected_failure_rate_before": round(baseline_rate, 4),
            "expected_failure_rate_after": round(optimized_rate, 4),
            "expected_improvement": round(max(0.0, baseline_rate - optimized_rate), 4),
            "orders_processed": int(processed_count),
            "orders_pending": int(len(pending)),
            "delivered_simulated": int(delivered_count),
        },
        "timeline": timeline,
    }
