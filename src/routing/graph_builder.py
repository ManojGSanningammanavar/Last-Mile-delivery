from __future__ import annotations

from typing import Dict, List

from src.utils.geo_utils import haversine_km


def build_distance_matrix(nodes: List[dict]) -> Dict[tuple[int, int], float]:
    matrix: Dict[tuple[int, int], float] = {}
    for i, node_i in enumerate(nodes):
        for j, node_j in enumerate(nodes):
            if i == j:
                matrix[(i, j)] = 0.0
                continue
            matrix[(i, j)] = haversine_km(node_i["lat"], node_i["lon"], node_j["lat"], node_j["lon"])
    return matrix
