from duration import format_duration, parse_duration


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


def test_parse_duration_milliseconds():
    assert parse_duration('500ms') == 500


def test_parse_duration_seconds_decimal():
    assert parse_duration('1.5s') == 1500


def test_parse_duration_seconds_whole():
    assert parse_duration('30.0s') == 30000


def test_parse_duration_minutes_zero_seconds():
    assert parse_duration('1m 0s') == 60000


def test_parse_duration_minutes_seconds():
    assert parse_duration('2m 5s') == 125000
