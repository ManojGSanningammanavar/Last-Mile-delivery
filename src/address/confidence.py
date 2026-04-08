from __future__ import annotations

from src.address.parser import ParsedAddress


def address_confidence(parsed: ParsedAddress) -> float:
    score = 0.2
    if parsed.clean_text and len(parsed.clean_text) > 10:
        score += 0.25
    if parsed.area:
        score += 0.25
    if parsed.landmark:
        score += 0.15
    if parsed.pincode and len(parsed.pincode) == 6:
        score += 0.15
    return round(min(score, 1.0), 3)
