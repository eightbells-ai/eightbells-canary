def format_duration(ms: int) -> str:
    """Render a millisecond duration as a short human string.
    
    Formatting ranges:
    - < 1000ms: '{ms}ms'
    - 1000-59999ms: '{ms/1000:.1f}s'
    - 60000-3599999ms: '{m}m {s}s'
    - >= 3600000ms: '{h}h {m}m'
    """
    if ms < 1000:
        return f"{ms}ms"
    if ms < 60000:
        return f"{ms / 1000:.1f}s"
    if ms < 3600000:
        minutes = ms // 60000
        remaining_ms = ms % 60000
        seconds = remaining_ms // 1000
        return f"{minutes}m {seconds}s"
    # >= 3600000ms (1 hour or more)
    hours = ms // 3600000
    remaining_ms = ms % 3600000
    minutes = remaining_ms // 60000
    return f"{hours}h {minutes}m"
