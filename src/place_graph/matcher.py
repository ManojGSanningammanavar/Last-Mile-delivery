from __future__ import annotations

from src.utils.geo_utils import haversine_km


def match_place(places: list[dict], area: str, lat: float, lon: float, threshold: float = 0.78) -> str | None:
    best_match = None
    best_score = -1.0

    for place in places:
        area_score = 1.0 if place.get("canonical_area", "") == area else 0.0
        geo_distance = haversine_km(lat, lon, place.get("lat", 0.0), place.get("lon", 0.0))
        geo_score = max(0.0, 1.0 - (geo_distance / 10.0))
        score = 0.6 * area_score + 0.4 * geo_score

        if score > best_score:
            best_score = score
            best_match = place.get("place_id")

    if best_score >= threshold:
        return best_match
    return None
