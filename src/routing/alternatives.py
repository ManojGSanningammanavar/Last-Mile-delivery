from __future__ import annotations

from src.routing.easiest_route import optimize_easiest_route
from src.routing.eta import eta_minutes
from src.routing.optimizer import nearest_neighbor_route
from src.routing.road_path import fetch_osrm_road_path
from src.routing.traffic import traffic_signal


def _sequence_polyline(nodes: list[dict], sequence: list[int]) -> list[dict]:
    return [
        {"lat": float(nodes[idx]["lat"]), "lon": float(nodes[idx]["lon"])}
        for idx in sequence
        if 0 <= idx < len(nodes)
    ]


def _sequence_ids(nodes: list[dict], sequence: list[int]) -> list[str]:
    return [str(nodes[idx]["order_id"]) for idx in sequence if 0 <= idx < len(nodes)]


def _attach_traffic(route: dict) -> dict:
    route["traffic_signal"] = traffic_signal(
        distance_km=float(route.get("distance_km", 0.0)),
        duration_min=float(route.get("duration_min", route.get("eta_minutes", 0.0))),
    )
    return route


def build_route_alternatives(nodes: list[dict]) -> dict:
    if len(nodes) <= 1:
        empty_route = {
            "key": "fastest",
            "label": "Fastest",
            "distance_km": 0.0,
            "duration_min": 0,
            "eta_minutes": 0,
            "sequence_order_ids": [str(n.get("order_id", "")) for n in nodes],
            "polyline": _sequence_polyline(nodes, list(range(len(nodes)))),
            "source": "empty",
        }
        return {
            "selected_key": "fastest",
            "routes": [_attach_traffic(empty_route)],
            "active": _attach_traffic(empty_route),
        }

    # Option 1: shortest by direct-distance heuristic (legacy baseline).
    shortest_nn = nearest_neighbor_route(nodes)
    shortest_seq = list(shortest_nn.get("sequence", list(range(len(nodes)))))
    shortest_distance = float(shortest_nn.get("distance_km", 0.0))
    shortest_route = {
        "key": "shortest",
        "label": "Shortest",
        "distance_km": round(shortest_distance, 2),
        "duration_min": int(eta_minutes(shortest_distance)),
        "eta_minutes": int(eta_minutes(shortest_distance)),
        "sequence_order_ids": _sequence_ids(nodes, shortest_seq),
        "polyline": _sequence_polyline(nodes, shortest_seq),
        "source": "direct_haversine",
    }

    # Option 2: fastest by road-network optimization.
    fastest = optimize_easiest_route(nodes)
    fastest_route = {
        "key": "fastest",
        "label": "Fastest",
        "distance_km": round(float(fastest.get("distance_km", 0.0)), 2),
        "duration_min": int(fastest.get("duration_min", fastest.get("eta_minutes", 0))),
        "eta_minutes": int(fastest.get("eta_minutes", 0)),
        "sequence_order_ids": list(fastest.get("sequence_order_ids", [])),
        "polyline": list(fastest.get("polyline", [])),
        "source": str(fastest.get("source", "unknown")),
    }

    # Option 3: balanced = road path over shortest sequence (stable order + real roads).
    shortest_points = [
        {"lat": float(nodes[idx]["lat"]), "lon": float(nodes[idx]["lon"])}
        for idx in shortest_seq
        if 0 <= idx < len(nodes)
    ]
    balanced_osrm = fetch_osrm_road_path(shortest_points)
    if balanced_osrm.get("available"):
        balanced_route = {
            "key": "balanced",
            "label": "Balanced",
            "distance_km": round(float(balanced_osrm.get("distance_km", 0.0)), 2),
            "duration_min": int(round(float(balanced_osrm.get("duration_min", 0.0)))),
            "eta_minutes": int(round(float(balanced_osrm.get("duration_min", 0.0)))),
            "sequence_order_ids": _sequence_ids(nodes, shortest_seq),
            "polyline": list(balanced_osrm.get("geometry", [])),
            "source": "road_sequence_osrm",
        }
    else:
        balanced_route = {
            "key": "balanced",
            "label": "Balanced",
            "distance_km": shortest_route["distance_km"],
            "duration_min": shortest_route["duration_min"],
            "eta_minutes": shortest_route["eta_minutes"],
            "sequence_order_ids": shortest_route["sequence_order_ids"],
            "polyline": shortest_route["polyline"],
            "source": "balanced_fallback_direct",
        }

    routes = [_attach_traffic(fastest_route), _attach_traffic(shortest_route), _attach_traffic(balanced_route)]
    active = routes[0]
    return {
        "selected_key": "fastest",
        "routes": routes,
        "active": active,
    }
