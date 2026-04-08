from __future__ import annotations

from typing import List

from src.routing.graph_builder import build_distance_matrix


def nearest_neighbor_route(nodes: List[dict]) -> dict:
    if not nodes:
        return {"sequence": [], "distance_km": 0.0}

    matrix = build_distance_matrix(nodes)
    remaining = set(range(1, len(nodes)))
    sequence = [0]
    total_distance = 0.0
    current = 0

    while remaining:
        next_node = min(remaining, key=lambda idx: matrix[(current, idx)])
        total_distance += matrix[(current, next_node)]
        sequence.append(next_node)
        remaining.remove(next_node)
        current = next_node

    return {
        "sequence": sequence,
        "distance_km": round(total_distance, 2),
        "stop_count": len(sequence) - 1,
    }
