from __future__ import annotations

from urllib.parse import urlencode

import httpx


def _sample_points(points: list[dict], max_points: int = 24) -> list[dict]:
    if len(points) <= max_points:
        return points

    sampled: list[dict] = []
    last = len(points) - 1
    step = last / (max_points - 1)

    for idx in range(max_points):
        src_idx = round(idx * step)
        sampled.append(points[min(src_idx, last)])

    return sampled


def fetch_osrm_road_path(points: list[dict], timeout_seconds: float = 8.0) -> dict:
    if len(points) < 2:
        return {
            "available": False,
            "message": "Need at least two coordinates.",
            "geometry": [],
            "distance_km": None,
            "duration_min": None,
            "provider": "osrm",
        }

    sampled = _sample_points(points, max_points=24)
    coord_text = ";".join(f"{p['lon']:.6f},{p['lat']:.6f}" for p in sampled)
    query = urlencode({"overview": "full", "geometries": "geojson", "steps": "false"})
    url = f"https://router.project-osrm.org/route/v1/driving/{coord_text}?{query}"

    try:
        response = httpx.get(url, timeout=timeout_seconds)
        response.raise_for_status()
        payload = response.json()

        route = (payload.get("routes") or [{}])[0]
        coords = route.get("geometry", {}).get("coordinates") or []
        geometry = [
            {"lat": float(pair[1]), "lon": float(pair[0])}
            for pair in coords
            if isinstance(pair, list) and len(pair) >= 2
        ]

        if not geometry:
            return {
                "available": False,
                "message": "Road route provider returned no geometry.",
                "geometry": [],
                "distance_km": None,
                "duration_min": None,
                "provider": "osrm",
            }

        return {
            "available": True,
            "message": "ok",
            "geometry": geometry,
            "distance_km": round(float(route.get("distance", 0.0)) / 1000, 3),
            "duration_min": round(float(route.get("duration", 0.0)) / 60, 2),
            "provider": "osrm",
        }
    except Exception as exc:
        return {
            "available": False,
            "message": f"Road route fetch failed: {exc}",
            "geometry": [],
            "distance_km": None,
            "duration_min": None,
            "provider": "osrm",
        }
