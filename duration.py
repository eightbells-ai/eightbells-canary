def format_duration(ms: int) -> str:
    """Render a millisecond duration as a short human string."""
    if ms < 1000:
        return f"{ms}ms"
    return f"{ms / 1000:.1f}s"
