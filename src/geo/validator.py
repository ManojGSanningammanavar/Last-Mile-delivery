from __future__ import annotations

from dataclasses import dataclass

from src.settings import get_city_geo_profile


@dataclass
class GeoValidationResult:
    geo_confidence: float
    is_valid: bool
    warnings: list[str]


def validate_geo(lat: float, lon: float, base_confidence: float, pincode: str, city: str = "Bengaluru") -> GeoValidationResult:
    warnings: list[str] = []
    conf = base_confidence
    dominant_penalty = 0.0

    profile = get_city_geo_profile(city)
    bounds = profile.get("bounds", {}) if isinstance(profile, dict) else {}
    lat_min = float(bounds.get("lat_min", 12.7))
    lat_max = float(bounds.get("lat_max", 13.2))
    lon_min = float(bounds.get("lon_min", 77.3))
    lon_max = float(bounds.get("lon_max", 77.9))

    if lat == 0.0 and lon == 0.0:
        warnings.append("coordinate_unresolved")
        conf = min(conf, 0.2)
        dominant_penalty = max(dominant_penalty, 0.2)

    if not pincode or len(pincode) != 6:
        warnings.append("pincode_missing_or_invalid")
        dominant_penalty = max(dominant_penalty, 0.1)

    if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
        warnings.append("outside_primary_city_bounds")
        dominant_penalty = max(dominant_penalty, 0.15)

    conf -= dominant_penalty

    conf = round(max(0.0, min(1.0, conf)), 3)
    return GeoValidationResult(geo_confidence=conf, is_valid=conf >= 0.45, warnings=warnings)
