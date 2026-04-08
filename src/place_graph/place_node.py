from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class PlaceNode:
    place_id: str
    canonical_area: str
    lat: float
    lon: float
    success_count: int = 0
    failure_count: int = 0

    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.5
        return round(self.success_count / total, 4)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["success_rate"] = self.success_rate()
        return payload
