from src.geo.validator import validate_geo


def test_geo_validator_marks_valid_coordinate() -> None:
    result = validate_geo(12.95, 77.61, 0.9, "560001")
    assert result.is_valid is True
    assert result.geo_confidence >= 0.7
