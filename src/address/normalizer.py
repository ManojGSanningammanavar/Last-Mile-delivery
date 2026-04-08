from __future__ import annotations

import re

ABBREVIATION_MAP = {
    "opp": "opposite",
    "nr": "near",
    "rd": "road",
    "st": "street",
    "lyt": "layout",
    "ph": "phase",
}


def normalize_address(raw_address: str) -> str:
    text = raw_address.strip().lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    tokens = text.split(" ")
    expanded = [ABBREVIATION_MAP.get(token, token) for token in tokens]
    return " ".join(expanded).strip()
