from duration import format_duration


def test_sub_second():
    assert format_duration(500) == "500ms"


def test_seconds():
    assert format_duration(1500) == "1.5s"


def test_minute_boundary():
    """Test exactly 60000ms (1 minute)"""
    assert format_duration(60000) == "1m 0s"


def test_minute_with_seconds():
    """Test 65000ms (1 minute 5 seconds)"""
    assert format_duration(65000) == "1m 5s"


def test_multiple_minutes():
    """Test 125000ms (2 minutes 5 seconds)"""
    assert format_duration(125000) == "2m 5s"


def test_milliseconds_no_regression():
    """Verify millisecond format still works"""
    assert format_duration(999) == "999ms"


def test_seconds_no_regression():
    """Verify seconds format still works for values under 60s"""
    assert format_duration(5000) == "5.0s"
    assert format_duration(59999) == "60.0s"
