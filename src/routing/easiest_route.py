from __future__ import annotations

from urllib.parse import urlencode

import httpx

from src.routing.eta import eta_minutes
from src.routing.optimizer import nearest_neighbor_route


OSRM_TRIP_BASE = "https://router.project-osrm.org/trip/v1/driving"


def _fallback_route(nodes: list[dict]) -> dict:
    fallback = nearest_neighbor_route(nodes)
    sequence = fallback.get("sequence", list(range(len(nodes))))
    polyline = [
        {"lat": float(nodes[idx]["lat"]), "lon": float(nodes[idx]["lon"])}
        for idx in sequence
        if 0 <= idx < len(nodes)
    ]

    distance_km = float(fallback.get("distance_km", 0.0))
    return {
        "sequence": sequence,
        "sequence_order_ids": [nodes[idx]["order_id"] for idx in sequence if 0 <= idx < len(nodes)],
        "distance_km": round(distance_km, 2),
        "duration_min": int(eta_minutes(distance_km)),
        "eta_minutes": int(eta_minutes(distance_km)),
        "stop_count": max(0, len(sequence) - 1),
        "polyline": polyline,
        "source": "haversine_fallback",
    }


def optimize_easiest_route(nodes: list[dict], timeout_seconds: float = 8.0) -> dict:
    if len(nodes) <= 1:
        return _fallback_route(nodes)

    coord_text = ";".join(f"{float(node['lon']):.6f},{float(node['lat']):.6f}" for node in nodes)
    query = urlencode(
        {
            "source": "first",
            "roundtrip": "false",
            "overview": "full",
            "geometries": "geojson",
            "steps": "false",
        }
    )
    url = f"{OSRM_TRIP_BASE}/{coord_text}?{query}"

    try:
        response = httpx.get(url, timeout=timeout_seconds)
        response.raise_for_status()
        payload = response.json()

        trip = (payload.get("trips") or [{}])[0]
        waypoints = payload.get("waypoints") or []
        if not waypoints or not trip:
            return _fallback_route(nodes)

        ranked = sorted(
            ((idx, int(wp.get("waypoint_index", idx))) for idx, wp in enumerate(waypoints)),
            key=lambda pair: pair[1],
        )
        sequence = [idx for idx, _ in ranked]

        geometry = trip.get("geometry", {}).get("coordinates") or []
        polyline = [
            {"lat": float(point[1]), "lon": float(point[0])}
            for point in geometry
            if isinstance(point, list) and len(point) >= 2
        ]

        if len(polyline) == 0 or len(sequence) == 0:
            return _fallback_route(nodes)

        distance_km = round(float(trip.get("distance", 0.0)) / 1000, 2)
        duration_min = int(round(float(trip.get("duration", 0.0)) / 60))

        return {
            "sequence": sequence,
            "sequence_order_ids": [nodes[idx]["order_id"] for idx in sequence if 0 <= idx < len(nodes)],
            "distance_km": distance_km,
            "duration_min": duration_min,
            "eta_minutes": duration_min,
            "stop_count": max(0, len(sequence) - 1),
            "polyline": polyline,
            "source": "road_trip_osrm",
        }
    except Exception:
        return _fallback_route(nodes)
