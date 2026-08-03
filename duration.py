def format_duration(ms: int) -> str:
    """Render a millisecond duration as a short human string.
    
    Args:
        ms: Duration in milliseconds
        
    Returns:
        Human-readable duration string (e.g., "500ms", "1.5s", "1m 5s")
    """
    if ms < 1000:
        return f"{ms}ms"
    if ms >= 60000:
        minutes = ms // 60000
        remaining_ms = ms % 60000
        seconds = remaining_ms // 1000
        return f"{minutes}m {seconds}s"
    return f"{ms / 1000:.1f}s"
