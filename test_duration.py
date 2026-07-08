from duration import format_duration


def test_sub_second():
    assert format_duration(500) == "500ms"


def test_seconds():
    assert format_duration(1500) == "1.5s"
