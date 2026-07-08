from duration import format_duration


def test_sub_second():
    assert format_duration(500) == "500ms"


def test_seconds():
    assert format_duration(1500) == "1.5s"


def test_seconds_30():
    assert format_duration(30000) == "30.0s"


def test_exact_60_seconds():
    assert format_duration(60000) == "1m 0s"


def test_one_minute_five_seconds():
    assert format_duration(65000) == "1m 5s"


def test_two_minutes_five_seconds():
    assert format_duration(125000) == "2m 5s"
