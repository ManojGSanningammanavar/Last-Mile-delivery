from src.address.parser import parse_address


def test_parse_address_extracts_area() -> None:
    parsed = parse_address("Near temple 3rd cross BTM Layout Bengaluru", "560076")
    assert parsed.area == "btm layout"
    assert parsed.pincode == "560076"


def test_parse_address_extracts_single_word_halli_area() -> None:
    parsed = parse_address("police station near, Harohalli", "562112")
    assert parsed.area == "harohalli"
    assert parsed.pincode == "562112"


def test_parse_address_extracts_cross_locality() -> None:
    parsed = parse_address("forum mall , Konamakunte Cross", "560062")
    assert parsed.area == "konamakunte cross"
    assert parsed.pincode == "560062"
