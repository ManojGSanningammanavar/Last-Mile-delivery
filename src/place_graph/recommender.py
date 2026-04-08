from __future__ import annotations


def recommend_action(place: dict | None, risk_label: str) -> str:
    if risk_label == "HIGH":
        if place and place.get("success_rate", 0.5) < 0.5:
            return "call_first_and_reschedule_slot"
        return "call_first_with_landmark_confirmation"

    if risk_label == "MEDIUM":
        return "send_pre_delivery_confirmation_sms"

    return "standard_delivery_flow"
