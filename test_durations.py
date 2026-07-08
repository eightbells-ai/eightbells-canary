import pytest
from durations import format_duration


def test_zero():
    """Test zero milliseconds."""
    assert format_duration(0) == "0ms"


def test_range1_upper_boundary():
    """Test range 1 upper boundary (999ms)."""
    assert format_duration(999) == "999ms"


def test_range1_to_range2_boundary():
    """Test range 1-2 boundary (1000ms → 1.0s)."""
    assert format_duration(1000) == "1.0s"


def test_mid_range2():
    """Test mid-range 2 (1500ms → 1.5s)."""
    assert format_duration(1500) == "1.5s"


def test_range2_upper_boundary():
    """Test range 2 upper boundary (59999ms → 60.0s)."""
    assert format_duration(59999) == "60.0s"


def test_range2_to_range3_boundary():
    """Test range 2-3 boundary (60000ms → 1m 0s)."""
    assert format_duration(60000) == "1m 0s"


def test_mid_range3_with_seconds():
    """Test mid-range 3 with non-zero seconds (125000ms → 2m 5s)."""
    assert format_duration(125000) == "2m 5s"


def test_multi_digit_minutes():
    """Test multi-digit minutes (600000ms → 10m 0s)."""
    assert format_duration(600000) == "10m 0s"


def test_range3_upper_boundary():
    """Test range 3 upper boundary (3599999ms → 59m 59s)."""
    assert format_duration(3599999) == "59m 59s"


def test_range3_to_range4_boundary():
    """Test range 3-4 boundary (3600000ms → 1h 0m)."""
    assert format_duration(3600000) == "1h 0m"


def test_mid_range4():
    """Test mid-range 4 (3665000ms → 1h 1m)."""
    assert format_duration(3665000) == "1h 1m"
