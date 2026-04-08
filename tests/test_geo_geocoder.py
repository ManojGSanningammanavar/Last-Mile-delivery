from src.geo.geocoder import geocode_address


def test_geocode_known_harohalli_returns_cached_coords() -> None:
    lat, lon, confidence = geocode_address("harohalli", "Bengaluru")
    assert round(lat, 4) == 12.7167
    assert round(lon, 4) == 77.5333
    assert confidence >= 0.8


def test_geocode_konamakunte_alias_returns_cached_coords() -> None:
    lat, lon, confidence = geocode_address("konamakunte cross", "Bengaluru", pincode="560062")
    assert round(lat, 4) == 12.8774
    assert round(lon, 4) == 77.5595
    assert confidence >= 0.8
