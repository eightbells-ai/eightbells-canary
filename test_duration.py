from duration import format_duration


def test_sub_second():
    assert format_duration(500) == "500ms"


def test_seconds():
    assert format_duration(1500) == "1.5s"


def test_sub_second_edge_cases():
    """Test values <1000ms to verify unchanged behavior."""
    assert format_duration(0) == "0ms"
    assert format_duration(1) == "1ms"
    assert format_duration(999) == "999ms"


def test_seconds_range():
    """Test values 1000-59999ms to verify unchanged behavior."""
    assert format_duration(1000) == "1.0s"
    assert format_duration(5000) == "5.0s"
    assert format_duration(30000) == "30.0s"
    assert format_duration(59999) == "60.0s"


def test_exactly_one_minute():
    """Test exactly 60000ms expecting '1m 0s'."""
    assert format_duration(60000) == "1m 0s"


def test_one_minute_five_seconds():
    """Test 65000ms expecting '1m 5s'."""
    assert format_duration(65000) == "1m 5s"


def test_two_minutes_five_seconds():
    """Test 125000ms expecting '2m 5s'."""
    assert format_duration(125000) == "2m 5s"


def test_minutes_edge_cases():
    """Test additional edge cases for minute formatting."""
    assert format_duration(119999) == "1m 59s"
    assert format_duration(120000) == "2m 0s"
    assert format_duration(600000) == "10m 0s"
    assert format_duration(3661000) == "61m 1s"
