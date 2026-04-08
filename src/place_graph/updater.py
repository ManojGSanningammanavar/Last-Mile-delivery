from __future__ import annotations

from src.place_graph.place_node import PlaceNode


def upsert_place(
    places: list[dict],
    matched_place_id: str | None,
    area: str,
    lat: float,
    lon: float,
    delivered: bool,
) -> list[dict]:
    if matched_place_id:
        for place in places:
            if place["place_id"] == matched_place_id:
                if delivered:
                    place["success_count"] += 1
                else:
                    place["failure_count"] += 1
                return places

    next_id = f"P{len(places) + 1:04d}"
    new_place = PlaceNode(
        place_id=next_id,
        canonical_area=area,
        lat=float(lat),
        lon=float(lon),
        success_count=1 if delivered else 0,
        failure_count=0 if delivered else 1,
    )
    places.append(new_place.to_dict())
    return places
