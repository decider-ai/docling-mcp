"""Date utility functions."""

from datetime import datetime, timezone


def get_created_at_date() -> str:
    """Get the current date and time in ISO format with UTC timezone."""
    return datetime.now(timezone.utc).isoformat()
