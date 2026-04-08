from __future__ import annotations

import re
from dataclasses import dataclass

from src.address.normalizer import normalize_address
from src.geo.cache import AREA_COORD_CACHE
from src.settings import get_yaml_config

LANDMARK_CUES = {"near", "opposite", "behind", "beside"}


def _known_areas() -> list[str]:
    cfg = get_yaml_config()
    aliases = cfg.get("address", {}).get("area_aliases", [])
    areas = {str(item).strip().lower() for item in AREA_COORD_CACHE.keys()}
    if isinstance(aliases, list):
        areas.update(str(item).strip().lower() for item in aliases if str(item).strip())
    return sorted(areas, key=len, reverse=True)


def _extract_generic_area(clean_text: str) -> str:
    # Prefer locality phrases around separators like commas first.
    comma_parts = [part.strip() for part in clean_text.split(",") if part.strip()]
    locality_patterns = [
        r"\b([a-z]+\s+cross)\b",
        r"\b([a-z]+\s+main\s+road)\b",
        r"\b([a-z]+\s+road)\b",
        r"\b([a-z]+\s+phase)\b",
        r"\b([a-z]+\s+stage)\b",
    ]
    for part in comma_parts:
        for pattern in locality_patterns:
            match = re.search(pattern, part)
            if match:
                return match.group(1).strip()

    patterns = [
        r"\b([a-z]+\s+(?:layout|nagar|halli|field|city))\b",
        r"\b([a-z]+\s+cross)\b",
        r"\b([a-z]+\s+main\s+road)\b",
        r"\b([a-z]+\s+road)\b",
        r"\b([a-z]+\s+phase)\b",
        r"\b([a-z]+\s+stage)\b",
        r"\b([a-z]+(?:pur|pet|pura|kere|wadi|halli))\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, clean_text)
        if match:
            return match.group(1).strip()
    return ""


@dataclass
class ParsedAddress:
    clean_text: str
    area: str
    landmark: str
    pincode: str


def parse_address(raw_address: str, fallback_pincode: str = "") -> ParsedAddress:
    clean_text = normalize_address(raw_address)
    fallback = str(fallback_pincode or "").strip()
    pincode = fallback if re.fullmatch(r"\d{6}", fallback) else ""
    if not pincode:
        pincode_match = re.search(r"\b\d{6}\b", clean_text)
        pincode = pincode_match.group(0) if pincode_match else ""

    area = ""
    for area_name in _known_areas():
        if area_name in clean_text:
            area = area_name
            break
    if not area:
        area = _extract_generic_area(clean_text)

    landmark = ""
    tokens = clean_text.split()
    for idx, token in enumerate(tokens):
        if token in LANDMARK_CUES and idx + 1 < len(tokens):
            landmark = " ".join(tokens[idx : min(idx + 4, len(tokens))])
            break

    return ParsedAddress(clean_text=clean_text, area=area, landmark=landmark, pincode=pincode)
