def format_duration(ms: int) -> str:
    """Render a millisecond duration as a short human string."""
    if ms < 1000:
        return f"{ms}ms"
    
    total_seconds = ms // 1000
    
    if total_seconds < 60:
        # Less than a minute: show as seconds with one decimal place
        return f"{ms / 1000:.1f}s"
    
    # One minute or more
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    if minutes < 60:
        # Less than an hour: show as minutes and seconds
        return f"{minutes}m {seconds}s"
    
    # One hour or more
    hours = minutes // 60
    minutes = minutes % 60
    
    if minutes == 0:
        return f"{hours}h"
    
    return f"{hours}h {minutes}m"
