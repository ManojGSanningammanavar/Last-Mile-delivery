from __future__ import annotations


def recommend_action(risk: float, address_conf: float) -> str:
    if risk > 0.7:
        return "call_customer_before_dispatch"
    if address_conf < 0.5:
        return "request_better_landmark"
    if risk > 0.45:
        return "send_confirmation_and_schedule_day_slot"
    return "proceed_normal_delivery"
