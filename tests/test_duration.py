from duration import format_duration


def test_sub_second() -> None:
    assert format_duration(500) == "500ms"


def test_seconds() -> None:
    assert format_duration(1500) == "1.5s"


def test_seconds_30() -> None:
    assert format_duration(30000) == "30.0s"


def test_exact_60_seconds() -> None:
    assert format_duration(60000) == "1m 0s"


def test_one_minute_five_seconds() -> None:
    assert format_duration(65000) == "1m 5s"


def test_two_minutes_five_seconds() -> None:
    assert format_duration(125000) == "2m 5s"


def test_zero_milliseconds() -> None:
    assert format_duration(0) == "0ms"


def test_one_millisecond() -> None:
    assert format_duration(1) == "1ms"


def test_just_under_one_second() -> None:
    assert format_duration(999) == "999ms"


def test_one_hour() -> None:
    assert format_duration(3600000) == "60m 0s"
