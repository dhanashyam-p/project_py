from datetime import datetime


def current_time() -> datetime:
    """Return the current local date and time."""
    return datetime.now()