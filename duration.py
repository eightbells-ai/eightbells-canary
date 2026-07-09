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
    s = s.strip()
    
    # Handle milliseconds format: 'Xms'
    if s.endswith('ms'):
        return int(s[:-2])
    
    # Handle minutes and seconds format: 'Xm Ys'
    if 'm' in s and 's' in s:
        parts = s.split()
        minutes = int(parts[0][:-1])  # Remove 'm'
        seconds = int(parts[1][:-1])  # Remove 's'
        return minutes * 60000 + seconds * 1000
    
    # Handle seconds format: 'X.Xs' or 'Xs'
    if s.endswith('s'):
        seconds = float(s[:-1])
        return int(seconds * 1000)
