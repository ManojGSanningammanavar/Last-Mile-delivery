from __future__ import annotations

import src.geo.geocoder as geocoder


def test_enqueue_geocode_enrichment_accepts_unknown_key(monkeypatch) -> None:
    monkeypatch.setattr(geocoder, "get_yaml_config", lambda: {"geocode": {"enable_async_enrichment": True}})
    accepted = geocoder.enqueue_geocode_enrichment(
        area="new locality",
        city="Bengaluru",
        raw_address="new locality bengaluru",
        pincode="560001",
    )
    assert accepted in {True, False}


def test_warmup_geocode_cache_counts_rows(monkeypatch) -> None:
    calls = []

    def _fake_geocode(area: str, city: str, raw_address: str = "", pincode: str = ""):
        calls.append((area, city, raw_address, pincode))
        return 12.9, 77.6, 0.8

    monkeypatch.setattr(geocoder, "geocode_address", _fake_geocode)

    rows = [
        {"area": "btm layout", "city": "Bengaluru", "pincode": "560076", "address_raw": "btm layout"},
        {"area": "whitefield", "city": "Bengaluru", "pincode": "560066", "address_raw": "whitefield"},
    ]
    result = geocoder.warmup_geocode_cache(rows, limit=2)

    assert result["requested"] == 2
    assert len(calls) == 2
