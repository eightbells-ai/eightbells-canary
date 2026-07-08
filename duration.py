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
