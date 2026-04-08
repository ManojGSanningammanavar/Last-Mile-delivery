from __future__ import annotations

from fastapi import APIRouter, Depends

from src.address.parser import parse_address
from src.api.schemas import OrdersBatchRequest, RoadPathRequest
from src.api.security import verify_api_key
from src.geo.geocoder import geocode_address
from src.geo.validator import validate_geo
from src.routing.alternatives import build_route_alternatives
from src.routing.road_path import fetch_osrm_road_path
from src.routing.traffic import traffic_signal

router = APIRouter(prefix="/route", tags=["route"], dependencies=[Depends(verify_api_key)])


@router.post("/optimize")
def optimize_route(request: OrdersBatchRequest) -> dict:
    nodes = [{"order_id": "WAREHOUSE", "lat": 12.9716, "lon": 77.5946}]
    geo_notes: list[dict] = []

    for order in request.orders:
        parsed = parse_address(order.address_raw, order.pincode)
        lat, lon, base_conf = geocode_address(
            parsed.area,
            order.city,
            raw_address=order.address_raw,
            pincode=parsed.pincode,
        )
        geo = validate_geo(lat, lon, base_conf, parsed.pincode, order.city)

        nodes.append({"order_id": order.order_id, "lat": lat, "lon": lon})
        geo_notes.append(
            {
                "order_id": order.order_id,
                "area": parsed.area,
                "geo_confidence": geo.geo_confidence,
                "geo_warnings": geo.warnings,
            }
        )

    bundle = build_route_alternatives(nodes)
    routes = list(bundle.get("routes", []))[:3]
    selected_key = str(bundle.get("selected_key", "fastest"))
    route = next((item for item in routes if str(item.get("key")) == selected_key), None)
    if route is None:
        route = routes[0] if routes else {}

    sequence_order_ids = route.get("sequence_order_ids", [])
    selected_traffic = route.get("traffic_signal")
    if not isinstance(selected_traffic, dict):
        selected_traffic = traffic_signal(
            distance_km=float(route.get("distance_km", 0.0)),
            duration_min=float(route.get("duration_min", route.get("eta_minutes", 0))),
        )
    return {
        "route_selected_key": selected_key,
        "route_options": routes,
        "sequence_order_ids": sequence_order_ids,
        "distance_km": route.get("distance_km", 0.0),
        "eta_minutes": route.get("eta_minutes", 0),
        "duration_min": route.get("duration_min", route.get("eta_minutes", 0)),
        "traffic_signal": selected_traffic,
        "source": route.get("source", "unknown"),
        "polyline": route.get("polyline", []),
        "geo_notes": geo_notes,
    }


@router.post("/road-path")
def road_path_route(request: RoadPathRequest) -> dict:
    points = [{"lat": p.lat, "lon": p.lon} for p in request.coordinates]
    return fetch_osrm_road_path(points)
