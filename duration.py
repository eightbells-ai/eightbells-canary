def format_duration(ms: int) -> str:
    """Render a millisecond duration as a short human string."""
    if ms < 1000:
        return f"{ms}ms"
    if ms >= 60000:
        minutes = ms // 60000
        remaining_ms = ms % 60000
        seconds = remaining_ms // 1000
        return f"{minutes}m {seconds}s"
    return f"{ms / 1000:.1f}s"


def parse_duration(s: str) -> int:
    """Parse a duration string and return milliseconds."""
    total_ms = 0
    parts = s.split()
    
    for part in parts:
        if part.endswith('ms'):
            # Parse milliseconds
            value = int(part[:-2])
            total_ms += value
        elif part.endswith('s'):
            # Parse seconds
            value = float(part[:-1])
            total_ms += int(value * 1000)
        elif part.endswith('m'):
            # Parse minutes
            value = int(part[:-1])
            total_ms += value * 60000
    
    return total_ms
